# Architecture: [PRODUCT NAME]

**Version**: 0.1.0 | **Last amended**: [YYYY-MM-DD]

This file says HOW the product is built. It is an index: detail lives in plans, contracts and code.
Product behavior lives in [product.md](product.md). The reasons live in [decisions.md](decisions.md).
Amend changes approved meaning with user approval. After DONE, converge automatically
writes new or meaning-preserving lessons; contradictions become product open questions.
Every write-back row carries its source feature; keep memory free of sensitive values.

## Stack

Choices only. Exact versions live in the lockfiles.

| Area | Choice | Decision |
|------|--------|----------|
| [Language / runtime] | [Choice] | [D-001] |

## Parts and boundaries

Each part, what it owns, where its code lives, and what it may depend on. **Paths** are folders,
files or globs, comma separated; a root file or a hidden folder that is product code belongs here
too. Paths inform context selection; planned parts need no code yet.
Keep the Tooling row only for paths the project uses; add hidden CI/deployment folders explicitly.

| Part | Owns | Paths | May depend on |
|------|------|-------|---------------|
| Tooling | Build, dependency and test configuration | package*.json, *lock*, tsconfig*.json, pyproject.toml, requirements*.txt, Dockerfile*, Makefile, tests, scripts | - |
| [Name] | [Data, rule or responsibility it is the one authority for] | [src/name] | [Parts] |

## Architecture rules

Design constraints that every plan and all code must follow. Delivery non-negotiables live
only in Delivery standards. **Check** is optional: a command that exits non-zero when the
rule is broken, such as the project's own lint or architecture test.
Write a pipe inside a command as `\|`.

| ID | Rule | Check |
|----|------|-------|
| AR-001 | [One sentence.] | - |

## Delivery standards

These 14 areas stay in every project. Status is `decided`, `undecided`, or `n/a: <reason>`.
Blocking is `yes` or `no`; blocking rows are the project's non-negotiables and this table is
their only home. A decided Check command becomes a Quality gates row in the feature plan.
Use `-` when there is no command; escape pipes as `\|`. Resolve an undecided area through
amend when a feature first touches it. The git defaults below are proposals until approved.

| Area | Status | Rule | Check | Blocking |
|------|--------|------|-------|----------|
| git & branching | undecided | Branches: <type>/<id>-<short-name>; type feature, fix, hotfix, refactor, docs or chore; id is the ticket, otherwise spec number. Conventional Commits: <type>[optional scope]: <Description>; types feat, fix, refactor, perf, test, docs, style, build, ci, ops, chore, revert. Subject at most 50 characters, capitalized imperative description, no trailing period. Optional body wrapped at 72 characters after a blank line; Refs: <ticket or spec id> footer matches branch id. | - | no |
| PRs & review | undecided | - | - | no |
| environments | undecided | - | - | no |
| CI/CD | undecided | - | - | no |
| code quality | undecided | - | - | no |
| testing | undecided | - | - | no |
| documentation | undecided | - | - | no |
| issues & tasks | undecided | - | - | no |
| release & versioning | undecided | - | - | no |
| security | undecided | - | - | no |
| database changes | undecided | - | - | no |
| observability | undecided | - | - | no |
| dependencies | undecided | - | - | no |
| repository governance | undecided | - | - | no |

## Interfaces and contracts

Links to the contracts between parts and to the outside.

- [Name: a Markdown link to the contract file]
