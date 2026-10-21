#!/bin/sh
# Real installation and upstream upgrade check; requires network and uv.
set -eu
[ "$#" -eq 1 ] || { echo "Usage: $0 <spec-kit-version>" >&2; exit 2; }
here=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
version=${1#v}
case "$version" in
    ''|*[!0-9A-Za-z.+-]*) echo 'FAIL invalid version' >&2; exit 2 ;;
esac
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT HUP INT TERM
# Isolate the selected CLI version without replacing the user's installed CLI.
mkdir "$scratch/bin"
cat > "$scratch/bin/specify" <<EOF_CLI
#!/bin/sh
exec uvx --from 'git+https://github.com/github/spec-kit.git@v$version' specify "\$@"
EOF_CLI
chmod +x "$scratch/bin/specify"
export PATH="$scratch/bin:$PATH"
if ! specify init --help > "$scratch/init-help"; then
    echo 'FAIL init help'; exit 1
fi
# Accept upstream's integration option name for the selected release.
if grep -q -- '--integration' "$scratch/init-help"; then
    set -- --integration claude
else
    set -- --ai claude
fi
if grep -q -- '--ignore-agent-tools' "$scratch/init-help"; then
    set -- "$@" --ignore-agent-tools
fi
# 1.2+ has no --no-git (Git is an extension) and may prompt unless told not to.
if grep -q -- '--non-interactive' "$scratch/init-help"; then
    set -- "$@" --non-interactive
fi
if grep -q -- '--no-git' "$scratch/init-help"; then
    set -- "$@" --no-git
fi
if specify init "$scratch/project" "$@"; then
    echo "PASS init $version"
else
    echo "FAIL init $version"; exit 1
fi
if "$here/install.sh" --agents claude "$scratch/project"; then
    echo 'PASS install'
    "$here/install.sh" --agents claude "$scratch/project"
    echo 'PASS repeated install'
else
    echo 'FAIL install'; exit 1
fi
python3 - "$here" "$scratch/project" <<'PY'
from pathlib import Path
import json
import os
import subprocess
import sys
source, project = map(Path, sys.argv[1:])
failures = []
def check(label, passed):
    print(('PASS ' if passed else 'FAIL ') + label)
    if not passed:
        failures.append(label)
# Only the installed shared skills prove composition; downloaded sources do not.
shared = project / '.agents/skills'
claude = project / '.claude/skills'
state = subprocess.run(['specify', 'integration', 'status', '--json'], cwd=project,
                       capture_output=True, text=True)
try:
    state_data = json.loads(state.stdout)
except ValueError:
    state_data = {}
check('single default integration', state.returncode == 0 and
      state_data.get('default_integration') == 'codex' and
      state_data.get('installed_integrations') == ['codex'])
linked = (claude.is_symlink() and claude.readlink() == Path('../.agents/skills')
          and claude.resolve() == shared.resolve())
check('Claude skills folder link', linked)
rendered = {}
for skill in sorted(shared.glob('speckit-*')):
    path = skill / 'SKILL.md'
    link = claude / skill.name
    check('shared directory ' + skill.name, skill.is_dir() and not skill.is_symlink())
    if path.is_file():
        rendered[skill.name] = [path.read_text()]
        check('Claude content ' + skill.name, linked and (link / 'SKILL.md').is_file()
              and (link / 'SKILL.md').read_text() == path.read_text())
def command_texts(name):
    return rendered.get(name.replace('.', '-'), [])
for name in ('analyze', 'checklist', 'clarify', 'constitution', 'converge',
             'implement', 'plan', 'specify', 'tasks', 'taskstoissues'):
    texts = command_texts('speckit.' + name)
    check('core skill ' + name, bool(texts))
    header = texts[0].split('---', 2)[1] if texts and texts[0].startswith('---') else ''
    check('standard skill metadata ' + name, all('\n' + key + ':' in '\n' + header
          for key in ('name', 'description', 'compatibility', 'metadata')))
for path in sorted((source / 'extension/commands').glob('*.md')):
    body = path.read_text().split('---', 2)[2].strip()
    check('baseline command ' + path.stem, any(body in text for text in command_texts(path.stem)))
for name in ('feature', 'validate', 'commit', 'initialize', 'remote'):
    check('git command ' + name, bool(command_texts('speckit.git.' + name)))
for name, rule in (('speckit.plan', 'Quality gates'), ('speckit.converge', 'Write-back is automatic')):
    check('shared rule ' + name, any(rule in text for text in command_texts(name)))
for path in sorted((source / 'preset/commands').glob('*.md')):
    body = path.read_text().split('---', 2)[2].split('{CORE_TEMPLATE}')[0].strip()
    matches = command_texts(path.stem)
    check('wrap ' + path.stem, any(body in text and '{CORE_TEMPLATE}' not in text
          and len(text) > len(body) + 100 for text in matches))
for path in sorted((source / 'preset/templates').glob('*.md')):
    resolver = project / '.specify/scripts/bash/resolve-template.sh'
    result = subprocess.run(['bash', str(resolver), path.stem], cwd=project,
                            capture_output=True, text=True)
    check('template ' + path.stem, result.returncode == 0
          and path.read_text().strip() in result.stdout
          and (path.stem == 'verification-template' or len(result.stdout) > len(path.read_text()) + 100))
for name in ('product.md', 'architecture.md', 'decisions.md'):
    candidates = [project / '.specify/memory' / name,
                  project / '.specify/extensions/baseline/templates' / name]
    check('memory template ' + name, any(p.is_file() and p.read_text() ==
          (source / 'extension/templates' / name).read_text() for p in candidates))
config = project / '.specify/extensions/git/git-config.yml'
settings = config.read_text() if config.is_file() else ''
for setting in ('branch_template: "feature/{number}-{slug}"', 'branch_prefix: ""',
                'commit_style: conventional'):
    check('Git setting ' + setting, setting in settings)
# Exercise upstream's configured branch generation without creating branches.
creator = project / '.specify/extensions/git/scripts/python/create_new_feature_branch.py'
if creator.is_file():
    result = subprocess.run([sys.executable, str(creator), '--json', '--dry-run',
                             '--short-name', 'install-check', 'Install check'],
                            cwd=project, capture_output=True, text=True,
                            env={k: v for k, v in os.environ.items() if k != 'GIT_BRANCH_NAME'})
    try:
        branch = json.loads(result.stdout).get('BRANCH_NAME', '')
    except ValueError:
        branch = ''
    check('upstream configured branch generation', result.returncode == 0
          and branch == 'feature/001-install-check')
else:
    check('upstream configured branch generation', False)
check('type/ticket override command', any('APP-142' in text and 'git branch -m' in text
      and 'hotfix' in text for text in command_texts('speckit.baseline.branch')))
# Upstream owns hook registration. Require the hook command in registration,
# excluding component manifests and source prompts, which prove no activation.
registrations = [p for p in (project / '.specify').rglob('*') if p.is_file()
                 and not any(part in ('baseline', 'git') for part in p.relative_to(project / '.specify').parts)
                 and 'presets' not in p.relative_to(project / '.specify').parts
                 and p.suffix in ('.json', '.yml', '.yaml')]
check('branch hook registered', any('speckit.baseline.branch' in p.read_text()
      and 'after_specify' in p.read_text() for p in registrations))
script = project / '.specify/extensions/baseline/scripts/baseline_check.py'
if script.is_file():
    # Memory templates intentionally contain unapproved markers, so use advisory.
    result = subprocess.run([sys.executable, str(script), '--root', str(project),
                             '--mode', 'advisory'], capture_output=True, text=True)
    check('checker runs', result.returncode == 0 and 'memory check:' in result.stdout)
else:
    check('checker runs', False)
# Deterministic source rules can be checked here; actual naming and interpretation
# still need the first-feature walkthrough after installation.
check('commit convention composed', any('Subject at most 50 characters' in t and
      'Refs: APP-142' in t and '72 characters' in t for t in command_texts('speckit.implement')))
sys.exit(bool(failures))
PY
