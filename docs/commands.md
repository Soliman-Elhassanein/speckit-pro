# Command reference

Every command is an Agent Skill in `.agents/skills/`; invoke it by name with your agent's
command interface, for example `speckit-specify APP-142: Let members reset a forgotten password`.

speckit-pro adds five `speckit-baseline-*` commands and wraps eight upstream Spec Kit
commands with extra rules. A wrap keeps upstream's behaviour and adds rules before it, so
each wrapped entry below says briefly what upstream does and then what speckit-pro changes.
For upstream's full behaviour see [Spec Kit v1.2.2](https://github.com/github/spec-kit/tree/v1.2.2).

## At a glance

| Command | You run it | Runs by itself | Changes files |
|---|---|---|---|
| [speckit-constitution](#speckit-constitution) | Once, then when working rules change | — | constitution.md |
| [speckit-baseline-amend](#speckit-baseline-amend) | To create or change project memory | — | Memory, after your approval of each row |
| [speckit-baseline-recover](#speckit-baseline-recover) | For existing code, or code changed outside the process | — | None; it proposes |
| [speckit-baseline-context](#speckit-baseline-context) | Rarely | Before specify and plan | None |
| [speckit-specify](#speckit-specify) | To start a feature | — | spec.md, a feature branch |
| [speckit-baseline-branch](#speckit-baseline-branch) | On the light path, when context asks | After specify | Branch name only |
| [speckit-clarify](#speckit-clarify) | After specify | — | spec.md |
| [speckit-plan](#speckit-plan) | After clarify | — | plan.md, design files, verification.md |
| [speckit-tasks](#speckit-tasks) | After plan | — | tasks.md |
| [speckit-analyze](#speckit-analyze) | After tasks | — | None |
| [speckit-implement](#speckit-implement) | After analyze | — | Code, tests, tasks.md, verification.md |
| [speckit-converge](#speckit-converge) | Rarely | Called by implement | tasks.md, verification.md, memory, one commit |
| [speckit-baseline-check](#speckit-baseline-check) | Any time | After plan, implement and converge; before analyze and implement | None |

Hooks run only when your agent follows Spec Kit's hook instructions; upstream sets
`auto_execute_hooks: true`. A failing required check stops the command that triggered it.

Memory means the four files in `.specify/memory/`: `constitution.md` (how we work),
`product.md` (what), `architecture.md` (how it is built) and `decisions.md` (why).
A feature's records live in its upstream folder, for example `specs/007-reset-password/`.

## Project memory

### speckit-baseline-amend

The only command that intentionally changes what memory means.

- **Use it** to create memory for a new project, record a decision, or apply proposals
  from recover, a report, a decision record or a finished feature folder.
- **You give** the proposal: in conversation, a file path or a feature folder.
- **It asks you** to approve each proposed row. It shows exact old and new values,
  evidence paths and conflicting sources, and asks only blocking questions; the rest
  become open questions.
- **It writes** approved rows only, with new IDs (`CAP-`, `PR-`, `AR-`, `D-`, `Q-`, at
  least three digits, never renumbered), a version bump per changed file and a Last
  amended date. Replaced decisions stay, marked `superseded by D-NNN`.
- **It never** treats input as approved because it says so, invents missing reasons,
  writes private values (paths, hosts, emails, secrets) or changes Spirit without your
  explicit approval.
- **Result:** the changed files, versions, rows and the output of the memory check.

### speckit-baseline-recover

Proposes memory from what the code actually does.

- **Use it** when a project has code but no memory, or when code changed outside the
  process.
- **You give** optionally the areas to look at.
- **It reads** code, tests, docs, manifests, CI and deployment files, plus existing memory.
- **It writes** nothing. It produces a proposal that keeps **observed behaviour** apart
  from **approved intent**, with evidence for every row. Unknown reasons become open
  questions. With existing memory it lists drift and conflicts and offers fixing the
  code as an alternative.
- **Next:** pass the proposal to `speckit-baseline-amend` to approve it row by row.

### speckit-baseline-context

Loads the right memory before specify and plan and decides how much process a request needs.

- **Runs by itself** before `speckit-specify` and `speckit-plan`.
- **It chooses** one path. **Full** for features: specify, clarify, plan, tasks, analyze,
  implement, converge. **Light** for small changes and bug fixes: name the approved
  behaviour and what stays unchanged, reproduce a bug with a failing test, change the
  code and run the relevant gates. On the light path it stops the specify or plan flow
  and applies branch naming instead.
- **It gives** one focus verdict per request:

  | Verdict | What happens |
  |---|---|
  | fits | Names the user and the promise it serves; work continues. |
  | stretch | Proposes a smaller version or deferral; you decide before work continues. |
  | distraction | Stops and says which non-goal or missing promise it hits. |
  | spirit change | Stops until you approve a Spirit amendment through amend. |

- **It asks you** about conflicts, duplicates, rejected options being revived, and each
  undecided Delivery area the feature touches first. Before plan it labels architecture
  impact `none`, `extends` or `changes`; the last two need your choice.
- **It hands** the Focus section to specify and the architecture citation lines to plan.
  "Do it anyway" is recorded as an accepted decision with its reason.
- **It writes** nothing; your answers are kept through amend.

### speckit-baseline-branch

Renames the branch upstream created to `<type>/<id>-<short-name>`, for example
`feature/APP-142-reset-password`.

- **Runs by itself** after `speckit-specify`. Context also calls it on the light path.
- **Type** is `feature` by default, or `fix`, `hotfix`, `refactor`, `docs`, `chore` from the
  request; a type you state wins. **Id** is the ticket you supply, otherwise upstream's
  spec number.
- **It never** creates a branch, renames main, master or a detached HEAD, overwrites an
  existing branch, or changes the feature folder or its number.
- **It asks you** for an id when a light change has none.
- **Then** it runs the memory check for the feature.

### speckit-baseline-check

A read-only script that checks structure, not meaning.

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py                    # all memory and features
python3 .specify/extensions/baseline/scripts/baseline_check.py --feature specs/007-reset-password
python3 .specify/extensions/baseline/scripts/baseline_check.py --mode advisory    # recovery diagnostics
python3 .specify/extensions/baseline/scripts/baseline_check.py --done --feature specs/007-reset-password
```

- **It checks** unique valid IDs, citations that resolve, accepted governing decisions,
  Spirit with non-goals, a Focus section in every spec, capabilities that cite a promise,
  and all 14 Delivery areas. It scans the four memory files for private values; those
  hits block even in advisory mode and are never printed.
- **`--done`** also requires every task checked, every planned gate recorded with exit 0
  and an existing local log, no remaining gaps and a converged outcome.
- **It never** runs gates, writes files or judges whether tests, architecture or a
  convergence conclusion are right. Analyze, converge and you judge those.

## Feature flow

### speckit-constitution

- **Upstream** creates or updates `.specify/memory/constitution.md` from your principles.
- **speckit-pro** keeps only how-we-work rules there. Product spirit, users, promises and
  non-goals go to `product.md` through amend. Non-negotiables live only in the blocking
  rows of the Delivery standards table in `architecture.md`; the constitution refers to them.

### speckit-specify

- **Upstream** writes `spec.md` in a new numbered feature folder from your description,
  with FR and SC requirement IDs. The Git extension creates the feature branch first.
- **speckit-pro** runs context first and copies its resolved `## Focus` into the spec:
  verdict, named user, reason and the promise (`**Promises**: PR-NNN`) or accepted
  override (`**Override**: D-NNN`). It keeps the `**Implements**` and `**Product rules**`
  lines. It stops on an unresolved stretch, distraction or spirit change. Updated specs
  keep their requirement IDs; new ones go above the highest.
- **Then** branch naming runs.

### speckit-clarify

- **Upstream** asks up to five targeted questions in total and writes answers into the spec.
- **speckit-pro** removes the total cap: it asks in rounds of up to five, one question at a
  time, and rescans until every material point (behaviour, acceptance, security, scope or
  verification) is resolved or explicitly deferred. It skips points memory already
  settles, writes each answer into the spec at once, and records what deferred points
  block. Project-wide questions are proposed through amend.

### speckit-plan

- **Upstream** writes `plan.md`, `research.md`, `data-model.md`, `contracts/` and
  `quickstart.md`.
- **speckit-pro** runs context first and keeps its architecture lines and the Focus scope.
  The plan gets a `## Quality gates` table (`Gate`, `Command`) with one real command per
  row, runnable from the repository root. Every decided Delivery Check that applies is
  added automatically; undecided areas the feature touches are resolved through amend.
  It creates `verification.md` with each gate marked NOT RUN and Completion NOT DONE.
- **Then** the memory check runs on the plan's citations.

### speckit-tasks

- **Upstream** writes a dependency-ordered `tasks.md` in phases; `[P]` marks tasks that
  may run in parallel.
- **speckit-pro** requires behaviour tests before implementation, even where upstream
  calls them optional, and traces tasks to spec requirements. `[P]` only marks tasks that
  touch different files, share no state and wait for no other task of their phase; when
  in doubt it is left off. Every phase ends with all Quality gates passing. The last phase
  is `## Phase N: Verification and convergence`. Existing IDs, text, order and ticks are kept.

### speckit-analyze

- **Upstream** reports inconsistencies across spec, plan and tasks without changing files.
- **speckit-pro** also compares them with cited promises, capabilities, decisions,
  architecture rules and part boundaries, and reports anything that grows beyond the
  Focus scope, with its location. It recommends reducing scope or an approved amendment;
  it never invents approval. The memory check runs first.

### speckit-implement

- **Upstream** works through `tasks.md` phase by phase and ticks finished tasks.
- **speckit-pro** works test-first: a failing behaviour test, then the code, then a rerun.
  A task is ticked only after its validation and the phase gates pass. Afterwards it
  runs every Quality gates command and records the exact command, exit code and local
  log path in `verification.md`. It then runs converge and repairs until converged.
  It never weakens a check to pass, and leaves the commit and delivery to converge.
- **Commits** use Conventional Commits with a `Refs: APP-142` or `Refs: 007` footer.

### speckit-converge

- **Upstream** compares the code with spec, plan and tasks and appends unbuilt work as new
  tasks.
- **speckit-pro** also checks architecture rules, boundaries, accepted decisions and
  blocking Delivery standards, and reads test assertions rather than names or ticks.
  It only appends deduplicated remediation and never edits old tasks. It returns exactly
  one outcome:

  | Outcome | Meaning |
  |---|---|
  | `tasks_appended` | New remediation tasks were added; go back to implement. |
  | `gaps_remaining` | No new tasks, but open work or verification gaps remain: NOT DONE. |
  | `converged` | No gaps, every gate passes and every task is checked. |

- **After `converged`** it sets `Completion: DONE`, runs the `--done` check and writes
  lessons to memory without asking: new rows go in, rows that only extend existing ones
  are merged, and contradictions become a new open question instead of changing approved
  rows. It checks those changes, then makes one Conventional Commit of code,
  `verification.md` and memory on the feature branch.
- **It asks you** before delivery, following the Git & branching Delivery row: push and
  open a pull request, or merge locally and delete the branch. If that row is undecided
  it asks which method and records your answer. If you decline, it stops and prints the
  commands for later. It never changes branch protection, CI or deployment.

## Unchanged upstream commands

speckit-pro does not wrap these; they behave as upstream documents them.

| Command | What it does |
|---|---|
| speckit-checklist | Writes a custom requirements-quality checklist to the feature's `checklists/` folder. |
| speckit-taskstoissues | Deprecated upstream: turns tasks into GitHub issues. |
| speckit-git-feature | Creates the feature branch; runs by itself before specify. speckit-pro sets its template to `feature/{number}-{slug}`. |
| speckit-git-initialize | Creates a Git repository with a first commit; runs by itself before constitution. |
| speckit-git-commit | Optional commits around commands; off unless `auto_commit` is enabled in `.specify/extensions/git/git-config.yml`. |
| speckit-git-validate | Checks the current branch name against the naming convention. |
| speckit-git-remote | Reports the remote URL and whether it is on GitHub. |
