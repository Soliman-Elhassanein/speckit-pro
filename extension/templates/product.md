# Product: [PRODUCT NAME]

**Version**: 0.1.0 | **Last amended**: [YYYY-MM-DD]

This file says WHAT the product does. It holds no technology choices; those live in
[architecture.md](architecture.md). The reasons live in [decisions.md](decisions.md).
Only the baseline amend command edits this file, and only after the user approves the change.

## Purpose and users

[Two to five lines: what the product is for, and who uses it.]

## Product rules

Rules that every feature must respect.

| ID | Rule |
|----|------|
| PR-001 | [One sentence.] |

## Capabilities

One row per promise that can be delivered on its own. A promise built in two steps is two rows.
Each row has one owning spec; a change to the promise amends that spec.

- **Decision** is typed here: `proposed`, `approved`, `superseded`, or `retired`. Rows are never deleted.
- **Depends on** lists the capabilities that must be verified first, or `-`.
- **Owning spec** and **Delivery** are never typed. The baseline check script calculates them: the
  owner is the spec that implements the capability, and Delivery is `unstarted`, `in progress`, or
  `verified` from the `verification.md` of that spec and of every spec that changes the capability.

| ID | Promise | Decision | Depends on | Owning spec | Delivery |
|----|---------|----------|------------|-------------|----------|
| CAP-001 | [One line the user would recognise.] | proposed | - | - | unstarted |

## Open questions

Questions that were deferred, so they are not lost. **Blocks** names the capabilities that cannot
be specified until the question is answered. **Status** is `open` or `answered by D-NNN`; rows stay.

| ID | Question | Blocks | Raised | Status |
|----|----------|--------|--------|--------|
| Q-001 | [Question.] | [CAP-NNN, or "nothing yet"] | [YYYY-MM-DD] | open |
