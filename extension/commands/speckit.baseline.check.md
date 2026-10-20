---
description: "Read-only checks of memory structure, citations and completion records"
---

# Baseline Check

Consider `$ARGUMENTS`. Run from the project root:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py
```

After specify or plan and before analyze or implement, use `--feature <feature folder>`
to check that feature's citations and global memory structure. Without a feature,
check all features. IDs must be valid and unique, typed citations resolve, and governing decisions
be accepted. Spirit must include non-goals; each spec needs a Focus section with
`**Promises**: PR-NNN` or `**Override**: D-NNN` (an accepted override decision).
Capabilities cite their PR in Serves. Delivery standards retain all 14 areas, with
Status `decided`, `undecided`, or `n/a: <reason>` and Blocking `yes` or `no`.
Only dedicated citation lines and typed reference cells govern; ordinary prose and
rejected options do not. The checker does not judge whether a decision really
authorizes an override or a promise fits the named user. Escape pipes in table cells as `\|`.

For existing-code recovery diagnostics use `--mode advisory`. It reports every error
but structural errors do not block recovery. Privacy hits always block, even in
advisory mode. All four memory files are scanned for sensitive paths, IP/email
addresses, credential URLs and common secret shapes. Rewrite hits generically or
drop them before committing. The check changes no setting and writes no files.

After convergence, use `--done --feature <feature folder>` to check the completion
record: checked tasks, all planned gates recorded with exit 0 and local log paths,
no remaining gaps and a converged outcome. DONE always blocks on structural errors.

Report errors verbatim. The script neither runs gate commands nor judges test assertions,
architecture meaning or whether a convergence conclusion is true. Those judgments
belong to analyze, converge and the user. Never claim more than the check establishes.
