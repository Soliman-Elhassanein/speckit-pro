#!/bin/sh
# speckit-plus installer: put a complete, ready-to-use Spec Kit setup into a project.
#
# Usage: install.sh [--force] [--with-cli] [PROJECT_DIR]
#
#   PROJECT_DIR   project root to install into (default: current folder)
#   --force       overwrite an existing speckit-plus / Spec Kit installation there
#   --with-cli    also install the pinned Spec Kit CLI with uv (optional; the
#                 installed files work without it)
#
# Nothing outside PROJECT_DIR is changed unless --with-cli is given.
set -eu

here=$(cd "$(dirname "$0")" && pwd)
force=0
with_cli=0
target=.

for arg in "$@"; do
    case "$arg" in
        --force) force=1 ;;
        --with-cli) with_cli=1 ;;
        -h|--help) sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        -*) echo "unknown option: $arg" >&2; exit 2 ;;
        *) target=$arg ;;
    esac
done

[ -d "$here/template/.specify" ] || { echo "template/ is missing next to install.sh; run scripts/build-template.sh" >&2; exit 1; }
[ -d "$target" ] || { echo "not a folder: $target" >&2; exit 1; }
target=$(cd "$target" && pwd)
[ "$target" != "$here" ] || { echo "refusing to install speckit-plus into its own folder" >&2; exit 1; }

version=$(cat "$here/template/SPECKIT_VERSION")

if [ "$force" -eq 0 ] && { [ -e "$target/.specify" ] || [ -e "$target/.agents/skills/speckit-specify" ]; }; then
    echo "Spec Kit is already installed in $target" >&2
    echo "re-run with --force to overwrite its command, script and template files" >&2
    echo "(specs, code, constitution.md and the baseline files are never overwritten)" >&2
    exit 1
fi

# Files the project owns once they exist: never replace them, even with --force.
keep_constitution=0
[ -f "$target/.specify/memory/constitution.md" ] && keep_constitution=1
[ "$keep_constitution" -eq 1 ] && cp "$target/.specify/memory/constitution.md" "$target/.specify/memory/constitution.md.keep"

mkdir -p "$target/.agents" "$target/.specify/speckit-plus"
cp -R "$here/template/.agents/." "$target/.agents/"
cp -R "$here/template/.specify/." "$target/.specify/"

[ "$keep_constitution" -eq 1 ] && mv "$target/.specify/memory/constitution.md.keep" "$target/.specify/memory/constitution.md"

cp "$here/speckit-universal-profile.md" "$target/.agents/skills/speckit-standard.md"
rm -rf "$target/.specify/speckit-plus/modules"
cp -R "$here/modules" "$target/.specify/speckit-plus/modules"
cp "$here/adoption-prompt.md" "$target/.specify/speckit-plus/adoption-prompt.md"
echo "$version" > "$target/.specify/speckit-plus/SPECKIT_VERSION"

if [ "$with_cli" -eq 1 ]; then
    command -v uv >/dev/null 2>&1 || { echo "--with-cli needs uv: https://docs.astral.sh/uv/" >&2; exit 1; }
    uv tool install specify-cli --force --from "git+https://github.com/github/spec-kit.git@v$version"
fi

skills=$(find "$target/.agents/skills" -name SKILL.md | wc -l | tr -d ' ')
cat <<EOF
speckit-plus installed in $target
  Spec Kit $version, $skills skills in .agents/skills
  standard:  .agents/skills/speckit-standard.md
  modules:   .specify/speckit-plus/modules/

Next: open your coding agent in that folder and paste the block from
  .specify/speckit-plus/adoption-prompt.md
EOF
