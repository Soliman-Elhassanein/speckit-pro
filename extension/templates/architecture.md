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

Each part, what it owns, where its code lives, and what it may depend on. **Paths** are folders
or globs, comma separated. The check script uses them to notice code that changed outside the
process and code that no part maps.

| Part | Owns | Paths | May depend on |
|------|------|-------|---------------|
| [Name] | [Data, rule or responsibility it is the one authority for] | [src/name] | [Parts] |

## Architecture rules

Rules that every plan and all code must follow. **Blocking** is `yes` or `no`: a broken blocking
rule stops the work; any other becomes a refactor task. **Check** is optional: a command that
exits non-zero when the rule is broken, such as the project's own lint or architecture test.

| ID | Rule | Blocking | Check |
|----|------|----------|-------|
| AR-001 | [One sentence.] | no | - |

## Interfaces and contracts

Links to the contracts between parts and to the outside.

- [Name: a Markdown link to the contract file]
