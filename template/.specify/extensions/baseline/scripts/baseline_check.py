#!/usr/bin/env python3
"""Deterministic check of the project baseline.

Reads .specify/memory/{product,architecture,decisions}.md and specs/, and keeps
a generated sidecar, .specify/memory/baseline-state.json, with the last synced
commit and one content pin per cited baseline entry.

Modes (default is a read-only check):
  --write             recalculate Delivery cells in product.md
  --repin [SPEC]      record current pins for all specs, or for one spec folder
  --stamp             record HEAD as the point where code and baseline agree
  --strict            treat warnings as errors
  --run-rule-checks   run the Check command of each architecture rule
  --context           print the baseline entries for --ids and/or --paths
  --touched SPEC      print the parts and rules touched since that spec's baseline
  --scan              print a partition of tracked files, to recover a baseline

Exit 0 when clean, 1 when any error is reported.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(?:CAP|PR|AR|D)-\d{3,}\b")
DEFINED_RE = re.compile(r"^(?:CAP|PR|AR|D)-\d{3,}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
COMPLETION_RE = re.compile(r"^Completion:\s*(NOT DONE|DONE)\b", re.MULTILINE)
BASELINE_LINE_RE = re.compile(r"^\*\*Baseline\*\*:\s*`?([0-9a-fA-F]{7,40})`?", re.MULTILINE)
DECISION_STATES = {"proposed", "approved", "superseded", "retired"}
BASELINE_FILES = ("product.md", "architecture.md", "decisions.md")
STATE_FILE = "baseline-state.json"
# Folders that hold process files, not product code.
NOT_CODE = ("specs", "docs")
MANIFESTS = (
    "package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "pom.xml",
    "build.gradle", "build.gradle.kts", "settings.gradle.kts", "pubspec.yaml", "Gemfile", "composer.json",
)


def find_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return None


def git(root: Path, *args: str) -> list[str] | None:
    """Output lines of a git command, or None when git or the repository is unavailable."""
    try:
        done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return [line for line in done.stdout.splitlines() if line.strip()]


def cells(line: str) -> list[str] | None:
    """Cells of a Markdown table row, or None for separators and non-rows."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    parts = [part.strip() for part in stripped.strip("|").split("|")]
    if all(re.fullmatch(r":?-+:?", part) for part in parts):
        return None
    return parts


def table_rows(text: str) -> list[tuple[int, list[str], list[str]]]:
    """(line index, header cells, row cells) for every data row of every table."""
    rows = []
    header: list[str] | None = None
    for index, line in enumerate(text.splitlines()):
        row = cells(line)
        if row is None:
            if not line.strip().startswith("|"):
                header = None
            continue
        if header is None:
            header = [cell.lower() for cell in row]
            continue
        rows.append((index, header, row))
    return rows


def spec_dir_of(value: str) -> str:
    """Folder name from an owning-spec cell such as `specs/001-x`, a link, or `-`."""
    link = LINK_RE.search(value)
    target = link.group(1) if link else value.strip("` ")
    target = target.strip("/")
    if target in ("", "-"):
        return ""
    target = re.sub(r"/spec\.md$", "", target)
    return target.split("/")[-1]


def patterns_of(value: str) -> list[str]:
    """Path patterns from a cell: comma separated, backticks optional, `-` means none."""
    found = [part.strip("` ").strip("/") for part in value.split(",")]
    return [part for part in found if part and part != "-" and not part.startswith("[")]


def path_matches(path: str, pattern: str) -> bool:
    """A pattern without wildcards is a folder or file prefix; otherwise it is a glob."""
    if any(char in pattern for char in "*?["):
        return fnmatch.fnmatchcase(path, pattern)
    return path == pattern or path.startswith(pattern + "/")


def row_hash(header: list[str], row: list[str]) -> str:
    """Content pin of one baseline row. Delivery is calculated, so it is left out."""
    kept = [cell for name, cell in zip(header, row) if name != "delivery"]
    return hashlib.sha256(" | ".join(kept).encode("utf-8")).hexdigest()[:16]


class Baseline:
    """The three baseline files, parsed."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.memory = root / ".specify" / "memory"
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.entries: dict[str, dict] = {}  # ID -> file, line, header, row, record
        self.parts: list[dict] = []
        for name in BASELINE_FILES:
            path = self.memory / name
            if not path.is_file():
                if name != "product.md":
                    self.errors.append(f"{name}: file is missing")
                continue
            text = path.read_text(encoding="utf-8")
            for index, header, row in table_rows(text):
                if not row:
                    continue
                record = dict(zip(header, row))
                if name == "architecture.md" and header and header[0] == "part" and not row[0].startswith("["):
                    self.parts.append({"name": row[0], "record": record, "paths": patterns_of(record.get("paths", ""))})
                if not DEFINED_RE.match(row[0]):
                    continue
                ident = row[0]
                if ident in self.entries:
                    self.errors.append(f"{name}:{index + 1}: {ident} is defined twice (also in {self.entries[ident]['file']})")
                    continue
                self.entries[ident] = {"file": name, "line": index, "header": header, "row": row, "record": record}
            for match in LINK_RE.finditer(text):
                target = match.group(1)
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                if not (path.parent / target.split("#")[0]).exists():
                    self.errors.append(f"{name}: link does not resolve: {target}")

    def of_kind(self, prefix: str) -> dict[str, dict]:
        return {ident: entry for ident, entry in sorted(self.entries.items()) if ident.startswith(prefix)}

    def status(self, ident: str) -> str:
        return self.entries[ident]["record"].get("status", "")

    def parts_for(self, paths: list[str]) -> list[dict]:
        return [part for part in self.parts if any(path_matches(p, pat) for p in paths for pat in part["paths"])]

    def decisions_for(self, paths: list[str], part_names: set[str]) -> list[str]:
        found = []
        for ident, entry in self.of_kind("D-").items():
            affects = patterns_of(entry["record"].get("affects", ""))
            if any(a in part_names for a in affects) or any(path_matches(p, a) for p in paths for a in affects):
                found.append(ident)
        return found

    def line(self, ident: str) -> str:
        entry = self.entries[ident]
        return "| " + " | ".join(entry["row"]) + " |"


def load_state(memory: Path) -> dict:
    path = memory / STATE_FILE
    if path.is_file():
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(state, dict):
                state.setdefault("pins", {})
                return state
        except json.JSONDecodeError:
            pass
    return {"version": 1, "stamp": "", "pins": {}}


def save_state(memory: Path, state: dict) -> None:
    (memory / STATE_FILE).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def is_code(path: str) -> bool:
    top = path.split("/")[0]
    return not top.startswith(".") and top not in NOT_CODE and "/" in path


def changed_since(root: Path, commit: str) -> list[str] | None:
    """Tracked and untracked files that differ from a commit, including uncommitted work."""
    committed = git(root, "diff", "--name-only", commit, "HEAD")
    if committed is None:
        return None
    pending = git(root, "status", "--porcelain", "--untracked-files=all") or []
    names = set(committed) | {line[3:].split(" -> ")[-1].strip('"') for line in pending}
    return sorted(names)


def print_context(base: Baseline, ids: list[str], paths: list[str]) -> int:
    """Exactly the entries a piece of work needs: by ID for specify, by path for plan."""
    missing = [ident for ident in ids if ident not in base.entries]
    for ident in missing:
        print(f"error: {ident} is not defined in the baseline")
    if not ids and not paths:
        print("## Capability index")
        for ident, entry in base.of_kind("CAP-").items():
            record = entry["record"]
            print(f"- {ident} [{record.get('decision', '')}, {record.get('delivery', '')}]: {record.get('promise', '')}")
    if ids:
        print("## Cited entries")
        for ident in ids:
            if ident in base.entries:
                print(base.line(ident))
    rules = base.of_kind("PR-") if not paths else {}
    if rules:
        print("## Product rules (apply to every feature)")
        for ident in rules:
            print(base.line(ident))
    if paths:
        parts = base.parts_for(paths)
        names = {part["name"] for part in parts}
        print("## Parts touched")
        for part in parts:
            print("| " + " | ".join(part["record"].values()) + " |")
        unmatched = [p for p in paths if not any(path_matches(p, pat) for part in base.parts for pat in part["paths"])]
        for path in unmatched:
            print(f"- no part maps `{path}`")
        print("## Architecture rules (apply to every plan)")
        for ident in base.of_kind("AR-"):
            print(base.line(ident))
        governing = base.decisions_for(paths, names)
        print("## Decisions governing these paths")
        for ident in governing:
            if base.status(ident).lower() == "accepted":
                print(base.line(ident))
        print("## Rejected or superseded here (do not propose these again)")
        for ident in governing:
            if base.status(ident).lower() != "accepted":
                print(base.line(ident))
    return 1 if missing else 0


def print_touched(base: Baseline, spec: str) -> int:
    """Parts and rules touched by the work of one spec, from git, for the code review."""
    spec_path = base.root / "specs" / spec_dir_of(spec) / "spec.md"
    if not spec_path.is_file():
        print(f"error: {spec_path.relative_to(base.root)} does not exist")
        return 1
    found = BASELINE_LINE_RE.search(spec_path.read_text(encoding="utf-8"))
    if not found:
        print(f"error: {spec_path.relative_to(base.root)} has no `**Baseline**: <commit>` line")
        return 1
    files = changed_since(base.root, found.group(1))
    if files is None:
        print(f"error: git cannot compare against {found.group(1)}")
        return 1
    files = [name for name in files if is_code(name)]
    print(f"## Files changed since {found.group(1)}: {len(files)}")
    for name in files:
        owners = [part["name"] for part in base.parts_for([name])]
        print(f"- {name} -> {', '.join(owners) if owners else 'no part'}")
    return print_context(base, [], files) if files else 0


def print_scan(root: Path) -> int:
    """Partition of tracked files by top-level folder. Reads names only, never contents."""
    tracked = git(root, "ls-files")
    if tracked is None:
        print("error: not a git repository; commit the code first, then scan")
        return 1
    buckets: dict[str, list[str]] = {}
    for name in tracked:
        if is_code(name):
            buckets.setdefault(name.split("/")[0], []).append(name)
    print("| Folder | Tracked files | Build manifests | Most common extensions |")
    print("|--------|---------------|-----------------|------------------------|")
    for folder, names in sorted(buckets.items()):
        manifests = sorted({n for n in names if n.split("/")[-1] in MANIFESTS})
        counts: dict[str, int] = {}
        for n in names:
            suffix = Path(n).suffix or "(none)"
            counts[suffix] = counts.get(suffix, 0) + 1
        top = ", ".join(f"{s} x{c}" for s, c in sorted(counts.items(), key=lambda item: -item[1])[:3])
        print(f"| {folder} | {len(names)} | {', '.join(manifests) or '-'} | {top} |")
    root_manifests = sorted(n for n in tracked if "/" not in n and n in MANIFESTS)
    print(f"\nRoot build manifests: {', '.join(root_manifests) or 'none'}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="recalculate Delivery cells in product.md")
    parser.add_argument("--repin", nargs="?", const="*", default=None, metavar="SPEC", help="record pins for all specs or one")
    parser.add_argument("--stamp", action="store_true", help="record HEAD as the synced point")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--run-rule-checks", action="store_true", help="run each architecture rule's Check command")
    parser.add_argument("--context", action="store_true", help="print entries for --ids and/or --paths")
    parser.add_argument("--ids", default="", help="comma separated baseline IDs")
    parser.add_argument("--paths", default="", help="comma separated file or folder paths")
    parser.add_argument("--touched", metavar="SPEC", help="print parts and rules touched since a spec's baseline")
    parser.add_argument("--scan", action="store_true", help="print a partition of tracked files")
    parser.add_argument("--root", type=Path, default=None, help="repository root (default: nearest folder with .specify)")
    args = parser.parse_args()

    root = args.root or find_root(Path.cwd())
    if root is None or not (root / ".specify").is_dir():
        print("error: no .specify folder found; run from inside a Spec Kit project", file=sys.stderr)
        return 1
    if args.scan:
        return print_scan(root)

    memory = root / ".specify" / "memory"
    product_path = memory / "product.md"
    if not product_path.is_file():
        print(f"error: {product_path.relative_to(root)} is missing; run the baseline amend command", file=sys.stderr)
        return 1

    base = Baseline(root)
    if args.context:
        split = lambda value: [item.strip() for item in value.split(",") if item.strip()]  # noqa: E731
        return print_context(base, split(args.ids), split(args.paths))
    if args.touched:
        return print_touched(base, args.touched)

    errors, warnings, notes = base.errors, base.warnings, base.notes
    capabilities = base.of_kind("CAP-")
    state = load_state(memory)
    pins: dict[str, dict[str, str]] = state["pins"]
    state_changed = False

    # What each spec implements, what specs and plans cite, and whether the cited rows moved.
    implements: dict[str, set[str]] = {}
    specs_root = root / "specs"
    spec_dirs = sorted(p for p in specs_root.iterdir() if (p / "spec.md").is_file()) if specs_root.is_dir() else []
    in_progress: list[str] = []
    live_docs: set[str] = set()
    for spec_dir in spec_dirs:
        spec_text = (spec_dir / "spec.md").read_text(encoding="utf-8")
        line = re.search(r"^\*\*Implements\*\*:(.*)$", spec_text, re.MULTILINE)
        named = set(re.findall(r"\bCAP-\d{3,}\b", line.group(1))) if line else set()
        implements[spec_dir.name] = named
        where = f"specs/{spec_dir.name}/spec.md"
        if not named:
            errors.append(f"{where}: no `**Implements**: CAP-NNN` line naming a capability")
        for ident in sorted(named):
            entry = capabilities.get(ident)
            if entry and entry["record"].get("decision", "").lower() != "approved":
                errors.append(f"{where}: implements {ident}, which is not approved")
        verification = spec_dir / "verification.md"
        completion = COMPLETION_RE.search(verification.read_text(encoding="utf-8")) if verification.is_file() else None
        done = bool(completion and completion.group(1) == "DONE")
        if not done:
            in_progress.append(spec_dir.name)
        for doc in ("spec.md", "plan.md"):
            doc_path = spec_dir / doc
            if not doc_path.is_file():
                continue
            key = f"specs/{spec_dir.name}/{doc}"
            live_docs.add(key)
            cited = sorted(set(ID_RE.findall(doc_path.read_text(encoding="utf-8"))))
            repin_this = args.repin is not None and args.repin in ("*", spec_dir.name, f"specs/{spec_dir.name}")
            for ident in cited:
                if ident not in base.entries:
                    errors.append(f"{key}: cites {ident}, which is not defined in the baseline")
                    continue
                if ident.startswith("D-") and base.status(ident).lower() != "accepted":
                    errors.append(f"{key}: cites {ident}, whose status is '{base.status(ident) or 'empty'}'")
                entry = base.entries[ident]
                now = row_hash(entry["header"], entry["row"])
                pinned = pins.get(key, {}).get(ident)
                if repin_this:
                    if pinned != now:
                        pins.setdefault(key, {})[ident] = now
                        state_changed = True
                elif pinned is None:
                    notes.append(f"{key}: {ident} is not pinned yet; run with --repin {spec_dir.name}")
                elif pinned != now and not done:
                    errors.append(
                        f"{key}: {ident} changed in the baseline after this file was written; "
                        f"re-read it, update the file if needed, then run with --repin {spec_dir.name}"
                    )
            if repin_this and key in pins:
                for ident in [i for i in pins[key] if i not in cited]:
                    del pins[key][ident]
                    state_changed = True
    if args.repin is not None:
        for key in [k for k in pins if k not in live_docs]:
            del pins[key]
            state_changed = True

    # Capabilities: state, owning spec, and Delivery calculated from evidence.
    product_lines = product_path.read_text(encoding="utf-8").splitlines()
    product_changed = False
    for ident, entry in capabilities.items():
        record, header, row = entry["record"], entry["header"], entry["row"]
        where = f"product.md:{entry['line'] + 1}"
        decision = record.get("decision", "").lower()
        if decision not in DECISION_STATES:
            errors.append(f"{where}: {ident} has decision '{decision}'; use one of {sorted(DECISION_STATES)}")
        owner = spec_dir_of(record.get("owning spec", ""))
        delivery = "unstarted"
        if owner:
            if owner not in implements:
                errors.append(f"{where}: {ident} names owning spec '{owner}', but specs/{owner}/spec.md does not exist")
            else:
                if ident not in implements[owner]:
                    errors.append(f"{where}: {ident} is owned by specs/{owner}, whose spec.md does not list it under Implements")
                delivery = "in progress" if owner in in_progress else "verified"
        if "delivery" not in header:
            errors.append(f"{where}: the capabilities table has no Delivery column")
            continue
        column = header.index("delivery")
        current = row[column].lower() if column < len(row) else ""
        if current == delivery:
            continue
        if args.write:
            parts = product_lines[entry["line"]].split("|")
            parts[column + 1] = f" {delivery} "
            product_lines[entry["line"]] = "|".join(parts)
            product_changed = True
            print(f"updated {ident}: Delivery '{current}' -> '{delivery}'")
        else:
            errors.append(f"{where}: {ident} shows Delivery '{current}', evidence says '{delivery}'; run with --write")

    # Every implemented capability must point back at its spec: one owning spec per promise.
    for spec_name, named in sorted(implements.items()):
        for ident in sorted(named):
            entry = capabilities.get(ident)
            if entry is None:
                continue  # already reported as undefined
            owner = spec_dir_of(entry["record"].get("owning spec", ""))
            if owner != spec_name:
                errors.append(f"specs/{spec_name}/spec.md: implements {ident}, but product.md names '{owner or '-'}' as its owning spec")

    # Code against the map: dangling parts, unmapped code, and changes made outside the process.
    tracked = git(root, "ls-files")
    mapped = [part for part in base.parts if part["paths"]]
    if tracked is None:
        notes.append("not a git repository: code drift is not checked")
    elif not mapped:
        if any(is_code(name) for name in tracked):
            warnings.append("architecture.md maps no part to a path, so code drift cannot be checked; add Paths to the parts table")
    else:
        code = [name for name in tracked if is_code(name)]
        for part in mapped:
            for pattern in part["paths"]:
                if not any(path_matches(name, pattern) for name in code):
                    errors.append(f"architecture.md: part '{part['name']}' maps `{pattern}`, which matches no tracked file")
        loose = sorted({name.split("/")[0] for name in code if not base.parts_for([name])})
        for folder in loose:
            warnings.append(f"`{folder}/` has tracked code that no part maps; add it to a part or run the baseline recover command")
        head = git(root, "rev-parse", "HEAD")
        if args.stamp and head:
            if state.get("stamp") != head[0]:
                state["stamp"] = head[0]
                state_changed = True
        elif not state.get("stamp"):
            notes.append("no synced point recorded yet; run with --stamp once code and baseline agree")
        else:
            changed = changed_since(root, state["stamp"])
            if changed is None:
                warnings.append(f"the synced point {state['stamp'][:8]} is not in this repository's history; run with --stamp")
            else:
                moved = [name for name in changed if is_code(name) and base.parts_for([name])]
                if moved and in_progress:
                    notes.append(f"{len(moved)} mapped file(s) changed since the synced point; feature in progress: {', '.join(in_progress)}")
                elif moved:
                    shown = ", ".join(moved[:5]) + (f" and {len(moved) - 5} more" if len(moved) > 5 else "")
                    warnings.append(
                        f"{len(moved)} mapped file(s) changed since the synced point {state['stamp'][:8]} "
                        f"with no feature in progress ({shown}); run the baseline reconcile command"
                    )

    # Architecture rules that carry an executable check.
    for ident, entry in base.of_kind("AR-").items():
        command = entry["record"].get("check", "").strip("` ")
        if not command or command == "-" or command.startswith("["):
            continue
        if not args.run_rule_checks:
            notes.append(f"{ident} has a Check command; run with --run-rule-checks to execute it")
            continue
        done = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True, check=False)
        if done.returncode != 0:
            blocking = entry["record"].get("blocking", "").lower() in ("yes", "true", "blocking")
            tail = (done.stdout + done.stderr).strip().splitlines()[-3:]
            message = f"{ident} check failed (`{command}`): " + (" / ".join(tail) or "no output")
            (errors if blocking else warnings).append(message)

    if product_changed:
        product_path.write_text("\n".join(product_lines) + "\n", encoding="utf-8")
    if state_changed:
        save_state(memory, state)

    if args.strict:
        errors, warnings = errors + warnings, []
    for message in notes:
        print(f"note: {message}")
    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    if errors:
        print(f"baseline check failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"baseline check passed: {len(capabilities)} capabilities, {len(spec_dirs)} specs, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
