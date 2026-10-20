# Product: [PRODUCT NAME]

**Version**: 0.1.0 | **Last amended**: [YYYY-MM-DD]

This file says WHAT the product does. It holds no technology choices; those live in
[architecture.md](architecture.md). The reasons live in [decisions.md](decisions.md).
Amend changes approved meaning with user approval. After DONE, converge automatically
writes new or meaning-preserving lessons; contradictions become product open questions.
Every write-back row carries its source feature; keep memory free of sensitive values.

## Spirit

### Purpose

[One sentence a user understands: why this product exists.]

### Who it's for

[Name the users and what they need.]

### Promises

| ID | Rule |
|----|------|
| PR-001 | [A promise to a named user.] |

### Non-goals

- [What this product deliberately does not do.]

## Capabilities

One row per capability that can be delivered on its own. **Serves** cites the Spirit promise (PR) it serves.
Features cite the capabilities they implement.

- **Decision** is typed here: `proposed`, `approved`, `superseded`, or `retired`. Rows are never deleted.
- **Depends on** lists the capabilities that must be verified first, or `-`.

| ID | Promise | Serves | Decision | Depends on |
|----|---------|--------|----------|------------|
| CAP-001 | [One line the user would recognise.] | PR-001 | proposed | - |

## Open questions

Questions that were deferred, so they are not lost. **Blocks** names the capabilities that cannot
be specified until the question is answered. **Status** is `open` or `answered by D-NNN`; rows stay.

| ID | Question | Blocks | Raised | Status |
|----|----------|--------|--------|--------|
| Q-001 | [Question.] | [CAP-NNN, or "nothing yet"] | [YYYY-MM-DD] | open |
