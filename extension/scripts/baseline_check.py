#!/usr/bin/env python3
"""Validate baseline intent, feature pins and evidence bound to current inputs.

Default checks and --gate are read-only. --gate always blocks on errors, requires
an adopted baseline/history base and runs executable architecture rules.
--feature scopes feature diagnostics; global structure and history remain checked.
--repin records reviewed citations; stale pins need --reason. --record-run executes
planned gates and saves logs plus verification-run.json. --write accepts supported
DONE evidence; --stamp records per-part reconciliation without renewing tests.
Delivery, ownership and part state are calculated on read (--status/--json).
Mutations use a checkout lock, input comparison and recoverable transaction journal.
Advisory mode permits recovery diagnostics but never accepts invalid completion.
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
import time
import uuid
from datetime import datetime, timezone
from baseline_store import contents, locked, recover, transact
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
COMPLETION_RE = re.compile(r"^Completion:\s*(NOT DONE|DONE|ABANDONED)\b", re.MULTILINE)
OUTCOME_RE = re.compile(r"^Outcome:\s*`?(NOT RUN|[a-z_]+)", re.MULTILINE)
TESTED_RE = re.compile(r"^Tested revision[^:\n]*:[ \t]*(\S.*)$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"<(?:actual[^<>\n]*|feature|IDs|TR|path|command|local evidence reference|covered|total|passing|met|complete|ID|outcome|change|method and status|run/fingerprint|run of[^<>\n]*|Missing[^<>\n]*|Retain prior[^<>\n]*|Actual assessment[^<>\n]*|locks/toolchain[^<>\n]*|browser/device[^<>\n]*|repository-owned path)>", re.IGNORECASE)
CODE_SPAN_RE = re.compile(r"`[^`\n]*`")
STATUSES = ("PASS", "FAIL", "NOT RUN", "BLOCKED")
NOT_PASSED_RE = re.compile(r"^(?:NOT RUN|FAIL|BLOCKED|SKIP|XFAIL|ERROR)", re.IGNORECASE)
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
# A coding agent never lists itself as a contributor. These match the agent's name in the name part
# of an author, a committer or a trailer; a person's own name and address are never matched.
AGENT_NAME_RES = (
    re.compile(r"^claude(?:\s+(?:code|opus|sonnet|haiku|fable|instant|\d).*)?$", re.IGNORECASE),
    re.compile(
        r"\b(?:chatgpt|codex|copilot|gemini|cursor agent|cursoragent|devin ai|aider|windsurf|codeium|"
        r"google-labs-jules|amazon q|openhands|cline|tabnine)\b", re.IGNORECASE,
    ),
    re.compile(r"\[bot\]", re.IGNORECASE),
)
AGENT_EMAILS = ("noreply@anthropic.com", "cursoragent@cursor.com")
TRAILER_RE = re.compile(
    r"^\s*(co-authored-by|signed-off-by|authored-by|co-developed-by|generated-by|assisted-by)\s*:\s*(.+)$", re.IGNORECASE
)
GENERATED_RE = re.compile(
    r"(?:\U0001F916.*\b(?:generated|created|written)\b)|"
    r"\b(?:generated|created|written|authored|assisted|co-authored)\s+(?:with|by)\b.*"
    r"\b(?:claude|chatgpt|codex|copilot|gemini|cursor|devin|aider|windsurf|codeium|jules|openhands|cline|an? ai\b|ai assistant)",
    re.IGNORECASE,
)
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
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16] if path.is_file() else ""


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
                if len(row) != len(header):
                    self.errors.append(f"{name}:{index + 1}: malformed row {row[0]}; escape pipes as \\| (expected {len(header)} cells, got {len(row)})")
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


def is_agent(identity: str) -> bool:
    """Whether `Name <email>` names a coding agent."""
    name, _, email = identity.partition("<")
    name, email = name.strip(), email.strip("> ").lower()
    return email in AGENT_EMAILS or any(pattern.search(name) for pattern in AGENT_NAME_RES)


def attribution_problems(message: str, identities: dict[str, str]) -> list[str]:
    """Places where a commit names a coding agent as a contributor."""
    problems = [f"the {role} is `{who}`" for role, who in identities.items() if is_agent(who)]
    for line in message.splitlines():
        if line.startswith("#"):
            continue
        trailer = TRAILER_RE.match(line)
        if trailer and is_agent(trailer.group(2)):
            problems.append(f"the line `{line.strip()}`")
        elif GENERATED_RE.search(line):
            problems.append(f"the line `{line.strip()}`")
    return problems


def check_commit_message(root: Path, path: Path) -> int:
    identities = {}
    for role, variable in (("author", "GIT_AUTHOR_IDENT"), ("committer", "GIT_COMMITTER_IDENT")):
        ident = git(root, "var", variable)
        if ident:
            identities[role] = re.sub(r"\s+\d+\s+[+-]\d{4}$", "", ident[0])
    problems = attribution_problems(path.read_text(encoding="utf-8", errors="replace"), identities)
    for problem in problems:
        print(f"error: this commit names a coding agent as a contributor: {problem}", file=sys.stderr)
    if problems:
        print("error: commit as the user alone; remove the line, or set the user's own git identity", file=sys.stderr)
    return 1 if problems else 0


def agent_commits(root: Path, since: str) -> list[str]:
    """Commits after the synced commit (or only the last one) that name an agent as a contributor."""
    span = [f"{since}..HEAD"] if since and git(root, "merge-base", "--is-ancestor", since, "HEAD") is not None else ["-1", "HEAD"]
    try:
        done = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%h%x1f%an <%ae>%x1f%cn <%ce>%x1f%B%x1e", *span],
            capture_output=True, text=True, check=False,
        )
    except OSError:
        return []
    found = []
    for record in done.stdout.split("\x1e") if done.returncode == 0 else []:
        fields = record.strip("\n").split("\x1f")
        if len(fields) == 4:
            problems = attribution_problems(fields[3], {"author": fields[1], "committer": fields[2]})
            if problems:
                found.append(f"commit {fields[0]} names a coding agent as a contributor ({problems[0]})")
    return found


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
    errors.append(f"{path.relative_to(root)}: not valid JSON; restore it from version control; do not delete accepted evidence state")
    return {}


def dump_json(state: dict) -> str:
    return json.dumps(state, indent=2, sort_keys=True) + "\n"


def git_paths(root: Path, *args: str) -> list[str] | None:
    """NUL-separated paths preserve spaces, Unicode and rename metadata safely."""
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
    return [os.fsdecode(p) for p in result.stdout.split(b'\0') if p] if result.returncode == 0 else None


def working_files(root: Path) -> list[str] | None:
    """Tracked and untracked files that exist, without ignored ones."""
    listed = git_paths(root, 'ls-files', '-z', '-co', '--exclude-standard')
    if listed is None:
        return None
    return sorted({name for name in listed if (root / name).is_file()})


def part_hashes(root: Path, base: Baseline, files: list[str]) -> dict[str, str]:
    """One content hash per part, from the files it maps. It survives a squash or a rebase."""
    mapped = [name for name in files if base.parts_for([name])]
    by_file = {name: file_hash(root / name) for name in mapped}
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
            for link in LINK_RE.finditer(contracts):
                target = link.group(1).split("#")[0]
                if "://" in target:
                    print(f"Contract omitted (external reference): {target}")
                    continue
                path = (base.memory / target).resolve()
                if not path.is_relative_to(base.root):
                    base.errors.append(f"contract is outside repository: {target}")
                elif path.is_file():
                    if path.stat().st_size > 65536:
                        base.errors.append(f"contract exceeds 64 KiB context limit; load explicitly: {target}")
                    else:
                        print(f"### Contract {target}\n{path.read_text(encoding='utf-8')}")
    for message in base.errors:
        print(f"error: {message}")
    if base.errors or missing:
        print("Context is INCOMPLETE; resolve these errors before using it as authority")
    return 1 if missing or base.errors else 0


def changed_since(root: Path, commit: str) -> list[str] | None:
    """Tracked and untracked files that differ from a commit, including uncommitted work."""
    committed = git_paths(root, 'diff', '--name-only', '-z', commit)
    if committed is None:
        return None
    pending = git_paths(root, 'ls-files', '--others', '--exclude-standard', '-z') or []
    return sorted(set(committed) | set(pending))


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
    top = git(root, 'rev-parse', '--show-toplevel')
    if not top or Path(top[0]).resolve() != root:
        return None
    lines = git(root, "show", f"HEAD:.specify/memory/{name}")
    return "\n".join(lines) if lines is not None else None



# v3 stores accepted evidence per feature. Shared baseline rows are never rewritten.
RUN_FILE = 'verification-run.json'
HEX = re.compile(r'^[0-9a-f]{16}$')


def state_schema(data: dict, kind: str) -> bool:
    def hashes(value):
        return isinstance(value, dict) and all(isinstance(k, str) and isinstance(v, str) and HEX.fullmatch(v) for k, v in value.items())
    if not isinstance(data, dict) or data.get('version', 3) not in (2, 3):
        return False
    if kind == 'state':
        stamp = data.get('stamp', {})
        return (data.get('mode', 'blocking') in ('advisory', 'blocking')
                and isinstance(data.get('accepted_base', ''), str)
                and isinstance(stamp, dict) and hashes(stamp.get('parts', {})))
    pins = data.get('pins', {})
    if not isinstance(pins, dict) or not all(isinstance(k, str) and hashes(v) for k, v in pins.items()):
        return False
    if not isinstance(data.get('verified', {}), dict) or not isinstance(data.get('accepted', {}), dict):
        return False
    accepted = data.get('accepted', {})
    if accepted and (not isinstance(accepted.get('run'), str) or not isinstance(accepted.get('inputs'), dict) or set(accepted['inputs']) != {'artifacts', 'baseline', 'code', 'contracts'} or any(not hashes(v) for v in accepted['inputs'].values())):
        return False
    transitions = data.get('transitions', {})
    return (isinstance(transitions, dict) and all(isinstance(v, dict) for v in transitions.values())
            and isinstance(data.get('review', {}), dict))


def read_state(path: Path, errors: list[str], root: Path, kind: str = 'pins') -> dict:
    data = load_json(path, errors, root)
    if not state_schema(data, kind):
        errors.append(f'{path.relative_to(root)}: invalid {kind} schema; restore state from version control')
        return {}
    return data


def feature_dirs(root: Path) -> dict[str, Path]:
    result = {}
    specs = root / 'specs'
    for path in sorted(specs.rglob('spec.md'), key=lambda p: (len(p.parts), str(p))) if specs.is_dir() else []:
        if not any(parent in result.values() for parent in path.parent.parents):
            result[path.parent.relative_to(specs).as_posix()] = path.parent
    return result


def citations(text: str) -> dict[str, str]:
    return {label.lower(): value for label, value in CITE_RE.findall(text)}


def input_binding(root: Path, base: Baseline, folder: Path) -> dict:
    spec, plan = (folder / 'spec.md').read_text(), (folder / 'plan.md').read_text()
    fields, design = citations(spec), citations(plan)
    ids = set(ID_RE.findall(' '.join(fields.get(k, '') for k in SPEC_LABELS)))
    ids.update(ID_RE.findall(' '.join(design.get(k, '') for k in PLAN_LABELS)))
    # Global rules and product decisions govern every feature, even when a citation was omitted.
    ids.update(base.of_kind('PR-')); ids.update(base.of_kind('AR-')); ids.update(base.product_decisions())
    named = set(CAP_RE.findall(fields.get('implements', '') + fields.get('changes', '')))
    ids.update(i for i, q in base.of_kind('Q-').items() if named & set(CAP_RE.findall(q['record'].get('blocks', ''))))
    shared = re.search(r'^\*\*Verification inputs\*\*:(.*)$', base.text.get('architecture.md', ''), re.M)
    parts = sorted(set(names_of(design.get('parts', ''))) | set(names_of(shared.group(1)) if shared else []))
    entries = {i: base.pin_now(i) for i in sorted(ids)}
    entries['stack'] = base.pin_now('stack')
    constitution = base.memory / 'constitution.md'
    if constitution.is_file(): entries['constitution'] = file_hash(constitution)
    entries.update({f'part:{name}': base.pin_now(f'part:{name}') for name in parts})
    code = part_hashes(root, base, working_files(root) or [])
    tasks = (folder / 'tasks.md').read_text() if (folder / 'tasks.md').is_file() else ''
    # Checkbox bookkeeping is excluded; changed task meaning is still a tested input.
    tasks = re.sub(r'(^\s*[-*]\s+)\[[ xX]\]', r'\1[]', tasks, flags=re.MULTILINE)
    contracts = {}
    for link in LINK_RE.finditer(section(base.text.get('architecture.md', ''), 'Interfaces and contracts')):
        target = link.group(1).split('#')[0]
        path = (base.memory / target).resolve()
        if '://' not in target and path.is_relative_to(root) and path.is_file():
            contracts[path.relative_to(root).as_posix()] = file_hash(path)
    return {'artifacts': {'spec.md': digest(spec), 'plan.md': digest(plan), 'tasks.md': digest(tasks)},
            'baseline': entries, 'code': {n: code.get(n, digest('')) for n in parts}, 'contracts': contracts}


def evidence_path(root: Path, folder: Path, value: str) -> Path | None:
    link = LINK_RE.fullmatch(value.strip())
    target = (link.group(1) if link else value).strip('` ').split('#')[0]
    if not target or '://' in target or target.startswith('/'):
        return None
    for candidate in (folder / target, root / target):
        path = candidate.resolve()
        if path.is_relative_to(root) and path.is_file():
            return path
    return None


def quality_gates(plan: str) -> list[dict]:
    gates = []
    for _, header, row in table_rows(section(plan, 'Quality gates')):
        record = dict(zip(header, row))
        if len(row) != len(header) or not all(record.get(k, '').strip('` ') for k in ('gate', 'working directory', 'exact command')):
            raise ValueError('Quality gates needs nonempty Gate, Working directory and Exact command columns; escape pipes')
        gates.append({k: record[k].strip('` ') for k in ('gate', 'working directory', 'exact command')})
    if not gates:
        raise ValueError('plan.md needs at least one complete Quality gates row')
    return gates


def run_evidence(root: Path, base: Baseline, folder: Path, writes: dict[Path, str]) -> dict:
    from baseline_runtime import run
    binding = input_binding(root, base, folder)
    run_id = uuid.uuid4().hex
    checks = []
    for n, gate in enumerate(quality_gates((folder / 'plan.md').read_text())):
        cwd = (root / gate['working directory']).resolve()
        if not cwd.is_relative_to(root) or not cwd.is_dir():
            raise ValueError('quality gate working directory must exist inside repository')
        code, output = run(gate['exact command'], cwd, RULE_CHECK_TIMEOUT)
        log = folder / 'evidence' / f'{run_id}-{n}.log'
        writes[log] = output
        checks.append({**gate, 'exit': code, 'evidence': log.relative_to(root).as_posix(), 'digest': digest(output)})
    if input_binding(root, base, folder) != binding:
        raise ValueError('test inputs changed during execution; no run was accepted')
    result = {'version': 3, 'id': run_id, 'date': datetime.now(timezone.utc).isoformat(),
              'inputs': binding, 'checks': checks, 'observations': []}
    # Archive superseded machine records without relabeling their results.
    old = folder / RUN_FILE
    if old.exists():
        writes[folder / 'evidence' / f'previous-{file_hash(old)}.json'] = old.read_text()
    writes[old] = dump_json(result)
    return result


def validate_run(root: Path, base: Baseline, folder: Path, historical: bool = False) -> tuple[list[str], dict]:
    gaps = []
    path = folder / RUN_FILE
    record = load_json(path, gaps, root)
    if record.get('version') != 3 or not re.fullmatch(r'[0-9a-f]{32}', str(record.get('id', ''))):
        return gaps + ['a v3 verification-run.json with a run ID is required; execute --record-run'], record
    now = input_binding(root, base, folder)
    inputs = record.get('inputs')
    if not isinstance(inputs, dict) or set(inputs) != set(now) or any(not isinstance(inputs[k], dict) for k in now):
        return gaps + ['verification-run.json has invalid input bindings'], record
    compare = ('artifacts',) if historical else tuple(now)
    for key in compare:
        if inputs[key] != now[key]:
            gaps.append(f'{key} changed after the feature was verified; execute new verification on current inputs')
    checks = record.get('checks')
    if not isinstance(checks, list) or not checks:
        return gaps + ['run has no executable checks'], record
    expected = quality_gates((folder / 'plan.md').read_text())
    actual = []
    for check in checks:
        if not isinstance(check, dict) or not all(isinstance(check.get(k), str) and check[k] for k in ('gate', 'exact command', 'working directory', 'evidence', 'digest')):
            gaps.append('run has missing command, directory or evidence fields'); continue
        actual.append({k: check[k] for k in ('gate', 'working directory', 'exact command')})
        evidence = evidence_path(root, folder, check['evidence'])
        if evidence is None or file_hash(evidence) != check['digest']:
            gaps.append('run evidence is missing or changed: ' + check['evidence'])
        if type(check.get('exit')) is not int or check['exit'] != 0:
            gaps.append('run command did not succeed: ' + check['exact command'])
        if evidence:
            output = evidence.read_text(errors='replace')
            if re.search(r'\b[1-9]\d*\s+(failed|errors?|skipped|xfailed)\b', output, re.I):
                gaps.append('required run reports failures/skips/xfails: ' + check['evidence'])
    if actual != expected:
        gaps.append('run does not match every planned quality gate')
    report = folder / 'verification.md'
    if report.is_file():
        execution = table_rows(section(HISTORY_RE.split(report.read_text(), maxsplit=1)[0], 'Execution'))
        if len(execution) != len(checks):
            gaps.append('Execution must report every recorded gate exactly once')
        for (_, header, row), check in zip(execution, checks):
            data = dict(zip(header, row))
            if not isinstance(check, dict) or not all(isinstance(check.get(k), str) for k in ('working directory', 'exact command', 'evidence')): continue
            if any(data.get(k, '').strip('` ') != check.get(k) for k in ('working directory', 'exact command')) or evidence_path(root, folder, data.get('evidence', '')) != evidence_path(root, folder, check.get('evidence', '')):
                gaps.append('Execution command, directory or log differs from recorded run')
    observations = record.get('observations', [])
    if not isinstance(observations, list):
        gaps.append('observations must be a list')
    else:
        for obs in observations:
            if not isinstance(obs, dict) or not all(isinstance(obs.get(k), str) and obs[k] for k in ('method', 'platform', 'expected', 'observed', 'evidence', 'digest')) or obs.get('status') != 'PASS' or evidence_path(root, folder, obs.get('evidence', '')) is None:
                gaps.append('manual observation needs method, platform, expected/observed, PASS and local evidence')
            elif file_hash(evidence_path(root, folder, obs['evidence'])) != obs['digest']:
                gaps.append('manual observation evidence changed')
        manual = table_rows(section(report.read_text(), 'Additional acceptance evidence')) if report.is_file() else []
        if len(manual) != len(observations):
            gaps.append('acceptance report must match the recorded manual observations')
        for (_, header, row), obs in zip(manual, observations):
            data = dict(zip(header, row))
            if not isinstance(obs, dict): continue
            if any(data.get(k) != obs.get(k) for k in ('expected', 'observed')):
                gaps.append('acceptance expected/observed differs from recorded observation')
    return gaps, record


def complete_gaps(folder: Path, root: Path) -> list[str]:
    gaps = done_gaps(folder, root)
    plan = folder / 'plan.md'
    if plan.is_file():
        try:
            quality_gates(plan.read_text())
        except ValueError as exc:
            gaps.append(str(exc))
        if not section(plan.read_text(), 'Verification plan').strip():
            gaps.append('plan.md needs a Verification plan')
    current = HISTORY_RE.split((folder / 'verification.md').read_text(), maxsplit=1)[0]
    for _, header, row in table_rows(current):
        if len(row) != len(header):
            gaps.append('malformed evidence table; escape pipes'); continue
        for n, name in enumerate(header):
            if 'status' in name and row[n].strip('`* ').split(' / ')[0] not in STATUSES:
                gaps.append(f'unknown status {row[n]!r}; use PASS, FAIL, NOT RUN or BLOCKED')
    for _, header, row in table_rows(section(current, 'Execution')):
        data = dict(zip(header, row))
        for name in ('working directory', 'exact command', 'evidence'):
            if not data.get(name, '').strip('` '):
                gaps.append(f'Execution requires nonempty {name}')
        if evidence_path(root, folder, data.get('evidence', '')) is None:
            gaps.append('Execution evidence must reference an existing repository file')
        counts = data.get('passed / failed / skipped / xfailed', '')
        four = re.fullmatch(r'\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*', counts)
        if not four:
            gaps.append('Execution requires numeric passed / failed / skipped / xfailed counts')
        if (four and any(int(four[n]) for n in (2, 3, 4))) or re.search(r'\b[1-9]\d*\s+(skipped|xfailed)\b', counts, re.I):
            gaps.append('required skipped/xfailing tests block DONE, even with a reason')
    for _, header, row in table_rows(section(current, 'Additional acceptance evidence')):
        data = dict(zip(header, row))
        if not all(data.get(k, '').strip() for k in ('as / sc', 'method and platform', 'expected', 'observed', 'status / evidence')):
            gaps.append('acceptance observations need nonempty ID, method/platform, expected, observed and status/evidence')
        link = LINK_RE.search(data.get('status / evidence', ''))
        if not link or evidence_path(root, folder, link.group(0)) is None:
            gaps.append('acceptance observation needs existing local evidence')
    return gaps


def check_project(args, root: Path, local: Path) -> int:
    base = Baseline(root)
    errors, warnings, notes = base.errors, [], []
    writes = {}
    initial_files = working_files(root)
    snapshot = {root / n: contents(root / n) for n in (initial_files or [])}
    state_path = base.memory / STATE_FILE
    before_state_errors = len(errors)
    state = read_state(state_path, errors, root, 'state')
    state_valid = len(errors) == before_state_errors
    # Policy preferences can be initialized before any baseline exists.
    if args.mode and state_valid:
        state['mode'] = args.mode
    advisory = state.get('mode') == 'advisory' and not args.gate
    if not (base.memory / 'product.md').is_file():
        adopted = state.get('adopted') or any((root / 'specs').rglob(PINS_FILE)) or head_version(root, 'product.md') is not None
        if args.gate or adopted:
            errors.append('required/adopted product.md is missing; restore the baseline')
        else:
            errors[:] = [e for e in errors if e not in ('product.md: file is missing', 'architecture.md: file is missing', 'decisions.md: file is missing')]
            notes.append('no baseline to check (non-adopter discovery)')
        if args.mode and not errors:
            state.update(version=3)
            transact(root, local, {state_path: dump_json(state)}, snapshot)
        for m in notes: print('note: ' + m)
        for m in errors: print('error: ' + m)
        return int(bool(errors))
    if args.touched:
        return print_touched(base, args.touched)

    keys = feature_dirs(root)
    target = ''
    if args.feature:
        if args.feature == 'current':
            pointer = load_json(root / '.specify' / 'feature.json', errors, root)
            target = spec_key(str(pointer.get('feature_directory', '')))
        else:
            target = spec_key(args.feature)
        if not target or target not in keys:
            errors.append('--feature must identify an existing feature (current reads .specify/feature.json)')
    repin_key = spec_key(args.repin) if args.repin not in (None, '*') else ''
    repin_doc = Path(args.repin.rstrip('/')).name if args.repin and args.repin.rstrip('/').endswith('.md') else ''
    if repin_key and repin_key not in keys:
        errors.append(f'--repin: no specs/{repin_key}/spec.md')
    if repin_doc and repin_doc not in ('spec.md', 'plan.md'):
        errors.append('--repin targets only spec.md or plan.md')
    recorded_result = None
    records, features, ferrors, fwarnings = {}, {}, {}, {}
    owners, changers = {}, {}
    capabilities = base.of_kind('CAP-')
    common_parts = re.search(r'^\*\*Verification inputs\*\*:(.*)$', base.text.get('architecture.md', ''), re.M)
    for name in names_of(common_parts.group(1)) if common_parts else []:
        if base.part(name) is None: errors.append(f'undefined shared Verification inputs part: {name}')
    for key, folder in keys.items():
        fe, fw = [], []
        ferrors[key], fwarnings[key] = fe, fw
        path = folder / PINS_FILE
        record = read_state(path, fe, root)
        records[key] = record
        snapshot.setdefault(path, contents(path))
        spec = (folder / 'spec.md').read_text()
        plan = (folder / 'plan.md').read_text() if (folder / 'plan.md').is_file() else ''
        cs, cp = citations(spec), citations(plan)
        named = set(CAP_RE.findall(cs.get('implements', '') + cs.get('changes', '')))
        completion_path = folder / 'verification.md'
        text = completion_path.read_text() if completion_path.is_file() else ''
        match = COMPLETION_RE.search(text)
        claim = match.group(1) if match else 'NOT DONE'
        features[key] = {'folder': folder, 'spec': spec, 'plan': plan, 'named': named,
                         'parts': names_of(cp.get('parts', '')), 'claim': claim, 'done': False,
                         'changes': set(CAP_RE.findall(cs.get('changes', '')))}
        for ident in CAP_RE.findall(cs.get('implements', '')): owners.setdefault(ident, []).append(key)
        for ident in CAP_RE.findall(cs.get('changes', '')): changers.setdefault(ident, []).append(key)
        if not named: fe.append('spec.md has no **Implements**: or **Changes**: capability')
        for ident in named:
            if ident not in capabilities: fe.append(f'spec.md: cites {ident}, which is not defined')
        pins = record.setdefault('pins', {})
        for doc, document, labels in (('spec.md', spec, SPEC_LABELS), ('plan.md', plan, PLAN_LABELS)):
            if not document: continue
            refs = citations(document)
            cited = sorted(set(ID_RE.findall(' '.join(refs.get(k, '') for k in labels))))
            if doc == 'plan.md': cited += ['stack'] + [f'part:{n}' for n in features[key]['parts']]
            dp = pins.setdefault(doc, {})
            repinning = args.repin is not None and (args.repin == '*' or (key == repin_key and repin_doc in ('', doc)))
            for ident in cited:
                now = base.pin_now(ident)
                if now is None:
                    fe.append(f'{doc}: cites {ident}, which is not defined in the baseline'); continue
                if repinning:
                    if dp.get(ident) != now and dp.get(ident) and not args.reason:
                        fe.append(f'{doc}: acknowledging stale {ident} requires --reason')
                    else: dp[ident] = now
                elif ident not in dp:
                    (fe if claim == 'DONE' else fw).append(f'{doc}: {ident} is not pinned; run --repin specs/{key}/{doc}')
                elif dp[ident] != now and claim not in ('DONE', 'ABANDONED') and not args.structural:
                    fe.append(f'{doc}: {ident} changed in the baseline; re-read and --repin specs/{key}/{doc} --reason ...')
            if repinning:
                pins[doc] = {i: dp[i] for i in cited if i in dp}
                record['pin_review'] = {'reason': args.reason or 'initial pins', 'date': datetime.now(timezone.utc).isoformat()}
        # Downstream review acknowledges the current spec explicitly, separately from execution.
        review = record.get('review', {})
        current_spec = digest(spec)
        if review and review.get('spec') != current_spec and not args.structural:
            if args.acknowledge and (target == key or repin_key == key) and args.reason:
                record['review'] = {'spec': current_spec, 'reason': args.reason}
            else:
                fe.append('spec.md changed: plan/tasks need review; use --feature ... --acknowledge --reason after updating them')
        elif not review and args.repin is not None and (args.repin == '*' or repin_key == key):
            record['review'] = {'spec': current_spec, 'reason': args.reason or 'initial planning'}
        if claim == 'ABANDONED': notes.append(f'specs/{key}: abandoned; no drift exemption')

    # Freeze each change's predecessor and capability revisions at initial spec repin.
    historical = set()
    edges = {}
    for ident, list_of_changes in changers.items():
        original = owners.get(ident, [])
        if len(original) != 1:
            errors.append(f'{ident}: a Changes spec requires exactly one implementing owner'); continue
        for key in list_of_changes:
            record = records[key]
            transition = record.setdefault('transitions', {}).get(ident)
            if transition is None and args.repin is not None and (args.repin == '*' or repin_key == key):
                requested = re.search(r'^\*\*Previous change\*\*:\s*(.+)$', features[key]['spec'], re.M)
                predecessor = spec_key(requested.group(1)) if requested else original[0]
                if predecessor not in features or ident not in features[predecessor]['named'] or predecessor == key:
                    ferrors[key].append(f'{ident}: invalid Previous change'); continue
                accepted = records[predecessor].get('accepted', {})
                previous = accepted.get('inputs', {}).get('baseline', {}).get(ident)
                if not previous:
                    ferrors[key].append(f'{ident}: predecessor needs accepted evidence before preparing a change'); continue
                transition = {'predecessor': predecessor, 'from': previous, 'to': base.pin_now(ident)}
                record['transitions'][ident] = transition
            if not isinstance(transition, dict) or not all(isinstance(transition.get(k), str) for k in ('predecessor', 'from', 'to')):
                ferrors[key].append(f'{ident}: missing revision transition; repin the new spec'); continue
            pred = transition['predecessor']
            if pred not in features or ident not in features[pred]['named'] or pred == key:
                ferrors[key].append(f'{ident}: invalid transition predecessor'); continue
            old = records[pred].get('accepted', {}).get('inputs', {}).get('baseline', {}).get(ident)
            if old != transition['from'] or not HEX.fullmatch(transition['from']) or not HEX.fullmatch(transition['to']):
                ferrors[key].append(f'{ident}: transition does not match accepted predecessor revision'); continue
            edge = (ident, pred)
            if edge in edges:
                errors.append(f'{ident}: conflicting change branches {edges[edge]} and {key}; resolve the transition')
            edges[edge] = key
        # Only a chain rooted in the actual owner can supersede its evidence.
        cursor, seen = original[0], set()
        while (ident, cursor) in edges:
            if cursor in seen:
                errors.append(f'{ident}: change transition cycle'); break
            seen.add(cursor)
            successor = edges[(ident, cursor)]
            if features[successor]['claim'] != 'ABANDONED' and records[successor]['transitions'][ident]['to'] == base.pin_now(ident):
                historical.update((k, ident) for k in seen if records[k].get('accepted'))
            cursor = successor

    for key, feature in features.items():
        folder, fe = feature['folder'], ferrors[key]
        record = records[key]
        accepted = record.get('accepted', {})
        is_historical = bool(accepted) and bool(feature['named']) and all((key, i) in historical or capabilities.get(i, {}).get('record', {}).get('decision') in ('retired', 'superseded') for i in feature['named'])
        for ident in feature['named']:
            entry = capabilities.get(ident)
            if not entry: continue
            if entry['record'].get('decision') != 'approved' and not is_historical:
                fe.append(f'{ident} is not approved')
            if not is_historical:
                for q, question in base.open_questions().items():
                    if ident in CAP_RE.findall(question['record'].get('blocks', '')):
                        fe.append(f'{ident} is blocked by open question {q}')
        for ident in ID_RE.findall(citations(feature['plan']).get('decisions', '')):
            if ident in base.entries and base.status(ident) != 'accepted' and not is_historical:
                fe.append(f'plan.md: cites {ident}, whose status is {base.status(ident)!r}')
        if args.record_run and key == target and not errors and not fe:
            if args.dry_run:
                notes.extend('would execute ' + g['exact command'] for g in quality_gates(feature['plan']))
            else:
                recorded_result = run_evidence(root, base, folder, writes)
        if feature['claim'] == 'DONE' and not args.structural and not (args.record_run and key == target):
            fe.extend(complete_gaps(folder, root))
            if not (folder / PINS_FILE).is_file(): fe.append('completed pins are missing; restore them before accepting evidence')
            if (folder / 'plan.md').is_file():
                run_gaps, run_record = validate_run(root, base, folder, is_historical)
                fe.extend(run_gaps)
                if is_historical and (accepted.get('run') != run_record.get('id') or accepted.get('inputs') != run_record.get('inputs')):
                    fe.append('historical run differs from accepted evidence; restore the original record')
                # First/renewed acceptance must satisfy current policy (above).
                if not fe:
                    feature['done'] = True
                    if args.write and not is_historical:
                        record['accepted'] = {'run': run_record['id'], 'inputs': run_record['inputs']}
        if args.require_done and (not target or key == target) and not feature['done'] and feature['claim'] != 'ABANDONED':
            fe.append('final gate requires supported DONE with current evidence')
        if feature['claim'] == 'NOT DONE' and not args.structural:
            latest = git(root, 'log', '-1', '--format=%ct', '--', str(folder.relative_to(root)))
            last = int(latest[0]) if latest else max(p.stat().st_mtime for p in folder.glob('*.md'))
            if time.time() - last > args.inactive_days * 86400:
                fwarnings[key].append(f'unfinished feature inactive for {args.inactive_days} days; review or mark ABANDONED')

    status = {'capabilities': {}, 'parts': {}}
    for ident, entry in capabilities.items():
        if entry['record'].get('decision') not in DECISION_STATES: errors.append(f'{ident}: invalid decision state')
        own = owners.get(ident, [])
        if len(own) > 1: errors.append(f'{ident}: multiple owners; a later spec lists it under `**Changes**:`')
        involved = own + [k for k in changers.get(ident, []) if features[k]['claim'] != 'ABANDONED']
        valid = bool(own) and all(features[k]['done'] and not ferrors[k] for k in involved)
        status['capabilities'][ident] = {'owner': 'specs/' + own[0] if len(own) == 1 else '',
                                         'delivery': 'verified' if valid else 'in progress' if own else 'unstarted'}
    dependencies = {i: CAP_RE.findall(e['record'].get('depends on', '')) for i, e in capabilities.items()}
    for ident, needed in dependencies.items():
        for other in needed:
            if other not in capabilities: errors.append(f'{ident}: undefined dependency {other}')
            elif status['capabilities'][ident]['delivery'] == 'in progress' and status['capabilities'][other]['delivery'] != 'verified':
                warnings.append(f'{ident} depends on unverified {other}')
        queue, seen = list(needed), set()
        while queue:
            other = queue.pop()
            if other == ident: errors.append(f'{ident} depends on itself through a cycle'); break
            if other not in seen: seen.add(other); queue.extend(dependencies.get(other, []))
    for ident, entry in base.of_kind('D-').items():
        if entry['record'].get('status') not in ('accepted', 'rejected') and not re.fullmatch(r'superseded by D-\d{3,}', entry['record'].get('status', '')):
            errors.append(f'{ident}: invalid decision status')

    # Accepted history, not every proposal ever present in any commit.
    comparison = args.base or state.get('accepted_base')
    if comparison:
        resolved = git(root, 'rev-parse', '--verify', comparison + '^{commit}')
        if not resolved: errors.append(f'accepted history base unavailable: {comparison}; fetch history or provide --base')
    elif args.gate:
        errors.append('required gate needs --base or an adopted accepted_base; initialize with --write --base HEAD')
    for revision in dict.fromkeys(r for r in (comparison, 'HEAD') if r):
        for name in BASELINE_FILES:
            lines = git(root, 'show', f'{revision}:.specify/memory/{name}')
            if lines is None: continue
            old_rows = {r[0]: (h, r) for _, h, r in table_rows('\n'.join(lines)) if r and DEFINED_RE.match(r[0])}
            for ident in set(old_rows) - set(base.entries): errors.append(f'{name}: {ident} was deleted against {revision}; restore or retire it')
            if name == 'decisions.md':
                for ident, (header, row) in old_rows.items():
                    current = base.entries.get(ident)
                    keep = lambda h, r: [c for n, c in zip(h, r) if n != 'status']
                    if current and keep(header, row) != keep(current['header'], current['row']):
                        errors.append(f'{name}: {ident} was rewritten; create a new superseding decision')

    files = working_files(root)
    hashes = part_hashes(root, base, files or [])
    expected = {p for key, f in features.items() if f['claim'] == 'NOT DONE' for p in f['parts']}
    stamp_key = spec_key(args.stamp) if args.stamp not in (None, '*') else ''
    if stamp_key and stamp_key not in features: errors.append('--stamp identifies no feature')
    if stamp_key and not features.get(stamp_key, {}).get('done'): errors.append('--stamp of a feature requires accepted DONE')
    for part in base.parts:
        name = part['name']
        status['parts'][name] = 'built' if name in hashes else 'planned'
        if part['record'].get('state') == 'built' and name not in hashes:
            errors.append(f'part {name!r} is built but paths match no file any more')
        stamp_path = base.memory / 'stamps' / (digest(name) + '.json')
        snapshot.setdefault(stamp_path, contents(stamp_path))
        old = load_json(stamp_path, errors, root)
        if old and (old.get('version') != 3 or old.get('part') != name or not isinstance(old.get('digest'), str) or not HEX.fullmatch(old['digest'])):
            errors.append(f'invalid stamp schema for {name}')
        synced = old.get('digest') or state.get('stamp', {}).get('parts', {}).get(name)
        moved = synced and hashes.get(name) != synced
        stamping = args.stamp is not None and (args.stamp == '*' or name in features.get(stamp_key, {}).get('parts', []))
        if stamping and name in hashes:
            if moved and not args.reason and not stamp_key: errors.append(f'stamping changed part {name} requires --reason')
            writes[stamp_path] = dump_json({'version': 3, 'part': name, 'digest': hashes[name], 'reason': args.reason or 'accepted feature / initial baseline'})
        elif moved and name not in expected and not args.structural:
            warnings.append(f'part {name!r} changed since its synced point; reconcile it')
    if files is None: warnings.append('not a git repository: code scope and history unavailable')
    for name in files or []:
        if base.is_code(name) and not base.parts_for([name]): warnings.append(f'`{name}` is code that no part maps')
    for message in agent_commits(root, str(state.get('accepted_base', ''))): warnings.append(message)
    if args.run_rule_checks or args.gate:
        from baseline_runtime import run
        for ident, entry in base.of_kind('AR-').items():
            command = entry['record'].get('check', '').strip('` ')
            if command and command != '-' and not command.startswith('['):
                code, output = run(command, root, RULE_CHECK_TIMEOUT)
                if code:
                    message = f'{ident} check failed (`{command}`): ' + ' / '.join(output.strip().splitlines()[-3:])
                    (errors if entry['record'].get('blocking', '').lower() in ('yes', 'true', 'blocking') else warnings).append(message)

    global_errors = list(errors)
    scoped = [target] if target in features else list(features)
    for key in features:
        if key in scoped:
            errors.extend(f'specs/{key}: {m}' for m in ferrors[key])
            warnings.extend(f'specs/{key}: {m}' for m in fwarnings[key])
        else:
            notes.extend(f'other feature specs/{key}: {m}' for m in ferrors[key] + fwarnings[key])
    if args.strict: errors.extend(warnings); warnings = []
    changing = args.write or args.repin is not None or args.stamp is not None or args.record_run or args.acknowledge
    # Explicit preference changes are separate from accepting delivery or pins.
    if args.mode and state_valid:
        state.update(version=3)
        if working_files(root) != initial_files: raise ValueError('file inventory changed during validation; retry')
        transact(root, local, {state_path: dump_json(state)}, snapshot)
        snapshot[state_path] = contents(state_path)
        initial_files = working_files(root)
    applicable = {}
    if changing:
        for key in scoped if target else features:
            path = features[key]['folder'] / PINS_FILE
            selected = args.write or args.acknowledge or args.repin == '*' or repin_key == key
            if selected and not global_errors and not ferrors[key] and (not args.strict or not fwarnings[key]):
                record = records[key]
                record['version'] = 3
                if dump_json(record) != (path.read_text() if path.exists() else ''): applicable[path] = dump_json(record)
        if not errors:
            applicable.update(writes)
            if not state.get('adopted') and args.write:
                head = git(root, 'rev-parse', 'HEAD')
                state.update(version=3, adopted=True, accepted_base=args.base or (head[0] if head else ''))
                applicable[state_path] = dump_json(state)
        if args.dry_run:
            notes.extend(f'would write {p.relative_to(root)}' for p in applicable)
        else:
            if working_files(root) != initial_files: raise ValueError('file inventory changed during validation; retry')
            transact(root, local, applicable, snapshot)
            notes.extend(f'wrote {p.relative_to(root)}' for p in applicable)
    if args.context:
        for ident, value in status['capabilities'].items():
            entry = base.entries[ident]
            entry['record'].update(delivery=value['delivery'], **{'owning spec': value['owner']})
            entry['raw'] = '| ' + ' | '.join(entry['record'][h].replace('|', '\\|') for h in entry['header']) + ' |'
        for part in base.parts:
            part['record']['state'] = status['parts'][part['name']]
            part['raw'] = '| ' + ' | '.join(part['record'][h].replace('|', '\\|') for h in part['header']) + ' |'
        context_code = print_context(base, names_of(args.ids), names_of(args.paths))
        for m in errors: print('error: ' + m)
        return int(bool(context_code or errors))
    if recorded_result is not None:
        for check in recorded_result['checks']:
            notes.append(f"executed {check['exact command']}: exit {check['exit']}")
        if any(c['exit'] != 0 for c in recorded_result['checks']):
            errors.append('recorded quality gate failed; logs saved, completion not accepted')
    if args.status and not args.json:
        for ident, value in status['capabilities'].items(): print(f"{ident}: {value['delivery']} ({value['owner'] or 'no owner'})")
        for name, value in status['parts'].items(): print(f'{name}: {value}')
    if args.json:
        print(json.dumps({**status, 'errors': errors, 'warnings': warnings, 'notes': notes}, indent=2))
    else:
        for m in notes: print('note: ' + m)
        for m in warnings: print('warning: ' + m)
        for m in errors: print('error: ' + m)
        print(f"baseline check {'failed' if errors else 'passed'}: {len(errors)} error(s), {len(warnings)} warning(s)" + ('; nothing was written' if changing and errors and not applicable else ''))
    failed_run = recorded_result is not None and any(c['exit'] != 0 for c in recorded_result['checks'])
    return int(failed_run) if advisory else int(bool(errors) or failed_run)


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate baseline intent and current evidence')
    for flag in ('write', 'strict', 'run-rule-checks', 'context', 'scan', 'gate', 'require-done', 'status', 'json', 'record-run', 'acknowledge', 'dry-run', 'structural'):
        parser.add_argument('--' + flag, action='store_true')
    for flag in ('repin', 'stamp'): parser.add_argument('--' + flag, nargs='?', const='*')
    for flag in ('feature', 'base', 'touched'): parser.add_argument('--' + flag)
    parser.add_argument('--reason', default='')
    parser.add_argument('--inactive-days', type=int, default=30)
    parser.add_argument('--ids', default=''); parser.add_argument('--paths', default='')
    parser.add_argument('--mode', choices=('advisory', 'blocking'))
    parser.add_argument('--commit-msg', type=Path); parser.add_argument('--root', type=Path)
    args = parser.parse_args()
    if args.gate and (args.write or args.repin is not None or args.stamp is not None or args.mode or args.record_run or args.acknowledge or args.structural or args.scan or args.touched or args.context or args.commit_msg):
        print('error: --gate is a read-only mandatory check; discovery, recovery and mutation options are incompatible')
        return 1
    if args.dry_run and args.mode:
        print('error: --dry-run cannot change persisted mode'); return 1
    root = args.root or find_root(Path.cwd())
    if args.commit_msg: return check_commit_message(root or Path.cwd(), args.commit_msg)
    if root is None or not (root / '.specify').is_dir():
        print('error: no .specify folder found'); return 1
    root = root.resolve()
    if args.scan: return print_scan(root)
    if args.record_run and not args.feature:
        print('error: --record-run requires explicit --feature'); return 1
    try:
        with locked(root) as local:
            if (local / 'journal.json').exists() and args.gate:
                print('error: interrupted transaction; run a non-gate check to recover'); return 1
            recover(root, local)
            return check_project(args, root, local)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f'error: baseline operation failed: {exc}'); return 1


if __name__ == '__main__':
    sys.exit(main())
