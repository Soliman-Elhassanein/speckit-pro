#!/bin/sh
# Insert the universal-profile converge rules into an installed Markdown converge
# command. Use it where `specify preset add` cannot reach the command: the generic
# integration with a custom commands directory, such as .agent/commands.
#
# Usage: sh apply-converge.sh <path/to/speckit.converge.md>
# Running it again replaces the existing rules block instead of adding a second one.
set -eu

target=${1:?usage: sh apply-converge.sh <path/to/installed converge command .md>}
rules=$(dirname "$0")/commands/speckit.converge.md

[ -f "$target" ] || { echo "not found: $target" >&2; exit 1; }
[ -f "$rules" ] || { echo "rules file missing: $rules" >&2; exit 1; }
[ "$(head -n 1 "$target")" = "---" ] || { echo "no YAML frontmatter in: $target" >&2; exit 1; }

tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

awk -v rules="$rules" '
BEGIN {
    begin = "<!-- universal-profile:converge:begin -->"
    end = "<!-- universal-profile:converge:end -->"
    # Rules body: everything after the rules file frontmatter, minus the wrap placeholder.
    while ((getline line < rules) > 0) {
        if (fm < 2) { if (line == "---") fm++; continue }
        if (line == "{CORE_TEMPLATE}") continue
        body[++n] = line
    }
    close(rules)
    first = 1; while (first <= n && body[first] == "") first++
    last = n; while (last >= first && body[last] == "") last--
}
function flush() { if (held) { print hold; held = 0 } }
# Drop a previously inserted block together with the blank line before it.
$0 == begin { if (held && hold == "") held = 0; flush(); skipping = 1; next }
skipping { if ($0 == end) skipping = 0; next }
{
    flush(); hold = $0; held = 1
    if (NR == 1) { infm = 1; next }
    if (infm && $0 == "---") {
        infm = 0; flush()
        print ""; print begin
        for (i = first; i <= last; i++) print body[i]
        print end
    }
}
END { flush() }
' "$target" > "$tmp"

cat "$tmp" > "$target"
echo "converge rules applied to $target"
