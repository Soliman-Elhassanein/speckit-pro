#!/bin/sh
# speckit-pro installer: put the speckit-pro standard, preset, baseline extension
# and workflow into a project.
#
# Usage: install.sh [--agent NAME] [--force] [--with-cli] [PROJECT_DIR]
#
#   PROJECT_DIR    project root to install into (default: current folder)
#   --agent NAME   the coding agent the project uses, as Spec Kit names it
#                  (claude, copilot, cursor, gemini, codex, ...). Needs the
#                  Spec Kit CLI. Without it, a project that has no Spec Kit
#                  gets the ready-made setup for agents that read .agents/skills.
#   --force        update a project where speckit-pro is already installed
#   --with-cli     install the pinned Spec Kit CLI with uv first
#
# A project that already has Spec Kit keeps its agent, its hooks, its other
# extensions and its settings: there the installer goes through the Spec Kit
# CLI and never copies over .specify. Specs, code, constitution.md and the
# baseline files are never overwritten.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
force=0
with_cli=0
agent=
target=.

while [ $# -gt 0 ]; do
    case "$1" in
        --force) force=1 ;;
        --with-cli) with_cli=1 ;;
        --agent) [ $# -ge 2 ] || { echo "--agent needs a name" >&2; exit 2; }; agent=$2; shift ;;
        --agent=*) agent=${1#--agent=} ;;
        -h|--help) sed -n '2,19p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        -*) echo "unknown option: $1" >&2; exit 2 ;;
        *) target=$1 ;;
    esac
    shift
done

[ -d "$here/template/.specify" ] || { echo "template/ is missing next to install.sh; run scripts/build-template.sh" >&2; exit 1; }
[ -d "$target" ] || { echo "not a folder: $target" >&2; exit 1; }
target=$(cd "$target" && pwd)
[ "$target" != "$here" ] || { echo "refusing to install speckit-pro into its own folder" >&2; exit 1; }

version=$(cat "$here/template/SPECKIT_VERSION")

# What the installed commands need at run time.
for tool in git bash python3; do
    command -v "$tool" >/dev/null 2>&1 || { echo "speckit-pro needs $tool on PATH" >&2; exit 1; }
done
python3 -c 'import yaml' 2>/dev/null || echo "warning: the Python package PyYAML is missing; Spec Kit needs it to compose the templates (pip install pyyaml)" >&2

if [ "$with_cli" -eq 1 ]; then
    command -v uv >/dev/null 2>&1 || { echo "--with-cli needs uv: https://docs.astral.sh/uv/" >&2; exit 1; }
    uv tool install specify-cli --force --from "git+https://github.com/github/spec-kit.git@v$version"
fi

need_cli() {
    command -v specify >/dev/null 2>&1 || {
        echo "$1" >&2
        echo "install the Spec Kit CLI, or re-run with --with-cli:" >&2
        echo "  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v$version" >&2
        exit 1
    }
    have=$(specify --version 2>/dev/null | awk '{print $NF}')
    [ "$have" = "$version" ] || echo "warning: speckit-pro was built and tested with Spec Kit $version; this machine has ${have:-an unknown version}" >&2
}

installed=0
[ -d "$target/.specify/extensions/baseline" ] || [ -d "$target/.specify/presets/universal-profile" ] && installed=1
if [ "$installed" -eq 1 ] && [ "$force" -eq 0 ]; then
    echo "speckit-pro is already installed in $target" >&2
    echo "re-run with --force to update its commands, templates, check script and workflow" >&2
    exit 1
fi

if [ ! -e "$target/.specify" ] && { [ -z "$agent" ] || [ "$agent" = "codex" ]; } && ! command -v specify >/dev/null 2>&1; then
    # No Spec Kit here and no CLI: copy the ready-made installation.
    mode="ready-made setup for agents that read .agents/skills"
    mkdir -p "$target/.agents"
    cp -R "$here/template/.agents/." "$target/.agents/"
    cp -R "$here/template/.specify" "$target/.specify"
else
    # Go through the Spec Kit CLI, so the project keeps what it already has.
    need_cli "this project already has Spec Kit, or uses another agent, so the installer must go through the Spec Kit CLI"
    cd "$target"
    if [ ! -e .specify ]; then
        agent=${agent:-codex}
        if [ "$agent" = "codex" ]; then
            specify init --here --force --integration codex --integration-options="--skills" --script sh --ignore-agent-tools >/dev/null
        else
            specify init --here --force --integration "$agent" --script sh --ignore-agent-tools >/dev/null
        fi
        mode="new Spec Kit project for $agent"
    else
        [ -z "$agent" ] || echo "note: this project already has Spec Kit; keeping its agent and ignoring --agent $agent" >&2
        mode="added to the existing Spec Kit project"
    fi
    if [ -d .specify/presets/universal-profile ]; then
        specify preset remove universal-profile >/dev/null
    fi
    specify preset add --dev "$here/preset" >/dev/null
    if [ -d .specify/extensions/baseline ]; then
        specify extension add --dev "$here/extension" --force >/dev/null
    else
        specify extension add --dev "$here/extension" >/dev/null
    fi
    specify workflow add --dev "$here/workflow" >/dev/null
    # The workflow registry records where a local workflow came from; keep this machine's path out.
    sed "s|$here/workflow|speckit-pro|" .specify/workflows/workflow-registry.json > .specify/workflows/registry.tmp
    mv .specify/workflows/registry.tmp .specify/workflows/workflow-registry.json
fi

# The standard itself lives beside its modules, outside any agent's folder.
mkdir -p "$target/.specify/speckit-pro"
cp "$here/speckit-universal-profile.md" "$target/.specify/speckit-pro/speckit-universal-profile.md"
rm -rf "$target/.specify/speckit-pro/modules"
cp -R "$here/modules" "$target/.specify/speckit-pro/modules"
cp "$here/adoption-prompt.md" "$target/.specify/speckit-pro/adoption-prompt.md"
echo "$version" > "$target/.specify/speckit-pro/SPECKIT_VERSION"

cat <<EOF2
speckit-pro installed in $target
  Spec Kit $version: $mode
  standard:  .specify/speckit-pro/speckit-universal-profile.md
  modules:   .specify/speckit-pro/modules/

Next: open your coding agent in that folder and paste the block from
  .specify/speckit-pro/adoption-prompt.md
EOF2
