#!/bin/sh
# Install the extension and preset into an initialized Spec Kit project.
# Usage: install.sh [--force] [--agents claude,codex,gemini,cursor,antigravity] [PROJECT_DIR]
set -eu
here=$(cd "$(dirname "$0")" && pwd)
target=.
force=0
agents=
while [ $# -gt 0 ]; do
    case "$1" in
        --force) force=1 ;;
        --agents)
            [ $# -ge 2 ] && [ -n "$2" ] || { echo '--agents requires a comma-separated list' >&2; exit 2; }
            agents=$2; shift ;;
        -h|--help) sed -n '2,3p' "$0" | sed 's/^# //'; exit 0 ;;
        -*) echo "unknown option: $1" >&2; exit 2 ;;
        *) target=$1 ;;
    esac
    shift
done
case ",$agents," in
    *,,*) [ -z "$agents" ] || { echo 'Empty agent in --agents list' >&2; exit 2; } ;;
esac
for agent in $(printf '%s' "$agents" | tr ',' ' '); do
    case "$agent" in
        claude|codex|gemini|cursor|antigravity) ;;
        *) echo "Unsupported agent: $agent. Supported: claude,codex,gemini,cursor,antigravity" >&2; exit 2 ;;
    esac
done
version=$(cat "$here/SPECKIT_VERSION")
command -v specify >/dev/null 2>&1 || {
    echo "Install the Spec Kit CLI first:" >&2
    echo "uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v$version" >&2
    exit 1
}
[ -d "$target/.specify" ] || { echo "Run specify init in the target project first." >&2; exit 1; }
cd "$target"
python3 - <<'INTEGRATION'
import json
import subprocess
import sys

def run(*args):
    subprocess.run(['specify', 'integration', *args], check=True)

try:
    state = json.loads(subprocess.check_output(
        ['specify', 'integration', 'status', '--json'], text=True))
    installed = state['installed_integrations']
    default = state['default_integration']
    if default != 'codex' or installed != ['codex']:
        print(f"Current default integration: {default or 'none'}; installed: {', '.join(installed) or 'none'}.", flush=True)
        print('speckit-pro will make codex the sole Spec Kit integration, rendering shared skills in .agents/skills/.', flush=True)
        print('Other integrations will be uninstalled through Spec Kit, preserving modified files. Use --agents claude for Claude skill links.', flush=True)
        if 'codex' in installed:
            run('use', 'codex')
        else:
            run('switch', 'codex')
        state = json.loads(subprocess.check_output(
            ['specify', 'integration', 'status', '--json'], text=True))
        for key in state['installed_integrations']:
            if key != 'codex':
                run('uninstall', key)
    state = json.loads(subprocess.check_output(
        ['specify', 'integration', 'status', '--json'], text=True))
    if state['default_integration'] != 'codex' or state['installed_integrations'] != ['codex']:
        sys.exit('Could not establish codex as the sole integration; inspect specify integration status.')
except (subprocess.CalledProcessError, ValueError, KeyError) as exc:
    sys.exit(f'Integration setup failed: {exc}')
INTEGRATION
git_installed=$(python3 - <<'INSTALLED'
import json
import subprocess
items = json.loads(subprocess.check_output(['specify', 'extension', 'list', '--json'], text=True))
print('yes' if any(item['id'] == 'git' for item in items) else 'no')
INSTALLED
)
if [ "$git_installed" = no ]; then
    specify extension add git
fi
python3 - <<'CONFIG'
from pathlib import Path
import re
path = Path('.specify/extensions/git/git-config.yml')
text = path.read_text()
for key, value in [('branch_template', '"feature/{number}-{slug}"'),
                   ('branch_prefix', '""'), ('commit_style', 'conventional')]:
    line = f'{key}: {value}'
    pattern = rf'^{key}:.*$'
    text = re.sub(pattern, lambda _: line, text, flags=re.M) if re.search(pattern, text, re.M) else text + '\n' + line + '\n'
path.write_text(text)
CONFIG
baseline_installed=$(python3 - <<'INSTALLED'
import json
import subprocess
items = json.loads(subprocess.check_output(['specify', 'extension', 'list', '--json'], text=True))
print('yes' if any(item['id'] == 'baseline' for item in items) else 'no')
INSTALLED
)
if [ "$force" -eq 1 ]; then
    specify extension add --dev "$here/extension" --force
elif [ "$baseline_installed" = no ]; then
    specify extension add --dev "$here/extension"
fi
preset_installed=$(python3 - <<'INSTALLED'
import json
import subprocess
items = json.loads(subprocess.check_output(['specify', 'preset', 'list', '--json'], text=True))
print('yes' if any(item['id'] == 'universal-profile' for item in items) else 'no')
INSTALLED
)
if [ "$preset_installed" = no ]; then
    specify preset add --dev "$here/preset"
elif [ "$force" -eq 1 ]; then
    specify preset update universal-profile --dev "$here/preset"
fi
python3 - "$agents" <<'LINKS'
from pathlib import Path
import sys

skills = sorted(Path('.agents/skills').glob('speckit-*'))
if not skills or any(not (p / 'SKILL.md').is_file() for p in skills):
    sys.exit('Shared skills missing; inspect specify integration status and the extension/preset installation.')
if 'claude' in sys.argv[1].split(','):
    folder, target = Path('.claude/skills'), Path('../.agents/skills')
    # One folder link shows every shared skill to Claude Code. Never replace user skills.
    if folder.is_dir() and not folder.is_symlink():
        entries = list(folder.iterdir())
        if any(not p.is_symlink() or p.readlink() != Path('../../.agents/skills') / p.name
               for p in entries):
            sys.exit(f'{folder} holds other skills. Move them into .agents/skills, remove {folder} '
                     'and rerun; nothing was overwritten.')
        # Replace the per-skill links of earlier versions.
        for p in entries:
            p.unlink()
        folder.rmdir()
    if folder.is_symlink():
        if folder.readlink() != target:
            sys.exit(f'Conflicting link: {folder}. Move it aside and rerun; nothing was overwritten.')
    elif folder.exists():
        sys.exit(f'Conflicting file: {folder}. Move it aside and rerun; nothing was overwritten.')
    else:
        folder.parent.mkdir(exist_ok=True)
        folder.symlink_to(target, target_is_directory=True)
LINKS
echo "speckit-pro installed. Start with the speckit-baseline-context command, or speckit-baseline-recover for existing code."
