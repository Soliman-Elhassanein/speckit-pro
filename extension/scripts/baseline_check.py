#!/usr/bin/env python3
"""Read-only structure checks for project memory and feature records; Python 3.11+."""
import argparse
import ipaddress
from pathlib import Path
import re

ID = re.compile(r'(CAP|PR|AR|D|Q)-\d{3,}')
CITE = re.compile(r'^\*\*(Implements|Product rules|Architecture rules|Decisions|Promises|Override)\*\*:\s*([^\n]*)$', re.M)
AREAS = ('git & branching', 'PRs & review', 'environments', 'CI/CD', 'code quality',
         'testing', 'documentation', 'issues & tasks', 'release & versioning', 'security',
         'database changes', 'observability', 'dependencies', 'repository governance')
FILES = {'product.md': ('CAP', 'PR', 'Q'), 'architecture.md': ('AR',), 'decisions.md': ('D',)}
KINDS = dict(zip(('Implements', 'Product rules', 'Architecture rules', 'Decisions', 'Promises', 'Override'),
                 ('CAP', 'PR', 'AR', 'D', 'PR', 'D')))


# One table of privacy shapes; diagnostics never echo the sensitive match.
PRIVATE = (
    ('absolute path', r'(?<![\w/.:])(?:/(?!/)[\w.-]+(?:/[^\s`|<>]+)*|[A-Za-z]:[\\/][^\s`|<>]+|~/[^\s`|<>]+)'),
    ('IP address', r'(?<![\w:])(?:\d{1,3}\.){3}\d{1,3}(?!\w|\.\d)|(?<![\w:])(?:[0-9a-f]{0,4}:){2,}[0-9a-f:.]*(?:%[\w.-]+)?(?![\w:])'),
    ('email', r'[\w.+-]+@[\w.-]+\.[a-z]{2,}'),
    ('URL credentials', r'[a-z][a-z0-9+.-]*://[^\s/@]+(?::[^\s/@]*)?@'),
    ('private key', r'-----BEGIN (?:[A-Z0-9]+ )*PRIVATE KEY-----'),
    ('AWS key', r'\bAKIA[A-Z0-9]{16}\b'),
    ('GitHub token', r'\b(?:ghp_[a-z0-9]{20,}|github_pat_[a-z0-9_]{20,})'),
    ('API key', r'\bsk-[a-z0-9_-]{20,}'),
    ('Slack token', r'\bxox[a-z]-[a-z0-9-]{10,}'),
    ('JWT', r'\beyJ[a-z0-9_-]+\.[a-z0-9_-]+\.[a-z0-9_-]+'),
    ('secret assignment', r"\b(?:password|secret|token)\s*=\s*[\"']?[^\s\"'`|<>]+"),
)


def privacy_check(memory):
    errors = []
    for name in (*FILES, 'constitution.md'):
        path = memory / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            for label, pattern in PRIVATE:
                for match in re.finditer(pattern, line, re.I):
                    if label == 'IP address':
                        try:
                            ipaddress.ip_address(match[0].rstrip('.'))
                        except ValueError:
                            continue
                    errors.append(f'privacy: {name}:{number}: {label}; rewrite generically or drop')
                    break
    return errors


def section(text, heading):
    match = re.search(r'^## ' + re.escape(heading) + r'[ \t]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    return match[1] if match else ''


def tables(text):
    """Read pipe tables without losing escaped pipes or silently truncating cells."""
    header, fenced = None, False
    for number, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if line.startswith(('```', '~~~')):
            fenced = not fenced
        if fenced or not line.startswith('|'):
            header = None
            continue
        row = re.split(r'(?<!\\)\|', line[1:])
        if line.endswith('|'):
            row.pop()
        row = [cell.strip().replace(r'\|', '|') for cell in row]
        if row and all(re.fullmatch(r':?-+:?', cell) for cell in row):
            continue
        if header is None:
            header = [cell.lower() for cell in row]
        else:
            yield number, header, row


def references(value, kind, entries, where):
    errors = []
    for token in re.split(r'[,\s]+', value.strip()):
        if token.lower() in ('', '-', 'none'):
            continue
        if not ID.fullmatch(token) or not token.startswith(kind + '-'):
            errors.append(f'{where}: invalid citation {token}')
        elif token not in entries:
            errors.append(f'{where}: undefined citation {token}')
        elif kind == 'D' and entries[token].get('status') != 'accepted':
            errors.append(f'{where}: cited decision {token} is not accepted')
    return errors


def memory_check(root):
    entries, texts = {}, {}
    memory = root / '.specify/memory'
    errors = privacy_check(memory)
    if errors:
        return entries, errors
    for name, kinds in FILES.items():
        path = memory / name
        if not path.is_file():
            errors.append(f'{name}: file is missing')
            continue
        texts[name] = path.read_text(encoding='utf-8')
        for number, header, row in tables(texts[name]):
            where = f'{name}:{number}'
            if not header or len(header) != len(row):
                errors.append(f'{where}: malformed table row; escape pipes as \\|')
                continue
            if header[0] != 'id':
                continue
            ident = row[0]
            match = ID.fullmatch(ident)
            if not match or match[1] not in kinds:
                errors.append(f'{where}: invalid ID {ident}')
            elif ident in entries:
                errors.append(f'{where}: {ident} is defined twice')
            else:
                entries[ident] = dict(zip(header, row))
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', texts[name]):
            if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                continue
            if not (memory / target.split('#')[0]).exists():
                errors.append(f'{name}: link does not resolve: {target}')
    spirit = section(texts.get('product.md', ''), 'Spirit')
    if not spirit.strip():
        errors.append('product.md: Spirit section is required')
    non_goals = re.search(r'^### Non-goals[ \t]*\n(.*?)(?=^#{1,6} |\Z)', spirit, re.M | re.S)
    if not non_goals or not re.sub(r'^\|.*$', '', non_goals[1], flags=re.M).strip():
        errors.append('product.md: Spirit requires non-goals')
    delivery = section(texts.get('architecture.md', ''), 'Delivery standards')
    seen = []
    for number, header, row in tables(delivery):
        if header != ['area', 'status', 'rule', 'check', 'blocking'] or len(row) != 5:
            errors.append(f'Delivery standards:{number}: malformed table row')
            continue
        area, status, rule, check, blocking = row
        seen.append(area)
        if status not in ('decided', 'undecided') and not re.fullmatch(r'n/a: \S.*', status):
            errors.append(f'Delivery standards: {area}: invalid status {status!r}')
        if blocking not in ('yes', 'no'):
            errors.append(f'Delivery standards: {area}: Blocking must be yes or no')
    if sorted(seen) != sorted(AREAS):
        errors.append('Delivery standards: exactly the 14 required areas must appear once')
    for ident, row in entries.items():
        fields = {'depends on': 'CAP', 'serves': 'PR'} if ident.startswith('CAP-') else {}
        for key, kind in fields.items():
            if key == 'serves' and row.get(key, '').lower() in ('', '-', 'none'):
                errors.append(f'{ident}: Serves requires a PR citation')
            errors.extend(references(row.get(key, ''), kind, entries, ident))
        if ident.startswith('Q-'):
            if row.get('blocks', '').lower() != 'nothing yet':
                errors.extend(references(row.get('blocks', ''), 'CAP', entries, ident))
            status = row.get('status', '')
            if status != 'open':
                if not status.startswith('answered by D-'):
                    errors.append(f'{ident}: invalid question status {status!r}')
                else:
                    errors.extend(references(status.removeprefix('answered by '), 'D', entries, ident))
        if ident.startswith('D-'):
            status = row.get('status', '')
            if status not in ('accepted', 'rejected'):
                match = re.fullmatch(r'superseded by (D-\d{3,})', status)
                if not match or match[1] not in entries or match[1] == ident:
                    errors.append(f'{ident}: invalid decision status {status!r}')
    for _, header, row in tables(texts.get('architecture.md', '')):
        if len(header) == len(row) and 'decision' in header:
            errors.extend(references(row[header.index('decision')], 'D', entries, 'architecture.md'))
    # Only typed reference cells govern; decision and rejected-option prose is context.
    for name, text in texts.items():
        for label, value in CITE.findall(text):
            errors.extend(references(value, KINDS[label], entries, name))
    return entries, errors


def features(root):
    found = []
    for path in sorted((root / 'specs').rglob('spec.md'), key=lambda p: (len(p.parts), str(p))):
        if not any(parent in path.parents for parent in found):
            found.append(path.parent)
    return found


def feature_check(folder, entries):
    errors = []
    for name in ('spec.md', 'plan.md'):
        path = folder / name
        if not path.is_file():
            continue
        text = path.read_text(encoding='utf-8')
        for label, value in CITE.findall(text):
            errors.extend(references(value, KINDS[label], entries, str(path)))
        if name == 'spec.md':
            focus = section(text, 'Focus')
            citations = [(label, value) for label, value in CITE.findall(focus)
                         if label in ('Promises', 'Override')]
            if not focus.strip():
                errors.append(f'{path}: Focus section is required')
            if not any(ID.fullmatch(token) and token.startswith(KINDS[label] + '-')
                       and token in entries for label, value in citations
                       for token in re.split(r'[,\s]+', value)):
                errors.append(f'{path}: Focus requires a real PR promise or recorded override')
    return errors


def done_check(root, folder):
    errors, texts = [], {}
    for name in ('spec.md', 'plan.md', 'tasks.md', 'verification.md'):
        path = folder / name
        if not path.is_file() or not path.read_text(encoding='utf-8').strip():
            errors.append(f'{folder}: {name} is missing or empty')
        else:
            texts[name] = path.read_text(encoding='utf-8')
    if errors:
        return errors
    boxes = re.findall(r'^\s*[-*] \[([ xX])\] T\d+\b', texts['tasks.md'], re.M)
    if not boxes or ' ' in boxes:
        errors.append('tasks.md: tasks must exist and all be checked')
    record = texts['verification.md']
    if not re.search(r'^Completion: DONE\s*$', record, re.M):
        errors.append('verification.md: Completion must be DONE')
    if not re.search(r'^Outcome: `?converged`?\s*$', section(record, 'Convergence'), re.M):
        errors.append('verification.md: outcome must be converged')
    if section(record, 'Remaining gaps').strip().lower() != 'none':
        errors.append('verification.md: remaining gaps must be None')
    planned, executed = {}, {}
    for text, heading, expected, output in (
        (texts['plan.md'], 'Quality gates', ['gate', 'command'], planned),
        (record, 'Execution', ['gate', 'command', 'exit code', 'log path'], executed),
    ):
        rows = list(tables(section(text, heading)))
        if not rows:
            errors.append(f'{heading}: gate rows are required')
        for number, header, row in rows:
            if header != expected or len(row) != len(expected):
                errors.append(f'{heading}:{number}: invalid table columns')
                continue
            if not all(row) or any(re.fullmatch(r'`?(?:<[^>]+>|\[[^]]+\]|-)`?', cell) for cell in row):
                errors.append(f'{heading}:{number}: gate fields must be filled')
                continue
            gate, command = row[:2]
            if gate in output or not re.fullmatch(r'`[^`]+`', command):
                errors.append(f'{heading}: duplicate gate or invalid command {gate}')
            output[gate] = command
            if heading == 'Execution':
                if row[2] != '0':
                    errors.append(f'{gate}: exit code must be 0')
                log = row[3].strip('`')
                if not (root / log).is_file():
                    errors.append(f'{gate}: log path does not resolve: {log}')
    if planned != executed:
        errors.append('Execution: gates and commands must match plan.md')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path)
    parser.add_argument('--feature', type=Path)
    parser.add_argument('--done', action='store_true')
    parser.add_argument('--mode', choices=('advisory', 'blocking'), default='blocking')
    args = parser.parse_args()
    root = args.root or next((p for p in (Path.cwd(), *Path.cwd().parents)
                              if (p / '.specify').is_dir()), Path.cwd())
    root = root.resolve()
    try:
        entries, errors = memory_check(root)
        if args.feature:
            folder = (root / args.feature).resolve()
            if not (folder / 'spec.md').is_file():
                errors.append(f'{folder}: spec.md is missing')
            selected = [folder]
        else:
            selected = features(root)
        for folder in selected:
            errors.extend(feature_check(folder, entries))
            if args.done:
                errors.extend(done_check(root, folder))
        if args.done and not selected:
            errors.append('DONE requires a feature')
    except (OSError, UnicodeError) as exc:
        errors = [str(exc)]
    for error in errors:
        print('error: ' + error)
    print(f'memory check: {len(errors)} error(s)' + (' (advisory)' if args.mode == 'advisory' else ''))
    return int(any(e.startswith('privacy:') for e in errors) or
               bool(errors) and (args.done or args.mode == 'blocking'))


if __name__ == '__main__':
    raise SystemExit(main())
