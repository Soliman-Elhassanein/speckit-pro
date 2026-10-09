#!/usr/bin/env python3
"""Deterministic check of the project baseline.

Reads .specify/memory/{product,architecture,decisions}.md and specs/. It keeps
two kinds of generated state:

  .specify/memory/baseline-state.json   the mode and the synced point of each part
  specs/<feature>/baseline-pins.json    content pins of the baseline entries that
                                        feature cites, and what it was verified on

Modes (default is a read-only check):
  --write             write the calculated cells: Delivery, Owning spec, part State
  --repin [TARGET]    record current pins: a spec folder, one spec.md or plan.md, or all
  --stamp [SPEC]      record the synced point of the parts in SPEC's plan, or of all parts
  --strict            treat warnings as errors
  --run-rule-checks   run the Check command of each architecture rule
  --mode MODE         set `advisory` (report, exit 0) or `blocking` (the default)
  --context           print the baseline entries for --ids and/or --paths
  --touched SPEC      print the parts and rules touched since that spec's baseline
  --scan              print a partition of tracked files, to recover a baseline

In blocking mode nothing is written when the check reports an error, and the
exit code is 1. In advisory mode errors are reported, the exit code is 0, and
the calculated cells and generated state are still written.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(?:CAP|PR|AR|D|Q)-\d{3,}\b")
DEFINED_RE = re.compile(r"^(?:CAP|PR|AR|D|Q)-\d{3,}$")
CAP_RE = re.compile(r"\bCAP-\d{3,}\b")
REQUIREMENT_RE = re.compile(r"\b(?:FR|AS|TR)-\d{3,}[a-z]?\b")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
# Only these header lines of a spec or plan cite the baseline; prose never does.
CITE_RE = re.compile(
    r"^\*\*(Implements|Changes|Product rules|Architecture rules|Decisions|Parts)\*\*:(.*)$", re.MULTILINE
)
SPEC_LABELS = ("implements", "changes", "product rules")
PLAN_LABELS = ("architecture rules", "decisions")
COMPLETION_RE = re.compile(r"^Completion:\s*(NOT DONE|DONE)\b", re.MULTILINE)
OUTCOME_RE = re.compile(r"^Outcome:\s*`?(NOT RUN|[a-z_]+)", re.MULTILINE)
TESTED_RE = re.compile(r"^Tested revision[^:\n]*:[ \t]*(\S.*)$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"<[A-Za-z][^<>\n]*>")
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
STATUSES = ("PASS", "FAIL", "NOT RUN", "BLOCKED")
NOT_PASSED_RE = re.compile(r"^(?:NOT RUN|FAIL|BLOCKED|SKIP|XFAIL|ERROR)")
FAILED_COUNT_RE = re.compile(r"\b([1-9]\d*)\s+(?:failed|failures?|errors?)\b", re.IGNORECASE)
FOUR_COUNTS_RE = re.compile(r"^\s*\d+\s*/\s*(\d+)\s*/\s*\d+\s*/\s*\d+\s*$")
COUNT_RE = re.compile(r"^[^|\n]*:\s*(\d+)\s*/\s*(\d+)\s*$", re.MULTILINE)
TASK_RE = re.compile(r"^\s*[-*]\s+\[([ xX])\]", re.MULTILINE)
HISTORY_RE = re.compile(r"^## Historical runs\b", re.MULTILINE)
BASELINE_LINE_RE = re.compile(r"^\*\*Baseline\*\*:\s*`?([0-9a-fA-F]{7,40})`?", re.MULTILINE)
VERSION_RE = re.compile(r"^\*\*Version\*\*:\s*([0-9][^\s|]*)", re.MULTILINE)
NOT_CODE_RE = re.compile(r"^\*\*Not code\*\*:(.*)$", re.MULTILINE)
DECISION_STATES = {"proposed", "approved", "superseded", "retired"}
BASELINE_FILES = ("product.md", "architecture.md", "decisions.md")
STATE_FILE = "baseline-state.json"
PINS_FILE = "baseline-pins.json"
# Calculated by this script, so a change to them is not a change to the entry.
CALCULATED = ("delivery", "owning spec", "state")
# Tracked files that are not product code unless a part maps them.
NOT_CODE_DEFAULT = ("specs", "docs", "*.md", "LICENSE*")
RULE_CHECK_TIMEOUT = 600
MANIFESTS = (
    "package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml", "pom.xml",
    "build.gradle", "build.gradle.kts", "settings.gradle.kts", "pubspec.yaml", "Gemfile", "composer.json",
)


def find_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return None


def git(root: Path, *args: str, stdin: str | None = None) -> list[str] | None:
    """Output lines of a git command, or None when git or the repository is unavailable."""
    try:
        done = subprocess.run(
            ["git", "-C", str(root), *args], input=stdin, capture_output=True, text=True, check=False
        )
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return [line for line in done.stdout.splitlines() if line.strip()]


def split_row(line: str) -> list[str] | None:
    """Raw cells of a Markdown table row. A pipe written as `\\|` does not end a cell."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    parts = re.split(r"(?<!\\)\|", stripped)
    return parts[1:-1] if len(parts) > 2 and not parts[-1].strip() else parts[1:]


def cells(line: str) -> list[str] | None:
    """Cells of a Markdown table row, or None for separators and non-rows."""
    raw = split_row(line)
    if raw is None:
        return None
    parts = [part.strip().replace("\\|", "|") for part in raw]
    if parts and all(re.fullmatch(r":?-+:?", part) for part in parts):
        return None
    return parts


def set_cell(line: str, column: int, value: str) -> str:
    raw = split_row(line) or []
    while len(raw) <= column:
        raw.append(" ")
    raw[column] = f" {value} "
    return "|" + "|".join(raw) + "|"


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


def section(text: str, heading: str) -> str:
    """Body of the `## heading` section, or an empty string."""
    found = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return found.group(1) if found else ""


def spec_key(value: str) -> str:
    """Path under specs/ from an owning-spec cell or an argument: `specs/001-x`, a link, a file, or `-`."""
    link = LINK_RE.search(value)
    target = (link.group(1) if link else value).strip("` ").replace("\\", "/").rstrip("/")
    if target in ("", "-"):
        return ""
    target = re.sub(r"/(?:spec|plan|tasks|verification)\.md$", "", target)
    if "/specs/" in target:
        target = target.split("/specs/", 1)[1]
    target = target[2:] if target.startswith("./") else target
    return target[len("specs/"):] if target.startswith("specs/") else target


def names_of(value: str) -> list[str]:
    """Comma separated names or patterns from a cell; backticks optional, `-` and `none` mean nothing."""
    found = [part.strip("` ").strip("/") for part in value.split(",")]
    return [part for part in found if part and part.lower() not in ("-", "none") and not part.startswith("[")]


def path_matches(path: str, pattern: str) -> bool:
    """A pattern without wildcards is a folder or file prefix; otherwise it is a glob."""
    if any(char in pattern for char in "*?["):
        return fnmatch.fnmatchcase(path, pattern)
    return path == pattern or path.startswith(pattern + "/")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def row_hash(header: list[str], row: list[str]) -> str:
    """Content pin of one baseline row, without the cells this script calculates."""
    return digest(" | ".join(cell for name, cell in zip(header, row) if name not in CALCULATED))


def file_hash(path: Path) -> str:
    return digest(path.read_text(encoding="utf-8")) if path.is_file() else ""


def write_atomic(path: Path, text: str) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


class Baseline:
    """The three baseline files, parsed."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.memory = root / ".specify" / "memory"
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.notes: list[str] = []
        self.entries: dict[str, dict] = {}  # ID -> file, line, header, row, record, raw
        self.parts: list[dict] = []
        self.stack: list[str] = []  # raw lines of the Stack table
        self.text: dict[str, str] = {}
        self.versions: dict[str, str] = {}
        for name in BASELINE_FILES:
            path = self.memory / name
            if not path.is_file():
                if name != "product.md":
                    self.errors.append(f"{name}: file is missing")
                continue
            text = path.read_text(encoding="utf-8")
            self.text[name] = text
            version = VERSION_RE.search(text)
            if version:
                self.versions[name] = version.group(1)
            lines = text.splitlines()
            for index, header, row in table_rows(text):
                if not row or row[0].startswith("["):
                    continue
                record = dict(zip(header, row))
                if name == "architecture.md" and header[0] == "part":
                    self.parts.append({
                        "name": row[0], "record": record, "header": header, "row": row, "line": index,
                        "raw": lines[index], "paths": names_of(record.get("paths", "")),
                    })
                if name == "architecture.md" and header[0] == "area":
                    self.stack.append(lines[index])
                if not DEFINED_RE.match(row[0]):
                    continue
                ident = row[0]
                if ident in self.entries:
                    self.errors.append(f"{name}:{index + 1}: {ident} is defined twice (also in {self.entries[ident]['file']})")
                    continue
                self.entries[ident] = {
                    "file": name, "line": index, "header": header, "row": row, "record": record, "raw": lines[index],
                }
            for match in LINK_RE.finditer(text):
                target = match.group(1)
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                if not (path.parent / target.split("#")[0]).exists():
                    self.errors.append(f"{name}: link does not resolve: {target}")
        declared = NOT_CODE_RE.search(self.text.get("architecture.md", ""))
        self.not_code = tuple(names_of(declared.group(1))) if declared else NOT_CODE_DEFAULT

    def of_kind(self, prefix: str) -> dict[str, dict]:
        return {ident: entry for ident, entry in sorted(self.entries.items()) if ident.startswith(prefix)}

    def status(self, ident: str) -> str:
        return self.entries[ident]["record"].get("status", "")

    def part(self, name: str) -> dict | None:
        return next((part for part in self.parts if part["name"].lower() == name.lower()), None)

    def parts_for(self, paths: list[str]) -> list[dict]:
        return [part for part in self.parts if any(path_matches(p, pat) for p in paths for pat in part["paths"])]

    def is_code(self, path: str) -> bool:
        """Product code: anything a part maps, and otherwise every file outside the process folders."""
        if self.parts_for([path]):
            return True
        return not path.startswith(".") and not any(path_matches(path, pattern) for pattern in self.not_code)

    def decisions_for(self, paths: list[str], part_names: set[str]) -> list[str]:
        found = []
        for ident, entry in self.of_kind("D-").items():
            affects = names_of(entry["record"].get("affects", ""))
            if any(a in part_names for a in affects) or any(path_matches(p, a) for p in paths for a in affects):
                found.append(ident)
        return found

    def product_decisions(self) -> list[str]:
        """Decisions that govern no path: they apply to what the product does."""
        return [i for i, e in self.of_kind("D-").items() if not names_of(e["record"].get("affects", ""))]

    def open_questions(self) -> dict[str, dict]:
        return {
            ident: entry for ident, entry in self.of_kind("Q-").items()
            if entry["record"].get("status", "open").lower() in ("", "open")
        }

    def pin_now(self, key: str) -> str | None:
        """Current content pin of a cited entry: an ID, `part:<name>`, or `stack`."""
        if key == "stack":
            return digest("\n".join(line.strip() for line in self.stack))
        if key.startswith("part:"):
            part = self.part(key[5:])
            return row_hash(part["header"], part["row"]) if part else None
        entry = self.entries.get(key)
        return row_hash(entry["header"], entry["row"]) if entry else None


def load_json(path: Path, errors: list[str], root: Path) -> dict:
    """A generated state file. A file that exists but cannot be read is an error, not an empty state."""
    if not path.is_file():
        return {}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(state, dict):
            return state
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    errors.append(f"{path.relative_to(root)}: not valid JSON; restore it from version control, or delete it and repin")
    return {}


def dump_json(state: dict) -> str:
    return json.dumps(state, indent=2, sort_keys=True) + "\n"


def working_files(root: Path) -> list[str] | None:
    """Tracked and untracked files that exist, without ignored ones."""
    listed = git(root, "ls-files", "-co", "--exclude-standard")
    if listed is None:
        return None
    return sorted({name for name in listed if (root / name).is_file()})


def part_hashes(root: Path, base: Baseline, files: list[str]) -> dict[str, str]:
    """One content hash per part, from the files it maps. It survives a squash or a rebase."""
    mapped = [name for name in files if base.parts_for([name])]
    blobs = git(root, "hash-object", "--stdin-paths", stdin="\n".join(mapped) + "\n") if mapped else []
    by_file = dict(zip(mapped, blobs or []))
    hashes = {}
    for part in base.parts:
        own = [name for name in mapped if any(path_matches(name, pattern) for pattern in part["paths"])]
        if own:
            hashes[part["name"]] = digest("\n".join(f"{name} {by_file.get(name, '')}" for name in own))
    return hashes


def done_gaps(spec_dir: Path, root: Path) -> list[str]:
    """Why the feature's own records do not support a `Completion: DONE` claim."""
    gaps = []
    if not (spec_dir / "plan.md").is_file():
        gaps.append("plan.md is missing")
    tasks = spec_dir / "tasks.md"
    if not tasks.is_file():
        gaps.append("tasks.md is missing")
    else:
        boxes = TASK_RE.findall(tasks.read_text(encoding="utf-8"))
        if not boxes:
            gaps.append("tasks.md has no tasks")
        elif boxes.count(" "):
            gaps.append(f"tasks.md has {boxes.count(' ')} unchecked task(s)")

    current = HISTORY_RE.split((spec_dir / "verification.md").read_text(encoding="utf-8"), maxsplit=1)[0]
    if PLACEHOLDER_RE.search(CODE_SPAN_RE.sub("", current)):
        gaps.append("the record still has unfilled <placeholders>")
    if not TESTED_RE.search(current):
        gaps.append("no tested revision or fingerprint is recorded")

    # Coverage: every requirement ID the spec defines needs a row that passed.
    required = set(REQUIREMENT_RE.findall((spec_dir / "spec.md").read_text(encoding="utf-8")))
    coverage = section(current, "Coverage")
    rows = table_rows(coverage)
    passed: set[str] = set()
    if not rows:
        gaps.append("the Coverage section has no rows")
    for _, header, row in rows:
        column = next((i for i, name in enumerate(header) if "status" in name), None)
        if column is None or column >= len(row):
            gaps.append("the Coverage table has no Status column")
            break
        status = row[column].strip("`* ")
        if status not in STATUSES:
            gaps.append(f"unknown status '{status}' in Coverage; use one of {', '.join(STATUSES)}")
        elif status == "PASS":
            passed.update(REQUIREMENT_RE.findall(" ".join(row)))
    if not required:
        gaps.append("spec.md defines no FR, AS or TR IDs to verify")
    missing = sorted(required - passed)
    if missing and rows:
        shown = ", ".join(missing[:6]) + (f" and {len(missing) - 6} more" if len(missing) > 6 else "")
        gaps.append(f"{len(missing)} ID(s) in spec.md have no passing Coverage row ({shown})")
    short = [found.group(0).strip() for found in COUNT_RE.finditer(coverage) if found.group(1) != found.group(2)]
    if short:
        gaps.append("coverage counts are incomplete (" + "; ".join(short) + ")")

    # Execution: at least one finished run, every one with exit code 0 and no failures.
    runs = table_rows(section(current, "Execution"))
    if not runs:
        gaps.append("the Execution section records no command")
    for _, header, row in runs:
        exit_column = next((i for i, name in enumerate(header) if "exit" in name), None)
        command = next((row[i] for i, name in enumerate(header) if "command" in name and i < len(row)), row[0])
        command = command.strip("` ")
        if exit_column is None or exit_column >= len(row):
            gaps.append("the Execution table has no Exit code column")
            break
        code = row[exit_column].strip("`* ")
        if code != "0":
            gaps.append(f"`{command}` has exit code '{code}', not 0")
        for cell in row:
            four = FOUR_COUNTS_RE.match(cell)
            if FAILED_COUNT_RE.search(cell) or (four and four.group(1) != "0"):
                gaps.append(f"`{command}` reports failures ({cell.strip()})")
                break

    # No row anywhere in the current record may be open, failed or skipped.
    open_rows = sum(
        1 for _, _, row in table_rows(current) if any(NOT_PASSED_RE.match(cell.strip("`* ")) for cell in row)
    )
    if open_rows:
        gaps.append(f"{open_rows} row(s) are NOT RUN, FAIL, BLOCKED or skipped")

    for match in LINK_RE.finditer(current):
        target = match.group(1).split("#")[0]
        if not target or "://" in match.group(1) or match.group(1).startswith("mailto:"):
            continue
        if not (spec_dir / target).exists() and not (root / target).exists():
            gaps.append(f"evidence link does not resolve: {target}")

    outcome = OUTCOME_RE.search(current)
    if not outcome or outcome.group(1) != "converged":
        gaps.append(f"the convergence Outcome is '{outcome.group(1) if outcome else 'missing'}', not 'converged'")
    return gaps


def print_context(base: Baseline, ids: list[str], paths: list[str]) -> int:
    """Exactly the entries a piece of work needs: by ID for specify, by path for plan."""
    missing = [ident for ident in ids if ident not in base.entries]
    for ident in missing:
        print(f"error: {ident} is not defined in the baseline")
    versions = ", ".join(f"{name[:-3]} {base.versions.get(name, 'unversioned')}" for name in base.text)
    print(f"Baseline versions: {versions}")

    def show(title: str, idents: list[str]) -> None:
        if idents:
            print(f"## {title}")
            for ident in idents:
                print(base.entries[ident]["raw"].strip())

    if not paths:
        purpose = section(base.text.get("product.md", ""), "Purpose and users").strip()
        if purpose:
            print("## Purpose and users")
            print(purpose)
        if not ids:
            print("## Capability index")
            for ident, entry in base.of_kind("CAP-").items():
                record = entry["record"]
                print(f"- {ident} [{record.get('decision', '')}, {record.get('delivery', '')}]: {record.get('promise', '')}")
        show("Cited entries", [ident for ident in ids if ident in base.entries])
        show("Product rules (apply to every feature)", list(base.of_kind("PR-")))
        decisions = base.product_decisions()
        show("Product decisions", [i for i in decisions if base.status(i).lower() == "accepted"])
        show("Rejected or superseded product decisions (do not propose these again)",
             [i for i in decisions if base.status(i).lower() != "accepted"])
        questions = base.open_questions()
        if ids:
            blocking = [i for i, e in questions.items() if set(ids) & set(CAP_RE.findall(e["record"].get("blocks", "")))]
            show("Open questions that block these capabilities (answer them before specifying)", blocking)
        else:
            show("Open questions", list(questions))
    if paths:
        if base.stack:
            print("## Stack (every plan must fit these choices)")
            for line in base.stack:
                print(line.strip())
        parts = base.parts_for(paths)
        names = {part["name"] for part in parts}
        print("## Parts touched")
        for part in parts:
            print(part["raw"].strip())
        print(f"**Parts**: {', '.join(sorted(names)) or 'none'}")
        for path in paths:
            if not base.parts_for([path]):
                print(f"- no part maps `{path}`")
        show("Architecture rules (apply to every plan)", list(base.of_kind("AR-")))
        governing = base.decisions_for(paths, names)
        show("Decisions governing these paths", [i for i in governing if base.status(i).lower() == "accepted"])
        show("Rejected or superseded here (do not propose these again)",
             [i for i in governing if base.status(i).lower() != "accepted"])
        contracts = section(base.text.get("architecture.md", ""), "Interfaces and contracts").strip()
        if contracts:
            print("## Interfaces and contracts")
            print(contracts)
    return 1 if missing else 0


def changed_since(root: Path, commit: str) -> list[str] | None:
    """Tracked and untracked files that differ from a commit, including uncommitted work."""
    committed = git(root, "diff", "--name-only", commit, "HEAD")
    if committed is None:
        return None
    pending = git(root, "status", "--porcelain", "--untracked-files=all") or []
    return sorted(set(committed) | {line[3:].split(" -> ")[-1].strip('"') for line in pending})


def print_touched(base: Baseline, spec: str) -> int:
    """Parts and rules touched by the work of one spec, from git, for the code review."""
    spec_path = base.root / "specs" / spec_key(spec) / "spec.md"
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
    files = [name for name in files if base.is_code(name)]
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
        top = name.split("/")[0] if "/" in name else "(root files)"
        if not top.startswith(".") and top not in ("specs", "docs") and not (top == "(root files)" and name.startswith(".")):
            buckets.setdefault(top, []).append(name)
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
    hidden = sorted({n.split("/")[0] for n in tracked if n.startswith(".") and "/" in n and not n.startswith(".specify/")})
    print(f"\nHidden folders (map one to a part if it is product code): {', '.join(hidden) or 'none'}")
    return 0


def head_version(root: Path, name: str) -> str | None:
    lines = git(root, "show", f"HEAD:.specify/memory/{name}")
    return "\n".join(lines) if lines is not None else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="write the calculated cells")
    parser.add_argument("--repin", nargs="?", const="*", default=None, metavar="TARGET", help="record pins for all specs, one folder, or one file")
    parser.add_argument("--stamp", nargs="?", const="*", default=None, metavar="SPEC", help="record the synced point of all parts, or of one spec's parts")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--run-rule-checks", action="store_true", help="run each architecture rule's Check command")
    parser.add_argument("--mode", choices=("advisory", "blocking"), help="set whether errors stop the work")
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
    root = root.resolve()
    if args.scan:
        return print_scan(root)

    memory = root / ".specify" / "memory"
    product_path = memory / "product.md"
    if not product_path.is_file():
        # A project that has not adopted the baseline is not blocked by it.
        print("note: this project has no .specify/memory/product.md, so there is no baseline to check")
        print("note: create one with the baseline amend command, or the baseline recover command when code exists")
        return 0

    base = Baseline(root)
    if args.context:
        split = lambda value: [item.strip() for item in value.split(",") if item.strip()]  # noqa: E731
        return print_context(base, split(args.ids), split(args.paths))
    if args.touched:
        return print_touched(base, args.touched)

    errors, warnings, notes = base.errors, base.warnings, base.notes
    writes: dict[Path, str] = {}  # applied only when the check reports no error
    state = load_json(memory / STATE_FILE, errors, root)
    state_before = dump_json(state)
    if args.mode:
        state["mode"] = args.mode
    advisory = state.get("mode") == "advisory"
    old_stamp = state.get("stamp")
    stamp = old_stamp if isinstance(old_stamp, dict) else {"commit": old_stamp or "", "parts": {}}
    legacy_pins = state.pop("pins", None) or {}  # the first version kept every pin in the state file
    capabilities = base.of_kind("CAP-")
    questions = base.open_questions()

    # Which spec, plan or folder --repin and --stamp name.
    specs_root = root / "specs"
    spec_dirs = sorted(p.parent for p in specs_root.rglob("spec.md")) if specs_root.is_dir() else []
    keys = {spec_dir.relative_to(specs_root).as_posix(): spec_dir for spec_dir in spec_dirs}
    repin_key = repin_doc = ""
    if args.repin not in (None, "*"):
        repin_key = spec_key(args.repin)
        repin_doc = Path(args.repin.rstrip("/")).name if args.repin.rstrip("/").endswith(".md") else ""
        if repin_key not in keys:
            errors.append(f"--repin {args.repin}: there is no specs/{repin_key}/spec.md")
    stamp_key = spec_key(args.stamp) if args.stamp not in (None, "*") else ""
    if stamp_key and stamp_key not in keys:
        errors.append(f"--stamp {args.stamp}: there is no specs/{stamp_key}/spec.md")

    # Each spec: what it implements and changes, what it cites, whether the cited rows moved, and whether it is done.
    implements: dict[str, set[str]] = {}
    changes: dict[str, set[str]] = {}
    done_specs: set[str] = set()
    expected_parts: set[str] = set()  # parts an unfinished feature says it is working in
    plan_parts: dict[str, list[str]] = {}
    for key, spec_dir in keys.items():
        where = f"specs/{key}"
        spec_text = (spec_dir / "spec.md").read_text(encoding="utf-8")
        cites = {label.lower(): rest for label, rest in CITE_RE.findall(spec_text)}
        implements[key] = set(CAP_RE.findall(cites.get("implements", "")))
        changes[key] = set(CAP_RE.findall(cites.get("changes", "")))
        plan_path = spec_dir / "plan.md"
        plan_text = plan_path.read_text(encoding="utf-8") if plan_path.is_file() else ""
        plan_cites = {label.lower(): rest for label, rest in CITE_RE.findall(plan_text)}
        plan_parts[key] = names_of(plan_cites.get("parts", ""))

        pins_path = spec_dir / PINS_FILE
        record = load_json(pins_path, errors, root)
        record_before = pins_path.read_text(encoding="utf-8") if pins_path.is_file() else ""
        pins: dict[str, dict[str, str]] = record.setdefault("pins", {})
        for doc in ("spec.md", "plan.md"):
            if doc not in pins and f"{where}/{doc}" in legacy_pins:
                pins[doc] = legacy_pins[f"{where}/{doc}"]

        # Done is a claim in verification.md that the rest of the feature's records must support.
        verification = spec_dir / "verification.md"
        completion = COMPLETION_RE.search(verification.read_text(encoding="utf-8")) if verification.is_file() else None
        done = bool(completion and completion.group(1) == "DONE")
        if done:
            gaps = done_gaps(spec_dir, root)
            if gaps:
                errors.append(f"{where}/verification.md: says Completion: DONE, but " + "; ".join(gaps))
                done = False
        if done:
            now = {doc: file_hash(spec_dir / doc) for doc in ("spec.md", "plan.md", "verification.md")}
            was = record.get("verified", {})
            moved = [doc for doc in ("spec.md", "plan.md") if was and was.get(doc) != now[doc]]
            if moved and was.get("verification.md") == now["verification.md"]:
                errors.append(
                    f"{where}: {' and '.join(moved)} changed after the feature was verified, and verification.md did not; "
                    "verify again on the changed requirements and record the run"
                )
                done = False
            else:
                record["verified"] = now
        else:
            record.pop("verified", None)
        if done:
            done_specs.add(key)
        else:
            expected_parts.update(plan_parts[key])

        named = implements[key] | changes[key]
        if not named:
            (warnings if done else errors).append(
                f"{where}/spec.md: no `**Implements**: CAP-NNN` or `**Changes**: CAP-NNN` line naming a capability"
            )
        for ident in sorted(named):
            entry = capabilities.get(ident)
            # Finished work stays valid after its capability is retired or superseded, never before approval.
            decision = entry["record"].get("decision", "").lower() if entry else "approved"
            if decision == "proposed" or (not done and decision != "approved"):
                errors.append(f"{where}/spec.md: names {ident}, which is not approved")
            for question, q_entry in questions.items():
                if not done and ident in CAP_RE.findall(q_entry["record"].get("blocks", "")):
                    errors.append(
                        f"{where}/spec.md: {ident} is blocked by open question {question}; "
                        "answer it through the baseline amend command first"
                    )

        for doc, text, labels in (("spec.md", spec_text, SPEC_LABELS), ("plan.md", plan_text, PLAN_LABELS)):
            if not text:
                continue
            doc_cites = cites if doc == "spec.md" else plan_cites
            cited = sorted(set(ID_RE.findall(" ".join(doc_cites.get(label, "") for label in labels))))
            if doc == "plan.md":
                cited += [f"part:{name}" for name in plan_parts[key]] + ["stack"]
            repin_this = args.repin is not None and (args.repin == "*" or (repin_key == key and repin_doc in ("", doc)))
            doc_pins = pins.setdefault(doc, {})
            for ident in cited:
                now_hash = base.pin_now(ident)
                if now_hash is None:
                    what = f"part '{ident[5:]}'" if ident.startswith("part:") else ident
                    errors.append(f"{where}/{doc}: cites {what}, which is not defined in the baseline")
                    continue
                if ident.startswith("D-") and not done and base.status(ident).lower() != "accepted":
                    errors.append(f"{where}/{doc}: cites {ident}, whose status is '{base.status(ident) or 'empty'}'")
                pinned = doc_pins.get(ident)
                if repin_this:
                    if pinned != now_hash:
                        print(f"pinned {ident} for {where}/{doc}" + (" (it had changed)" if pinned else ""))
                        doc_pins[ident] = now_hash
                elif pinned is None:
                    if not done:
                        warnings.append(f"{where}/{doc}: {ident} is not pinned; run with --repin specs/{key}/{doc}")
                elif pinned != now_hash:
                    if not done:
                        errors.append(
                            f"{where}/{doc}: {ident} changed in the baseline after this file was written; "
                            f"re-read it, update the file if needed, then run with --repin specs/{key}/{doc}"
                        )
                    elif ident.startswith("CAP-") and capabilities[ident]["record"].get("decision", "").lower() == "approved":
                        errors.append(
                            f"{where}/{doc}: {ident} changed after this feature was verified against it; "
                            f"add a spec that Changes {ident}, or verify again and run with --repin specs/{key}/{doc}"
                        )
            if repin_this:
                for ident in [i for i in doc_pins if i not in cited]:
                    del doc_pins[ident]
        for doc in [d for d in pins if not pins[d]]:
            del pins[doc]
        if pins or record.get("verified"):
            if dump_json(record) != record_before:
                writes[pins_path] = dump_json(record)

    # Capabilities: decision state, owning spec, and Delivery calculated from evidence.
    product_lines = base.text["product.md"].splitlines()
    product_changed = False
    delivery_now: dict[str, str] = {}
    for ident, entry in capabilities.items():
        record, header = entry["record"], entry["header"]
        where = f"product.md:{entry['line'] + 1}"
        decision = record.get("decision", "").lower()
        if decision not in DECISION_STATES:
            errors.append(f"{where}: {ident} has decision '{decision}'; use one of {sorted(DECISION_STATES)}")
        if "owning spec" not in header or "delivery" not in header:
            errors.append(f"{where}: the capabilities table needs the Owning spec and Delivery columns")
            continue
        owners = sorted(key for key, named in implements.items() if ident in named)
        changers = sorted(key for key, named in changes.items() if ident in named)
        if len(owners) > 1:
            errors.append(
                f"{where}: {ident} is implemented by {', '.join('specs/' + o for o in owners)}; "
                "one spec implements a capability, and a later spec lists it under `**Changes**:`"
            )
        if changers and not owners:
            errors.append(f"{where}: specs/{changers[0]} changes {ident}, but no spec implements it yet")
        cell_owner = spec_key(record.get("owning spec", ""))
        owner = owners[0] if len(owners) == 1 else ""
        if cell_owner and cell_owner != owner and len(owners) < 2:
            errors.append(
                f"{where}: {ident} names owning spec 'specs/{cell_owner}', "
                + (f"but specs/{owner} implements it" if owner else "whose spec.md does not list it under Implements")
            )
        elif owner and not cell_owner:
            if args.write:
                product_lines[entry["line"]] = set_cell(product_lines[entry["line"]], header.index("owning spec"), f"specs/{owner}")
                product_changed = True
                print(f"updated {ident}: Owning spec -> specs/{owner}")
            else:
                notes.append(f"{where}: {ident} is implemented by specs/{owner}; run with --write to record its owning spec")
        involved = owners + changers
        delivery = "unstarted" if not owners else "verified" if all(k in done_specs for k in involved) else "in progress"
        delivery_now[ident] = delivery
        current = record.get("delivery", "").lower()
        if current != delivery:
            if args.write:
                product_lines[entry["line"]] = set_cell(product_lines[entry["line"]], header.index("delivery"), delivery)
                product_changed = True
                print(f"updated {ident}: Delivery '{current}' -> '{delivery}'")
            elif current == "verified":
                errors.append(f"{where}: {ident} shows Delivery 'verified', but the evidence says '{delivery}'; run with --write")
            else:
                notes.append(f"{where}: {ident} shows Delivery '{current}', the evidence says '{delivery}'; run with --write")
    if product_changed:
        writes[product_path] = "\n".join(product_lines) + "\n"

    # Dependencies between capabilities.
    depends = {i: CAP_RE.findall(e["record"].get("depends on", "")) for i, e in capabilities.items()}
    for ident, needed in depends.items():
        for other in needed:
            if other not in capabilities:
                errors.append(f"product.md: {ident} depends on {other}, which is not defined")
            elif delivery_now.get(ident) == "in progress" and delivery_now.get(other) != "verified":
                warnings.append(f"product.md: {ident} is in progress and depends on {other}, whose Delivery is '{delivery_now.get(other)}'")
        seen: set[str] = set()
        queue = list(needed)
        while queue:
            other = queue.pop()
            if other == ident:
                errors.append(f"product.md: {ident} depends on itself through a cycle")
                break
            if other not in seen:
                seen.add(other)
                queue.extend(depends.get(other, []))

    # Rows are never deleted, and a decision is never rewritten: compare with the last commit.
    for name in base.text:
        before = head_version(root, name)
        if before is None:
            continue
        old_rows = {row[0]: (header, row) for _, header, row in table_rows(before) if row and DEFINED_RE.match(row[0])}
        for ident in sorted(set(old_rows) - set(base.entries)):
            errors.append(f"{name}: {ident} was deleted; rows are never deleted, so restore it and change its state instead")
        if name == "decisions.md":
            for ident, (header, row) in old_rows.items():
                entry = base.entries.get(ident)
                keep = lambda h, r: [c for n, c in zip(h, r) if n != "status"]  # noqa: E731
                if entry and keep(header, row) != keep(entry["header"], entry["row"]):
                    warnings.append(f"{name}: {ident} was rewritten; a changed decision gets a new row that supersedes the old one")

    # Code against the map: part state, unmapped code, and changes made outside the process.
    files = working_files(root)
    arch_text = base.text.get("architecture.md", "")
    arch_lines = arch_text.splitlines()
    arch_changed = False
    mapped = [part for part in base.parts if part["paths"]]
    if files is None:
        notes.append("not a git repository: code drift is not checked")
    elif not mapped:
        if any(base.is_code(name) for name in files):
            warnings.append("architecture.md maps no part to a path, so code drift cannot be checked; add Paths to the parts table")
    else:
        code = [name for name in files if base.is_code(name)]
        for part in mapped:
            built = any(path_matches(name, pattern) for name in code for pattern in part["paths"])
            calculated = "built" if built else "planned"
            if "state" not in part["header"]:
                if not built:
                    notes.append(f"architecture.md: part '{part['name']}' has no code yet; add a State column to the parts table to track it")
                continue
            current = part["record"].get("state", "").lower()
            if current == calculated:
                continue
            if current == "built":
                errors.append(
                    f"architecture.md: part '{part['name']}' is built, but its paths match no file any more; "
                    "run the baseline reconcile command"
                )
            elif args.write:
                arch_lines[part["line"]] = set_cell(arch_lines[part["line"]], part["header"].index("state"), calculated)
                arch_changed = True
                print(f"updated part '{part['name']}': State '{current}' -> '{calculated}'")
            else:
                notes.append(f"architecture.md: part '{part['name']}' shows State '{current}', the code says '{calculated}'; run with --write")
        loose = sorted({name.split("/")[0] + ("/" if "/" in name else "") for name in code if not base.parts_for([name])})
        for item in loose:
            warnings.append(
                f"`{item}` is tracked code that no part maps; add it to a part, list it under `**Not code**:` "
                "in architecture.md, or run the baseline recover command"
            )

        hashes = part_hashes(root, base, code)
        synced: dict[str, str] = dict(stamp.get("parts", {}))
        if args.stamp is not None and (args.stamp == "*" or stamp_key in keys):
            wanted = set(hashes)
            if args.stamp != "*":
                listed = {part["name"] for name in plan_parts[stamp_key] if (part := base.part(name))}
                wanted &= listed
                if not wanted:
                    notes.append(f"--stamp {args.stamp}: its plan.md lists no built part under `**Parts**:`, so nothing was stamped")
            for name in wanted:
                synced[name] = hashes[name]
            head = git(root, "rev-parse", "HEAD")
            stamp = {"commit": head[0] if head else stamp.get("commit", ""), "parts": synced}
        elif not synced:
            notes.append("no synced point recorded yet; run with --stamp once code and baseline agree")
        else:
            expected = {part["name"] for name in expected_parts if (part := base.part(name))}
            for name, now_hash in sorted(hashes.items()):
                if name in expected:
                    continue
                if name not in synced:
                    notes.append(f"part '{name}' has no synced point yet; run with --stamp once it agrees with the baseline")
                elif synced[name] != now_hash:
                    warnings.append(
                        f"part '{name}' changed since its synced point, and no unfinished feature lists it under `**Parts**:`; "
                        "run the baseline reconcile command"
                    )
    if arch_changed:
        writes[memory / "architecture.md"] = "\n".join(arch_lines) + "\n"
    if stamp.get("parts") or stamp.get("commit"):
        state["stamp"] = stamp
    if dump_json(state) != state_before:
        state["version"] = 2
        writes[memory / STATE_FILE] = dump_json(state)

    # Architecture rules that carry an executable check.
    for ident, entry in base.of_kind("AR-").items():
        command = entry["record"].get("check", "").strip("` ")
        if not command or command == "-" or command.startswith("["):
            continue
        if not args.run_rule_checks:
            notes.append(f"{ident} has a Check command; run with --run-rule-checks to execute it")
            continue
        try:
            ran = subprocess.run(
                command, shell=True, cwd=root, capture_output=True, text=True, check=False, timeout=RULE_CHECK_TIMEOUT
            )
            failed, output = ran.returncode != 0, ran.stdout + ran.stderr
        except subprocess.TimeoutExpired:
            failed, output = True, f"timed out after {RULE_CHECK_TIMEOUT} seconds"
        if failed:
            blocking = entry["record"].get("blocking", "").lower() in ("yes", "true", "blocking")
            tail = output.strip().splitlines()[-3:]
            message = f"{ident} check failed (`{command}`): " + (" / ".join(tail) or "no output")
            (errors if blocking else warnings).append(message)

    if args.strict:
        errors, warnings = errors + warnings, []
    for message in notes:
        print(f"note: {message}")
    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    changing = args.write or args.repin is not None or args.stamp is not None or bool(args.mode)
    if errors and not advisory:
        print(
            f"baseline check failed: {len(errors)} error(s), {len(warnings)} warning(s)"
            + ("; nothing was written" if changing else "")
        )
        return 1
    if changing:
        for path, text in writes.items():
            # Calculated cells need --write; the generated state follows any changing run.
            if path.name in (STATE_FILE, PINS_FILE) or args.write:
                write_atomic(path, text)
    if errors:
        print(f"baseline check failed: {len(errors)} error(s), {len(warnings)} warning(s)")
        print("advisory mode: reported, not blocking; switch with --mode blocking once the check is clean")
        return 0
    print(f"baseline check passed: {len(capabilities)} capabilities, {len(spec_dirs)} specs, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
