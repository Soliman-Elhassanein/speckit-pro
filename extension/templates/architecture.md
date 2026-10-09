# Architecture: [PRODUCT NAME]

**Version**: 0.1.0 | **Last amended**: [YYYY-MM-DD]

This file says HOW the product is built. It is an index: detail lives in plans, contracts and code.
Product behavior lives in [product.md](product.md). The reasons live in [decisions.md](decisions.md).
Only the baseline amend command edits this file, and only after the user approves the change.

## Stack

Choices only. Exact versions live in the lockfiles.

| Area | Choice | Decision |
|------|--------|----------|
| [Language / runtime] | [Choice] | [D-001] |

## Parts and boundaries

Each part, what it owns, and what it may depend on.

| Part | Owns | May depend on |
|------|------|---------------|
| [Name] | [Data, rule or responsibility it is the one authority for] | [Parts] |

## Architecture rules

Rules that every plan must follow.

| ID | Rule |
|----|------|
| AR-001 | [One sentence.] |

## Interfaces and contracts

Links to the contracts between parts and to the outside.

- [Name: a Markdown link to the contract file]
