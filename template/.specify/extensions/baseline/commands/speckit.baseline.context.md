---
description: "Before specify or plan: pick the path for the request, load the relevant baseline entries, and put conflicts to the user"
---

# Baseline Context

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

This command runs as a hook before specify and before plan. It reads the baseline and never edits it. Changes go through the baseline amend command.

The script selects the entries; do not load the baseline files whole. Its output is complete for the step: it carries the purpose, the rules, the decisions, the open questions, the stack and the contracts that apply. In the commands below, `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`.

If `.specify/memory/product.md` does not exist, the project has no baseline. Say so, recommend the baseline amend command (or the baseline recover command when the project already has code), and let the calling command continue.

## Before specify

### 1. Pick the path

Process weight follows the size of the change. Classify the request first:

| Request | Path |
|---------|------|
| New behavior that no capability promises yet | Full path. The spec **implements** the capability. |
| Changed behavior of a capability that a spec already implements | Full path. If the promise itself changes, amend the capability row first. The new spec **changes** the capability; the first spec stays its owner. |
| Bug: an approved behavior is violated | Fix path: name the capability or requirement that is violated, reproduce it with a failing test, fix, and run the gates. No new spec. Use the bug commands if that extension is installed. |
| Behavior stays the same (refactor, dependency, tidy-up) | Small-change path: state what must not change, make the change, and run the gates. No new spec. |

If the request is not a full path, say which path applies and why, and stop the specify command there. After a fix or a small change is done, run the baseline reconcile command so the change is recorded.

### 2. Load only what is relevant

```sh
CHECK --context                        # purpose, the capability index, product rules, product decisions, open questions
CHECK --context --ids CAP-NNN,CAP-NNN  # the full rows you picked, and the open questions that block them
```

Pick the capabilities this request touches from the index, then load those rows. Do not load architecture or stack detail; the spec stays free of technology.

### 3. Check the request against the product

Look for each of these, and put every finding to the user with options (adapt the request, amend the baseline, or defer it as an open question) and your recommendation:

- a capability that already promises this (duplicate);
- a capability, product rule or accepted product decision this would contradict, or a rejected option it would bring back;
- an open question that blocks a capability this request touches. It must be answered through the baseline amend command before the spec is written;
- a dependency on a capability whose Delivery is not `verified`;
- a promise that has no capability row. It needs an approved row before the spec is written: run the baseline amend command first.

### 4. Hand over

Give the specify command this block, and have it written directly below the `**Input**` line of `spec.md`:

```markdown
**Implements**: CAP-NNN[, CAP-NNN]      (new capabilities; leave the line out when there are none)
**Changes**: CAP-NNN[, CAP-NNN]         (capabilities another spec already implements; leave out when none)
**Product rules**: PR-NNN[, PR-NNN] or none
**Baseline**: <output of `git rev-parse --short HEAD`>
```

Every capability listed must be `approved`. Ownership is calculated on read; do not edit a calculated ownership cell.

## Before plan

### 1. Load

List the folders and files this feature will create or change, then load exactly what governs them:

```sh
CHECK --context --paths src/billing,src/api/invoices.py
```

The output has the stack, the parts touched and a ready `**Parts**:` line, every architecture rule, the accepted decisions that govern those paths, the rejected or superseded ones, and the interfaces and contracts. Do not propose an option that appears in the rejected list unless the user asks to reopen it.

### 2. Label the impact

Compare the intended design with the stack, the parts and boundaries, and the architecture rules:

- **none**: the plan uses what exists.
- **extends**: the plan adds a part, an interface or a dependency without changing a rule or a boundary.
- **changes**: the plan needs a different stack choice, a moved boundary, or an exception to a rule.

On **extends** or **changes**, stop and ask the user: fit the plan to the architecture, or amend the architecture. An amendment runs the baseline amend command and records a decision before planning continues. A new folder of code needs a part that maps it; the part is added as `planned`, and needs no code yet.

### 3. Hand over

Give the plan command this block, and have it written directly below the `**Input**` line of `plan.md`:

```markdown
**Architecture impact**: none | extends | changes
**Architecture rules**: AR-NNN[, AR-NNN] or none
**Decisions**: D-NNN[, D-NNN] or none
**Parts**: <every part this feature creates or changes code in, by name> or none
**Baseline**: <output of `git rev-parse --short HEAD`>
```

The `**Parts**:` line matters: the check pins those parts, and while this feature is unfinished it expects their code to change.
