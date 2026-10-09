---
name: speckit-baseline-reconcile
description: Reconcile code that changed outside the process with the baseline and the specs
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Soliman-Elhassanein
  source: baseline:commands/speckit.baseline.reconcile.md
---

# Reconcile Changes Made Outside the Process

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

Use this after a bug fix, a small change, a manual edit, or whenever the baseline check warns that mapped code changed with no feature in progress. It proposes; the user decides; only the baseline amend command writes the baseline. `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`.

## Steps

### 1. Find what changed

Run `CHECK`. It names each part whose code changed since its synced point, and code that no part maps. Then look at those folders:

```sh
git diff --stat <commit> HEAD -- <paths of the changed parts>
git status --short
CHECK --context --paths <changed folders, comma separated>
```

`<commit>` is the `commit` value under `stamp` in `.specify/memory/baseline-state.json`. If history was rewritten and that commit is gone, use `git log -- <paths>` to find the changes, or ask the user which commit to compare against.

### 2. Classify each change

Read the diff, not just the file names. Put every change in exactly one row:

| What the change did | Action |
|---------------------|--------|
| Fixed code so it matches an approved capability or requirement | Nothing to amend. Note the capability or requirement it restored. |
| Changed behavior that an owning spec describes | The owning spec must be amended, or the code reverted. Ask the user which. |
| Added behavior no capability promises | Propose a capability row (`proposed`), or removal of the code. Ask the user. |
| Moved a boundary, added a part, a dependency or a folder of code | Propose the architecture amendment and a decision row. Ask the user. |
| Broke an architecture rule | Blocking rule: stop and report. Otherwise propose a refactor task or an approved exception. |
| Changed nothing a user or a rule can observe | Nothing to amend. |

Never resolve a difference by quietly editing the baseline to match the code.

### 3. Decide with the user

Present the table, with your recommendation for every row that needs a decision. Ask one question at a time.

### 4. Apply

- Baseline changes the user approved: run the baseline amend command with them.
- Spec changes the user approved: amend the owning spec in place, keeping its IDs. Then update its plan and tasks where the change reaches them, and verify again: the check rejects a finished feature whose spec changed after its last recorded run.
- Code the user wants reverted or refactored: add the work to the owning spec's `tasks.md`, or do it if it is small and the user says so.

### 5. Record the new synced point

Once the code, the specs and the baseline agree:

```sh
CHECK --write --stamp
```

A bare `--stamp` records every part as agreeing with the baseline, so run it only after every change in step 2 has a decision. Report what changed, what was decided, and the check result. Commit the reconciliation as its own unit.