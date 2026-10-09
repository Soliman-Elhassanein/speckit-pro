#!/usr/bin/env python3
"""Deterministic check of the project baseline.

Checks .specify/memory/{product,architecture,decisions}.md against specs/ and
recalculates each capability's Delivery from its owning spec's verification.md.

Usage: baseline_check.py [--write] [--root DIR]
Exit 0 when clean, 1 when any error is reported.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"\b(?:CAP|PR|AR|D)-\d{3,}\b")
DEFINED_RE = re.compile(r"^(?:CAP|PR|AR|D)-\d{3,}$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
COMPLETION_RE = re.compile(r"^Completion:\s*(NOT DONE|DONE)\b", re.MULTILINE)
DECISION_STATES = {"proposed", "approved", "superseded", "retired"}
BASELINE_FILES = ("product.md", "architecture.md", "decisions.md")


def find_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / ".specify").is_dir():
            return candidate
    return None


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="rewrite stale Delivery cells in product.md")
    parser.add_argument("--root", type=Path, default=None, help="repository root (default: nearest folder with .specify)")
    args = parser.parse_args()

    root = args.root or find_root(Path.cwd())
    if root is None or not (root / ".specify").is_dir():
        print("error: no .specify folder found; run from inside a Spec Kit project", file=sys.stderr)
        return 1

    memory = root / ".specify" / "memory"
    product_path = memory / "product.md"
    if not product_path.is_file():
        print(f"error: {product_path.relative_to(root)} is missing; run the baseline amend command", file=sys.stderr)
        return 1

    errors: list[str] = []
    defined: dict[str, str] = {}  # ID -> file that defines it
    decision_status: dict[str, str] = {}
    capabilities: dict[str, dict] = {}

    for name in BASELINE_FILES:
        path = memory / name
        if not path.is_file():
            if name != "product.md":
                errors.append(f"{name}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for index, header, row in table_rows(text):
            if not row or not DEFINED_RE.match(row[0]):
                continue
            ident = row[0]
            if ident in defined:
                errors.append(f"{name}:{index + 1}: {ident} is defined twice (also in {defined[ident]})")
                continue
            defined[ident] = name
            record = dict(zip(header, row))
            if ident.startswith("D-"):
                decision_status[ident] = record.get("status", "")
            if ident.startswith("CAP-") and name == "product.md":
                capabilities[ident] = {"line": index, "header": header, "row": row, "record": record}
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if "://" in target or target.startswith(("#", "mailto:")):
                continue
            if not (path.parent / target.split("#")[0]).exists():
                errors.append(f"{name}: link does not resolve: {target}")

    # What each spec says it implements, and what specs and plans cite.
    implements: dict[str, set[str]] = {}
    specs_root = root / "specs"
    spec_dirs = sorted(p for p in specs_root.iterdir() if (p / "spec.md").is_file()) if specs_root.is_dir() else []
    for spec_dir in spec_dirs:
        spec_text = (spec_dir / "spec.md").read_text(encoding="utf-8")
        line = re.search(r"^\*\*Implements\*\*:(.*)$", spec_text, re.MULTILINE)
        named = set(re.findall(r"\bCAP-\d{3,}\b", line.group(1))) if line else set()
        implements[spec_dir.name] = named
        where = f"specs/{spec_dir.name}/spec.md"
        if not named:
            errors.append(f"{where}: no `**Implements**: CAP-NNN` line naming a capability")
        for ident in sorted(named):
            capability = capabilities.get(ident)
            if capability and capability["record"].get("decision", "").lower() != "approved":
                errors.append(f"{where}: implements {ident}, which is not approved")
        for doc in ("spec.md", "plan.md"):
            doc_path = spec_dir / doc
            if not doc_path.is_file():
                continue
            for ident in sorted(set(ID_RE.findall(doc_path.read_text(encoding="utf-8")))):
                if ident not in defined:
                    errors.append(f"specs/{spec_dir.name}/{doc}: cites {ident}, which is not defined in the baseline")
                elif ident.startswith("D-") and decision_status.get(ident, "").lower() != "accepted":
                    errors.append(
                        f"specs/{spec_dir.name}/{doc}: cites {ident}, whose status is "
                        f"'{decision_status.get(ident) or 'empty'}'"
                    )

    # Capabilities: state, owning spec, and Delivery calculated from evidence.
    product_lines = product_path.read_text(encoding="utf-8").splitlines()
    changed = False
    for ident, capability in sorted(capabilities.items()):
        record, header, row = capability["record"], capability["header"], capability["row"]
        where = f"product.md:{capability['line'] + 1}"
        state = record.get("decision", "").lower()
        if state not in DECISION_STATES:
            errors.append(f"{where}: {ident} has decision '{state}'; use one of {sorted(DECISION_STATES)}")
        owner = spec_dir_of(record.get("owning spec", ""))
        delivery = "unstarted"
        if owner:
            if owner not in implements:
                errors.append(f"{where}: {ident} names owning spec '{owner}', but specs/{owner}/spec.md does not exist")
            else:
                if ident not in implements[owner]:
                    errors.append(f"{where}: {ident} is owned by specs/{owner}, whose spec.md does not list it under Implements")
                verification = specs_root / owner / "verification.md"
                completion = COMPLETION_RE.search(verification.read_text(encoding="utf-8")) if verification.is_file() else None
                delivery = "verified" if completion and completion.group(1) == "DONE" else "in progress"
        if "delivery" not in header:
            errors.append(f"{where}: the capabilities table has no Delivery column")
            continue
        column = header.index("delivery")
        current = row[column].lower() if column < len(row) else ""
        if current == delivery:
            continue
        if args.write:
            parts = product_lines[capability["line"]].split("|")
            parts[column + 1] = f" {delivery} "
            product_lines[capability["line"]] = "|".join(parts)
            changed = True
            print(f"updated {ident}: Delivery '{current}' -> '{delivery}'")
        else:
            errors.append(f"{where}: {ident} shows Delivery '{current}', evidence says '{delivery}'; run with --write")

    # Every implemented capability must point back at its spec: one owning spec per promise.
    for spec_name, named in sorted(implements.items()):
        for ident in sorted(named):
            capability = capabilities.get(ident)
            if capability is None:
                continue  # already reported as undefined
            owner = spec_dir_of(capability["record"].get("owning spec", ""))
            if owner != spec_name:
                errors.append(
                    f"specs/{spec_name}/spec.md: implements {ident}, but product.md names "
                    f"'{owner or '-'}' as its owning spec"
                )

    if changed:
        product_path.write_text("\n".join(product_lines) + "\n", encoding="utf-8")

    for message in errors:
        print(f"error: {message}")
    if errors:
        print(f"baseline check failed: {len(errors)} error(s)")
        return 1
    print(f"baseline check passed: {len(capabilities)} capabilities, {len(spec_dirs)} specs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
