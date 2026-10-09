#!/bin/sh
# Install the speckit-pro commit-msg hook in the current git repository.
# The hook rejects a commit whose message, author or committer names a coding
# agent as a contributor. Safe to run again; it never replaces a hook it did
# not write.
set -eu

hooks=$(git rev-parse --git-path hooks 2>/dev/null) || {
    echo "not a git repository yet; run this again after git init" >&2
    exit 0
}
marker="speckit-pro: no agent as a contributor"
hook="$hooks/commit-msg"
call='python3 "$(git rev-parse --show-toplevel)/.specify/extensions/baseline/scripts/baseline_check.py" --commit-msg "$1"'

if [ -e "$hook" ] && ! grep -q "$marker" "$hook"; then
    echo "this repository already has its own commit-msg hook: $hook" >&2
    echo "add this line to it so that agents cannot list themselves as contributors:" >&2
    echo "  $call || exit 1" >&2
else

mkdir -p "$hooks"
cat > "$hook" <<HOOK
#!/bin/sh
# $marker
script="\$(git rev-parse --show-toplevel)/.specify/extensions/baseline/scripts/baseline_check.py"
[ -f "\$script" ] || exit 0
exec python3 "\$script" --commit-msg "\$1"
HOOK
chmod +x "$hook"
echo "installed the commit-msg hook: $hook"
fi

# A work-in-progress commit checks structure, not completed acceptance evidence.
pre="$hooks/pre-commit"
if [ ! -e "$pre" ] || grep -q "speckit-pro: structural baseline" "$pre"; then
    cat > "$pre" <<'PRE'
#!/bin/sh
# speckit-pro: structural baseline
script="$(git rev-parse --show-toplevel)/.specify/extensions/baseline/scripts/baseline_check.py"
[ -f "$script" ] || exit 0
exec python3 "$script" --structural
PRE
    chmod +x "$pre"
else
    echo "existing pre-commit hook preserved; add the baseline --structural invocation to it" >&2
fi
