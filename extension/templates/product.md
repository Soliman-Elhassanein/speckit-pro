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
- **Delivery** is never typed. The baseline check script calculates it from the owning spec's
  `verification.md`: `unstarted`, `in progress`, or `verified`.

| ID | Promise | Decision | Owning spec | Delivery |
|----|---------|----------|-------------|----------|
| CAP-001 | [One line the user would recognise.] | proposed | - | unstarted |

## Open questions

Questions that were deferred, so they are not lost.

| ID | Question | Blocks | Raised |
|----|----------|--------|--------|
| Q-001 | [Question.] | [CAP or step it blocks, or "nothing yet"] | [YYYY-MM-DD] |
