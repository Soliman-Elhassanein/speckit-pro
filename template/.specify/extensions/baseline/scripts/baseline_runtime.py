"""Bounded Bash execution with pipeline failures and process-group cleanup."""
from __future__ import annotations

import os
import selectors
import signal
import subprocess
import time


def run(command: str, cwd, timeout: float = 600, limit: int = 2_000_000) -> tuple[int, str]:
    process = subprocess.Popen(['bash', '-o', 'pipefail', '-c', command], cwd=cwd,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               start_new_session=True)
    output = bytearray()
    reason = ''
    deadline = time.monotonic() + timeout
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            while selector.get_map():
                if time.monotonic() >= deadline:
                    reason = f'timed out after {timeout} seconds'
                    break
                for key, _ in selector.select(min(.1, max(0, deadline - time.monotonic()))):
                    data = os.read(key.fileobj.fileno(), 65536)
                    if not data:
                        selector.unregister(key.fileobj)
                    elif len(output) + len(data) > limit:
                        output.extend(data[:max(0, limit - len(output))])
                        reason = f'output exceeded {limit} bytes'
                        break
                    else:
                        output.extend(data)
                if reason:
                    break
        if reason:
            try: os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError: pass
        process.wait(timeout=max(.1, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        reason = f'timed out after {timeout} seconds'
        try: os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        process.wait()
    finally:
        process.stdout.close()
    return (124 if reason else process.returncode), output.decode('utf-8', errors='replace') + ('\n' + reason if reason else '')
