---
description: "Run the deterministic baseline check and write the calculated cells"
---

# Baseline Check

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

This command runs a script. The script decides; do not replace its result with your own judgment. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`, run from the repository root. `<feature>` is the current feature folder, such as `specs/001-login`; any form of that path works.

## Which form to run

| When | Run | Why |
|------|-----|-----|
| After specify | `CHECK --write --repin <feature>/spec.md` | Records the spec as the owner of its capability and pins the entries the spec cites. |
| After plan | `CHECK --write --repin <feature>/plan.md` | Pins the stack, the parts and the entries the plan cites. It leaves the spec's pins alone. |
| Before analyze | `CHECK` | Read-only. Its errors go into the analysis as critical findings. |
| Before implement | `CHECK --run-rule-checks` | Stops implementation while anything is wrong. |
| After converge | `CHECK --write` | Recalculates Delivery. |
| After implement | `CHECK --write --stamp <feature>` | Recalculates Delivery from the finished record, and records the synced point of the parts this feature's plan lists. |
| On request, or in CI | `CHECK --strict` | Read-only; warnings count as errors. |

## What it checks

- IDs are unique, and every ID on a citation line of a spec or plan exists. The citation lines are `**Implements**`, `**Changes**`, `**Product rules**`, `**Architecture rules**`, `**Decisions**` and `**Parts**`. IDs in prose are not citations.
- Every unfinished spec names a capability, each one is `approved`, and none is blocked by an open question.
- One spec implements a capability. A later spec that changes it lists it under `**Changes**:`.
- No unfinished spec or plan cites a decision that is rejected or superseded.
- **Stale pins**: a cited entry, a listed part or the stack changed after the spec or plan was written. A capability that changes after its feature was verified is reported too.
- **Unsupported DONE**: `Completion: DONE` in `verification.md` is a claim. It is an error, and the capability stays `in progress`, unless all of these hold:
  - `plan.md` and `tasks.md` exist, and every task is checked;
  - the record has a tested revision and no unfilled placeholder;
  - every FR, AS and TR ID in `spec.md` appears in a Coverage row whose status is `PASS`, and no status is outside `PASS`, `FAIL`, `NOT RUN`, `BLOCKED`;
  - the Execution table has at least one command, every exit code is `0`, and no count reports a failure;
  - no row outside "Historical runs" is open, failed or skipped, and every evidence link resolves;
  - the convergence `Outcome:` is `converged`.
- **Evidence still current**: `spec.md` or `plan.md` changed after the feature was verified, and `verification.md` did not.
- **Code against the map**: code that no part maps, a built part whose paths match no file, and a part whose code changed since its synced point while no unfinished feature lists that part.
- **Rule checks**: with `--run-rule-checks`, each architecture rule's Check command. A failing rule marked Blocking is an error; any other is a warning.
- **History**: a baseline row that was deleted since the last commit is an error; a rewritten decision is a warning.
- Dependencies between capabilities exist and form no cycle. Links inside the three baseline files resolve.

`--strict` turns warnings into errors.

## What it writes

The script writes only what it calculates, and never the meaning of an entry:

- with `--write`: the Delivery and Owning spec cells of `product.md`, and the State cell of the parts table;
- with `--repin`: `<feature>/baseline-pins.json`;
- with `--stamp` or `--mode`: `.specify/memory/baseline-state.json`.

In blocking mode it writes nothing when it reports an error. Commit what it wrote with the work that caused the change.

## Modes

`CHECK --mode advisory` makes the check report errors without stopping the work; `CHECK --mode blocking` makes errors stop it again. A new project is blocking. A project that adopts the baseline with code already written starts advisory, and switches once the check is clean. A project with no `product.md` has no baseline, and the check passes with a note.

## Act on the result

- **Exit 0**: report the result and every warning, then continue.
- **Exit 1**: show the errors exactly as printed. Before implement, stop: implementation does not start until they are fixed.
- **Stale pin**: re-read the changed entry with `CHECK --context --ids <ID>`, update the spec or plan if the change affects it, then `CHECK --repin <feature>/spec.md` or `<feature>/plan.md`. Repin only the file you re-read.
- **A part changed since its synced point**, or **code no part maps**: run the baseline reconcile command.
- Anything that needs a change to the meaning of `product.md`, `architecture.md` or `decisions.md` goes to the user through the baseline amend command; do not edit those files here.
