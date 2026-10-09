---
name: speckit-baseline-check
description: Validate baseline pins and current evidence; calculate status without editing shared rows
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Soliman-Elhassanein
  source: baseline:commands/speckit.baseline.check.md
---

# Baseline Check

## User Input

```text
$ARGUMENTS
```

Consider the input. Run the script; do not replace its result with your judgment.
`CHECK` means `python3 .specify/extensions/baseline/scripts/baseline_check.py` from the root.
`<feature>` means the explicit current feature folder (or `--feature current` to read `.specify/feature.json`).

| When | Run | Purpose |
|------|-----|---------|
| After specify | `CHECK --write --feature <feature> --repin <feature>/spec.md` | Record initial citations without modifying shared baseline rows. |
| After plan | `CHECK --write --feature <feature> --repin <feature>/plan.md` | Record stack, parts and plan citations; preserve spec pins. |
| Before analyze | `CHECK --feature <feature>` | Add errors to analysis as critical findings. |
| Before implement | `CHECK --gate --feature <feature>` | Mandatory read-only check, including executable architecture rules. |
| Final verification | `CHECK --record-run --feature <feature>` | Execute every planned quality gate and record inputs, exit codes and hashed logs. |
| After converge | `CHECK --write --feature <feature>` | Accept supported DONE evidence. |
| After implement | `CHECK --write --feature <feature> --stamp <feature>` | Accept supported DONE and synchronize its parts. |
| Final workflow gate | `CHECK --gate --require-done --feature <feature>` | Independently require current completion after all agent steps. |
| Global CI | `CHECK --gate --strict --base <accepted-or-PR-base-commit>` | Check all features and accepted history; warnings fail. |
| Inspect status | `CHECK --status --json` | Calculate capability ownership, delivery and part state on read. |

## Checks and evidence

IDs and table widths must be valid; escape command pipes as `\|`. Citation lines are
`**Implements**`, `**Changes**`, `**Product rules**`, `**Architecture rules**`,
`**Decisions**` and `**Parts**`. Each capability has one implementing owner.
New completion must be approved, unblocked by open questions and free of rejected
or superseded cited decisions, including on the first DONE claim.

DONE requires plan, verification plan, complete quality gates, checked tasks,
passing FR/AS/TR coverage, numeric execution counts with no failed/skipped/xfailed
checks, existing local evidence, known uppercase statuses and converged outcome.
A skip reason alone never waives a required check.

`verification-run.json` must match the spec, plan, task meaning (checkboxes excluded),
governing baseline entries, constitution when present, listed parts' code, shared `**Verification inputs**` parts (such as Tooling) and linked
local contracts. Each recorded command must match the planned gate and have exit 0
and an unchanged log. Cosmetic edits to verification.md or reconciliation stamps
cannot renew evidence. Complete the Markdown report from the recorded run's exact
commands and log paths; never invent results. Manual observations in the JSON record
need method, platform, expected/observed result, PASS, existing local evidence and its SHA-256 digest (first 16 hexadecimal characters).
Local files are reviewable evidence, not cryptographic attestation of a trusted runner.

## Reviewed changes

Use `--repin <feature>/spec.md` or `plan.md` for the file you actually reviewed.
Changing an existing pin requires `--reason`. Use `--dry-run` to preview writes;
with `--record-run` it previews commands without executing them. A spec edit also
requires reviewing its downstream plan/tasks, then `--feature <feature>
--acknowledge --reason "..."`. This acknowledgment does not renew test evidence.
A valid targeted repin may be saved while other features still report errors.
Global baseline structure and history errors still prevent acceptance.

For an amended capability, create a new `**Changes**:` spec. Initial repinning freezes
its predecessor's accepted revision and the new capability revision. For a second
change, name `**Previous change**: specs/<previous-change>`. Preserve predecessor
pins and run records as historical evidence; do not reanchor old tests onto new
promises. Parallel unrelated features need no shared calculated-cell edits.

## Drift and persistence

Map root tooling and hidden product code explicitly. Unfinished features only excuse
reconciliation warnings for listed parts; they never excuse stale completed evidence.
Inactive unfinished work is reported after 30 days. Set `Completion: ABANDONED` when
work is abandoned; it provides no drift exemption. Feature-scoped stamping requires
supported DONE. Global reconciliation stamps need `--reason` when code changed.

Writes go to per-feature pins/run records, per-part `.specify/memory/stamps/` files,
and initial adoption/mode in baseline-state.json. Product and architecture rows are
never rewritten. Legacy calculated columns are ignored. A checkout lock and journal
make mutations recoverable, and changed inputs abort acceptance. An interrupted
transaction blocks gates; run a regular check to recover before retrying.

Advisory mode is for recovery diagnostics. Invalid evidence is never accepted;
`--gate` always blocks and cannot mutate or weaken checks. Non-adopter discovery is
permissive; a missing adopted baseline or required gate baseline fails. Initialize an
accepted history base with `CHECK --write --base HEAD` after creating the baseline.
CI supplies the PR base explicitly, with full Git history. Deleted accepted IDs and
rewritten decision text fail; retire rows or create a superseding decision instead.

The installer preserves foreign Git hooks. Integrate its printed invocation when
necessary; local hooks can be bypassed. CI must be configured with the project's
runtime and required in repository branch settings. Analysis and convergence judge
assertion meaning and architecture intent; the script checks their records and
executable rules, not the truth of their semantic conclusions.