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

The script selects the entries; do not load the baseline files whole. In the commands below, `CHECK` stands for `python3 .specify/extensions/baseline/scripts/baseline_check.py`.

If `.specify/memory/product.md` or `.specify/memory/architecture.md` does not exist, say so, recommend the baseline amend command (or the baseline recover command when the project already has code), and let the calling command continue.

## Before specify

### 1. Pick the path

Process weight follows the size of the change. Classify the request first:

| Request | Path |
|---------|------|
| New or changed behavior | Full path: continue with specify. |
| Bug: an approved behavior is violated | Fix path: name the capability or requirement that is violated, reproduce it with a failing test, fix, and run the gates. No new spec. Use the bug commands if that extension is installed. |
| Behavior stays the same (refactor, dependency, tidy-up) | Small-change path: state what must not change, make the change, and run the gates. No new spec. |

If the request is not the full path, say which path applies and why, and stop the specify command there. After a fix or a small change is done, run the baseline reconcile command so the change is recorded.

### 2. Load only what is relevant

```sh
CHECK --context                      # the capability index: one line each
CHECK --context --ids CAP-NNN,CAP-NNN  # the full rows you picked, plus every product rule
```

Pick the capabilities this request touches from the index, then load only those rows. Do not load architecture or stack detail; the spec stays free of technology.

### 3. Check the request against the product

Look for each of these, and put every finding to the user with options (adapt the request, amend the baseline, or defer it as an open question) and your recommendation:

- a capability that already promises this (duplicate);
- a capability or product rule this would contradict;
- a dependency on a capability whose Delivery is not `verified`;
- a promise that has no capability row. It needs an approved row before the spec is written: run the baseline amend command first.

### 4. Hand over

Give the specify command this block, and have it written at the top of `spec.md`:

```markdown
**Implements**: CAP-NNN[, CAP-NNN]
**Product rules**: PR-NNN[, PR-NNN] or none
**Baseline**: <output of `git rev-parse --short HEAD`>
```

Every capability listed must be `approved`. Set this spec as the owning spec of each one through the baseline amend command if the row still shows `-`.

## Before plan

### 1. Load

List the folders and files this feature will create or change, then load exactly what governs them:

```sh
CHECK --context --paths src/billing,src/api/invoices.py
```

The output has the parts touched, every architecture rule, the accepted decisions that govern those paths, and the rejected or superseded ones. Do not propose an option that appears in the rejected list unless the user asks to reopen it.

### 2. Label the impact

Compare the intended design with the stack, the parts and boundaries, and the architecture rules:

- **none**: the plan uses what exists.
- **extends**: the plan adds a part, an interface or a dependency without changing a rule or a boundary.
- **changes**: the plan needs a different stack choice, a moved boundary, or an exception to a rule.

On **extends** or **changes**, stop and ask the user: fit the plan to the architecture, or amend the architecture. An amendment runs the baseline amend command and records a decision before planning continues. A new folder of code needs a part that maps it.

### 3. Hand over

Give the plan command this block, and have it written at the top of `plan.md`:

```markdown
**Architecture impact**: none | extends | changes
**Architecture rules**: AR-NNN[, AR-NNN] or none
**Decisions**: D-NNN[, D-NNN] or none
**Baseline**: <output of `git rev-parse --short HEAD`>
```
