# speckit-pro

Project memory and stricter feature rules built on upstream [Spec Kit](https://github.com/github/spec-kit).
Specifications lead implementation: code serves the spec. speckit-pro carries that
principle across the product: every feature serves its purpose, respects its
architecture and remembers past decisions. You approve changes to that intent.
See [CONSTITUTION.md](CONSTITUTION.md) for the spirit and non-goals.

It ships a memory extension (`baseline`) and a feature preset (`universal-profile`),
using upstream hooks, command wraps and template appends. It neither copies upstream
commands nor replaces them. Version 4.0.0 targets Spec Kit 1.2.2 (`>=1.2.2`); newer
versions require the upgrade check below.

## Requirements and installation

Requirements: Spec Kit CLI 1.2.2, Git, Python 3.11+ and a POSIX shell.
Install the Spec Kit CLI yourself (the example uses uv):

```sh
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.2
specify init my-project
```

Clone this repository, then install into the initialized project:

```sh
git clone https://github.com/Soliman-Elhassanein/speckit-pro.git
./speckit-pro/install.sh ./my-project
```

The installer requires `specify`; if absent it prints the install command and
stops. It makes `codex` the sole Spec Kit integration so upstream renders standard
Agent Skills in `.agents/skills/`. If another integration is the default, it prints
what will change, switches through `specify integration switch codex` (or `use`
when Codex is already installed), and uninstalls the others through Spec Kit.
Upstream preserves modified files; no upstream files or integration metadata are
edited by speckit-pro. Resolve any preserved conflicting skills before rerunning.

It adds the upstream Git extension, baseline extension and preset, then sets the
Git defaults listed below, preserving unrelated settings and memory. `--force`
delegates baseline extension and preset updates to upstream. Already installed
components are kept on ordinary reruns. Run `install.sh --help` for usage.

## Several agents in one project

All commands have one real copy in `.agents/skills/`. Agents that read this folder
need no extra installation. Claude Code reads `.claude/skills/`, so install with:

```sh
./speckit-pro/install.sh --agents claude ./my-project
```

This makes `.claude/skills` one relative folder link to `../.agents/skills`, so
Claude Code sees every shared skill, including ones added later, with no second
copy. Keep any other skills in `.agents/skills/` too; `npx skills` installs into
this layout unchanged. A `.claude/skills` folder holding only earlier speckit-pro
links is replaced; a folder with other skills, or another file or link, stops
installation with instructions and nothing overwritten.
`--agents` accepts a comma-separated list: `claude,codex,gemini,cursor,antigravity`;
only Claude needs the link. This works around Spec Kit 1.2.2 applying presets and
extensions only to the default integration. Keep Codex as the sole managed
integration rather than installing another integration to get its own copies.

## First feature

In your initialized project, invoke the named skills with your agent's command interface:

1. Run `speckit-constitution` for working rules. Run `speckit-baseline-amend` to
   create product, architecture and decisions memory; approve each proposed row.
   For existing code, `speckit-baseline-recover` proposes sourced rows first,
   distinguishing observed behavior from approved intent.
2. Run `speckit-specify` with `APP-142: Let members reset a forgotten password`.
   Context consults memory, picks full or light, resolves Focus, and retains
   conflicts through approved amendments. The upstream Git extension creates the
   branch; the branch hook applies the ticket/type (`feature/APP-142-reset-password`).
3. Run `speckit-clarify` until every material point is resolved or deferred.
   Run `speckit-plan`; resolve Delivery areas this feature first touches and
   choose concrete repository commands for Quality gates.
4. Run `speckit-tasks`, then `speckit-analyze`. Fix scope or consistency findings.
5. Run `speckit-implement` test-first. It runs every planned gate, records commands,
   exits and logs in verification.md, and invokes converge. Repair appended work
   until converged, then run the structural DONE check below.
6. After `converged`, converge sets `Completion: DONE`, checks DONE and automatically
   writes memory lessons. It checks its changes, then commits code, verification.md
   and memory together on the feature branch as one Conventional Commit. It asks
   before delivering through the Git & branching Delivery rule: push and open a PR,
   or merge locally into the target and delete the feature branch. If undecided,
   it asks which method and records your choice once. If you decline, it stops and
   gives commands for later. The feature folder number stays upstream's number
   even with a ticket branch. Branch protection, CI and deployment are never changed.

Small changes and bug fixes use the light path: state the approved behavior and
what stays unchanged, reproduce bugs where applicable, change and run relevant
gates. Do not create a full feature spec for process alone. Context applies branch
naming on an existing numbered branch; an unknown branch id requires user input.
The feature-record DONE check applies to the full path.

## Memory and focus

Memory lives beside upstream `.specify/memory/constitution.md`:

| File | Owns |
|---|---|
| constitution.md | How we work; refers to blocking Delivery rows as non-negotiable |
| product.md | Spirit, purpose, users, PR promises, non-goals, CAP capabilities with Serves PR citations, Q open questions |
| architecture.md | Stack, parts and boundaries, AR rules, interfaces, Delivery standards |
| decisions.md | D decisions, rationale, rejected options and reasons, supersession |

Context runs before specify and plan. It loads relevant entries, rejected choices
and linked contracts. Every request gets one focus verdict: `fits` names a user
and promise; `stretch` reduces or defers scope; `distraction` stops; `spirit change`
requires approved amendment first. A “do it anyway” is an accepted decision with
its reason, not silent drift. The spec retains `## Focus` with typed PR or override
D citations. Analyze checks that plan and tasks stay within that justified scope.

Delivery standards always retain 14 areas: git & branching, PRs & review,
environments, CI/CD, code quality, testing, documentation, issues & tasks,
release & versioning, security, database changes, observability, dependencies and
repository governance. Each is decided, undecided or n/a with a reason, with Rule,
Check and Blocking cells. Blocking rows alone hold non-negotiables. Resolve touched
undecided areas through amend. A decided applicable Check becomes a Quality gates
row automatically: `Gate`, `Command`, one concrete command in a code span per row.

After `converged` and `Completion: DONE`, write-back automatically applies new rows
and merges that extend an existing row without changing its meaning. This includes
capabilities with Serves, project-wide decisions from upstream research.md (with
rationale and alternatives), new architecture rules or parts and answered questions.
Every written row is tagged with its source feature. A contradiction is never
applied: a new Q-NNN in product.md cites both rows and the feature, leaving approved
intent intact and nothing waiting on you. Use amend to change meaning on purpose.

Memory is committed and often public. Write-back, amend, recover and context must
never write absolute or home paths, usernames, hostnames, IP addresses, internal
URLs, emails, private-service ports, credentials, tokens, keys, secrets or values
copied from `.env` / config files. Use generic descriptions such as `the database
host`; repo-relative paths are fine. A deterministic blocking check scans all four
memory files for sensitive path, IP, email, credential-URL and common secret shapes.
It cannot recognize every sensitive value; commands must also follow the instruction.
Write-back checks its own changes before commit, rewriting hits generically or
dropping the row; sensitive matches are never printed by the checker.

## Commands

The [command reference](docs/commands.md) describes every command: when to use it,
what it asks you, what it writes, what it never does and what it returns. It marks
which commands run by themselves as hooks and what upstream does before speckit-pro's
additions.

## Overrides of upstream behaviour

- Git extension configuration: `branch_template: "feature/{number}-{slug}"`,
  empty `branch_prefix` (so it cannot supersede the template), and
  `commit_style: conventional` in `.specify/extensions/git/git-config.yml`.
- The baseline after_specify hook renames only the current upstream-created branch
  for a requested type or ticket: `<type>/<id>-<short-name>`. Types are feature,
  fix, hotfix, refactor, docs, chore; id is the supplied ticket or spec number.
  It uses `git branch -m`, never changes upstream files or feature discovery state.
  Context explicitly calls it for light changes. The hook fallback avoids relying
  on support for wrapping extension commands.
- Commit subjects follow `<type>[optional scope]: <Description>`, at most 50
  characters, capitalized imperative description, no trailing period. Types:
  feat, fix, refactor, perf, test, docs, style, build, ci, ops, chore, revert.
  After a blank line, an optional body explains what and why, wrapped at 72
  characters; `Refs: APP-142` or `Refs: 007` matches the branch id.
- The installer selects Codex as the sole managed integration for standard skills
  in `.agents/skills/`; an optional Claude folder link shares that exact folder. This
  compensates for presets and extensions applying only to the default integration.
- Clarify overrides the total five-question cap with rounds. Behavior tests precede
  implementation, including where upstream treats them as optional. Converge uses
  the three outcomes above and writes only appended remediation tasks.

These are prompt rules unless described as script checks below. Install/upgrade
checks verify their composition; a real feature run verifies their interpretation.

## Structural checks and limits

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py
python3 .specify/extensions/baseline/scripts/baseline_check.py --done --feature specs/007-reset-password
```

Privacy hits block even in advisory mode. Memory checking validates IDs, typed citations, accepted governing decisions,
Spirit/non-goals, Focus citations and Delivery structure. Ordinary ID-like prose is
not a citation. Planned architecture paths need no code yet. Use `--mode advisory`
for recovery diagnostics; DONE remains blocking even in advisory mode.

DONE requires nonempty feature records, every task checked, all planned gates
matched by execution rows with exit 0 and existing local logs, no remaining gaps,
and a converged outcome. The checker reads records; it does not run gates or prove
log truth, freshness, coverage, scope, architectural correctness, branch/commit
semantics or approval. Analyze, converge and the user judge those meanings.

## Development and upstream upgrades

```sh
python3 -m unittest discover -s tests
sh scripts/check-install.sh 1.2.2
```

The first command is offline. The second requires network and uv; it creates a temp
project with that CLI version, initializes it, runs install.sh, and prints PASS/FAIL
for every shared wrap, the Claude folder link and matching content, baseline and Git
command, appended template, memory template, Git configuration, branch hook,
commit convention and checker invocation. It removes the scratch project afterward.
Validate real installation with this check and a first feature walk-through;
offline tests use a simulated CLI and cannot establish upstream composition.
The installation script checks composition, not the semantic quality of generated work.

For upgrades: bump SPECKIT_VERSION, run both checks, inspect each wrap/append and
**delete additions upstream now supplies**. See the [design note](docs/design-decisions-and-rationale.md).

Deferred until real use shows need: extra AS/TR IDs and a verification matrix,
optional modules (`admin-content`, `brand-assets`, `live-e2e`, `native-platforms`),
derived status views, more change-size paths and native
Windows installation. No attestation or task execution system is planned.
