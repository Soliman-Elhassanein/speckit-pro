---
name: speckit-baseline-amend
description: Create or amend product.md, architecture.md and decisions.md, each change approved by the user first
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Soliman-Elhassanein
  source: baseline:commands/speckit.baseline.amend.md
---

# Amend the Project Baseline

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## What the baseline is

Three files beside the constitution, each the one home for its kind of fact:

| File | Holds | Never holds |
|------|-------|-------------|
| `.specify/memory/product.md` | WHAT: purpose, product rules, one row per capability | Technology choices |
| `.specify/memory/architecture.md` | HOW: stack, parts and boundaries, architecture rules | Product scope, delivery claims |
| `.specify/memory/decisions.md` | WHY: one row per decision, with rejected options | Anything that is not a decision |

The constitution keeps the working rules. Feature detail stays in `specs/`. These files are indexes that link to detail; keep each entry to one line.

## Rules

1. **Only this command edits what the three files mean.** Every other command reads them and proposes. The check script writes only the cells it calculates: Delivery, Owning spec, and the State of a part.
2. **The user approves every change first.** Show the exact rows you would add or change, then wait for the answer. Do not write on your own judgment.
3. **Never delete or renumber.** A capability that is dropped becomes `retired`; a replaced one becomes `superseded`. A changed decision gets a new row, and the old row's status becomes `superseded by D-NNN`.
4. **Never type a calculated cell.** The check script calculates Delivery and Owning spec. A new capability gets `-` and `unstarted`; a new part gets the State `planned`, and needs no code yet.
5. **Never make code correct by editing the baseline.** If built code differs from an approved entry, the user chooses: fix the code, or approve an amendment. Record that choice as a decision.
6. **One capability, one promise, one owning spec.** A promise that will be delivered in two steps is two rows. A later change to a promise amends the row here first; the spec that builds the change lists the capability under `**Changes**:`.
7. **An answered question stays.** Set its Status to `answered by D-NNN` and record the decision; do not remove the row.

## Steps

### 1. Load

Read the three files if they exist, plus `.specify/memory/constitution.md`. If a file is missing, start it from `.specify/extensions/baseline/templates/` and remove every placeholder row before saving.

### 2. Gather

- **First creation**: read the project's own material (vision, requirement, design and research documents, existing specs and code). Where sources conflict, list the conflict; do not choose silently. For existing code, mark anything you inferred as inferred until the user confirms it.
- **Amendment**: take the change from the user input or from the proposal handed over by another command.

Ask only what blocks the change, one question at a time, each with your recommendation. Park anything else as a row under "Open questions" in `product.md`, with the capabilities it blocks in the Blocks cell: the check stops a spec for a blocked capability until the question is answered.

### 3. Propose

Show the user a short list of the exact changes, grouped by file:

- new rows with their next free ID (`CAP-`, `PR-`, `AR-`, `D-`, `Q-`; three digits, appended above the current maximum);
- for a capability, the capabilities it depends on;
- changed cells, old value and new value;
- the decision row that records why.

Wait for approval. Apply only what was approved.

### 4. Write

- Apply the approved rows.
- Add one `decisions.md` row for every choice the user made, including conflict answers, so the same question is never asked twice.
- Bump the version of each file you changed: MAJOR when existing behavior or a boundary changed, MINOR when something was added, PATCH for wording. Set "Last amended" to today.

### 5. Check and report

Run:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py --write
```

Fix anything it reports that your change caused. When the change makes an unfinished spec or plan stale, that is the check working: re-read the changed entry in that file, then repin that file. Then report: files and versions changed, rows added or changed by ID, decisions recorded, open questions parked, and the check result. Commit the baseline change as its own unit under the project's version-control rules.