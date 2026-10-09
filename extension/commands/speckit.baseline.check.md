---
description: "Run the deterministic baseline check and recalculate delivery status"
---

# Baseline Check

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

This command runs a script. The script decides; do not replace its result with your own judgment. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`, run from the repository root.

## Which form to run

| When | Run | Why |
|------|-----|-----|
| After specify, after plan | `CHECK --repin <spec folder>` | Pins each baseline entry the new file cites, so a later change to that entry is noticed. |
| Before analyze | `CHECK` | Read-only. Its errors go into the analysis as critical findings. |
| Before implement | `CHECK --run-rule-checks` | Stops implementation while anything is wrong. |
| After converge, and again after the outcome is recorded in `verification.md` | `CHECK --write`; add `--stamp` when the outcome was `converged` | Recalculates Delivery; the stamp records that code and baseline agree. |
| On request | `CHECK` | Read-only. |

## What it checks

- IDs are unique, and every ID cited in a spec or plan exists.
- Every spec names the capabilities it implements, and each one is `approved`.
- Each capability's owning spec exists and names that capability.
- No spec or plan cites a decision that is `rejected` or superseded.
- **Stale pins**: a baseline entry changed after an unfinished spec or plan cited it.
- **Code against the map**: a part whose path matches no file (error), code that no part maps (warning), and mapped code that changed since the last stamp with no feature in progress (warning).
- **Rule checks**: with `--run-rule-checks`, each architecture rule's Check command. A failing rule marked Blocking is an error; any other is a warning.
- Links inside the three baseline files resolve.
- The Delivery column matches the owning spec's `verification.md`: `verified` only when it says `Completion: DONE`.
- **Unsupported DONE**: `Completion: DONE` is an error, and the capability stays `in progress`, while the same file has a row that is `NOT RUN`, `FAIL` or `BLOCKED` outside "Historical runs", a coverage count that is not complete, or a convergence `Outcome:` other than `converged`, or while `tasks.md` has an unchecked task.

`--strict` turns warnings into errors.

## Act on the result

- **Exit 0**: report the result and every warning, then continue.
- **Exit 1**: show the errors exactly as printed. Before implement, stop: implementation does not start until they are fixed.
- **Stale pin**: re-read the changed entry with `CHECK --context --ids <ID>`, update the spec or plan if the change affects it, then `CHECK --repin <spec folder>`.
- **Changed outside the process**, or **code no part maps**: run the baseline reconcile command.
- Anything that needs a change to `product.md`, `architecture.md` or `decisions.md` goes to the user through the baseline amend command; do not edit those files here.

The script writes only the Delivery cells of `product.md` and the generated file `.specify/memory/baseline-state.json`. Commit both with the work that caused the change.
