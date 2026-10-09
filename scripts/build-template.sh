#!/bin/sh
# Rebuild template/ : a complete, ready-to-copy Spec Kit installation with the
# speckit-pro preset, baseline extension and workflow already applied.
#
# Needs the Spec Kit CLI named in the SPECKIT_VERSION file on PATH. Run it after
# changing preset/, extension/ or workflow/, or when moving to a newer Spec Kit release.
set -eu

repo=$(cd "$(dirname "$0")/.." && pwd)
SPECKIT_VERSION=$(cat "$repo/SPECKIT_VERSION")
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
specify workflow add --dev "$repo/workflow" >/dev/null
# The workflow registry records where a local workflow came from; keep this machine's path out.
python3 - <<'PYREG'
import json
from pathlib import Path
p = Path('.specify/workflows/workflow-registry.json')
data = json.loads(p.read_text())
data['workflows']['speckit-pro']['source'] = 'speckit-pro'
p.write_text(json.dumps(data, indent=2) + '\n')
PYREG

# Generated registries must be byte-reproducible; timestamps are installation metadata.
python3 - <<'PYNORMAL'
import json
import shutil
from pathlib import Path
for directory in (Path('.agents'), Path('.specify')):
    for cache in directory.rglob('__pycache__'):
        shutil.rmtree(cache)
for p in Path('.specify').rglob('*'):
    if p.is_file() and (p.suffix == '.json' or p.name == '.registry'):
        data = json.loads(p.read_text())
        def normalize(value):
            if isinstance(value, dict):
                return {k: normalize(v) for k, v in value.items() if k not in ('installed_at', 'updated_at')}
            if isinstance(value, list): return [normalize(v) for v in value]
            return value
        p.write_text(json.dumps(normalize(data), indent=2, sort_keys=True) + '\n')
PYNORMAL
printf '\n.baseline-local/\n' >> .specify/.gitignore

# Catalog caches are downloaded data, not part of the installation.
rm -rf .specify/extensions/.cache .specify/integrations/.cache .specify/presets/.cache

if grep -FrIl -e "$repo" -e "$work" .agents .specify >/dev/null 2>&1; then
    echo "generated files contain a path from this machine:" >&2
    grep -FrIl -e "$repo" -e "$work" .agents .specify >&2
    exit 1
fi

rm -rf "$repo/template"
mkdir "$repo/template"
cp -R .agents .specify "$repo/template/"
echo "$SPECKIT_VERSION" > "$repo/template/SPECKIT_VERSION"
echo "template rebuilt from Spec Kit $SPECKIT_VERSION: $(find "$repo/template" -type f | wc -l) files"
