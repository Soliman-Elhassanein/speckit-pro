#!/bin/sh
# Rebuild template/ : a complete, ready-to-copy Spec Kit installation with the
# speckit-plus converge preset and baseline extension already applied.
#
# Needs the pinned Spec Kit CLI on PATH (see SPECKIT_VERSION). Run it after
# changing preset/ or extension/, or when moving to a newer Spec Kit release.
set -eu

SPECKIT_VERSION="1.1.2"

repo=$(cd "$(dirname "$0")/.." && pwd)
have=$(specify --version 2>/dev/null | awk '{print $NF}')
[ "$have" = "$SPECKIT_VERSION" ] || {
    echo "need specify $SPECKIT_VERSION on PATH, found '${have:-none}'" >&2
    echo "install it with: uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git@v$SPECKIT_VERSION" >&2
    exit 1
}

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cd "$work"
specify init --here --force --integration codex --integration-options="--skills" \
    --script sh --ignore-agent-tools >/dev/null
specify preset add --dev "$repo/preset" >/dev/null
specify extension add --dev "$repo/extension" >/dev/null

# Catalog caches are downloaded data, not part of the installation.
rm -rf .specify/extensions/.cache .specify/integrations/.cache .specify/presets/.cache

if grep -rIl -e "$repo" -e "$work" .agents .specify >/dev/null 2>&1; then
    echo "generated files contain a path from this machine:" >&2
    grep -rIl -e "$repo" -e "$work" .agents .specify >&2
    exit 1
fi

rm -rf "$repo/template"
mkdir "$repo/template"
cp -R .agents .specify "$repo/template/"
echo "$SPECKIT_VERSION" > "$repo/template/SPECKIT_VERSION"
echo "template rebuilt from Spec Kit $SPECKIT_VERSION: $(find "$repo/template" -type f | wc -l) files"
