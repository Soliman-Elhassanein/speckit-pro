"""Per-checkout locking and recoverable, compare-before-apply file updates."""
from __future__ import annotations

import base64
import contextlib
import fcntl
import json
import os
import tempfile
from pathlib import Path


def atomic(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=path.name + '.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        Path(name).unlink(missing_ok=True)


def contents(path: Path) -> bytes | None:
    return path.read_bytes() if path.is_file() else None


@contextlib.contextmanager
def locked(root: Path):
    # Machine-local state; each worktree has its own .specify directory.
    local = root / '.specify' / '.baseline-local'
    local.mkdir(parents=True, exist_ok=True)
    with (local / 'lock').open('a+b') as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield local


def recover(root: Path, local: Path) -> None:
    journal = local / 'journal.json'
    if not journal.exists():
        return
    data = json.loads(journal.read_text())
    if not isinstance(data, dict) or not all(isinstance(n, str) and (b is None or isinstance(b, str)) for n, b in data.items()):
        raise ValueError('invalid transaction journal schema')
    for name, old in data.items():
        path = root / name
        if path.resolve().is_relative_to(root) is False:
            raise ValueError('invalid transaction journal path')
        if old is None:
            path.unlink(missing_ok=True)
        else:
            atomic(path, base64.b64decode(old, validate=True))
    journal.unlink()


def transact(root: Path, local: Path, writes: dict[Path, str], snapshot: dict[Path, bytes | None]) -> None:
    if any(contents(p) != data for p, data in snapshot.items()):
        raise ValueError('inputs changed during validation; retry on a stable working tree')
    if not writes:
        return
    journal = local / 'journal.json'
    old = {p.relative_to(root).as_posix(): contents(p) for p in writes}
    atomic(journal, json.dumps({n: None if b is None else base64.b64encode(b).decode()
                               for n, b in old.items()}).encode())
    try:
        for path, text in writes.items():
            atomic(path, text.encode())
    except BaseException:
        recover(root, local)
        raise
    journal.unlink()
