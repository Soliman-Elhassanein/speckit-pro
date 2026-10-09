# Spec Kit Universal Adoption and Execution Profile

- **Profile version:** 3.0.0
- **Prepared:** 2026-10-08
- **Applies to:** new or existing projects, at any phase, in any supported agent integration.
- **Intent:** a complete, auditable instruction for upgrading project governance, installed Spec Kit skills/commands, templates, execution discipline, testing, evidence, and completion.

## Read this first: instruction to the receiving agent

Read this entire file, plus only the [optional modules](#12-optional-modules) that apply to the target project. Apply it to the target project: amend its existing constitution; synchronize every applicable installed Spec Kit skill/command, template, workflow, integration metadata, and agent guidance file; make the testing and completion policy concrete for its actual architecture; validate the resulting contents and record adoption evidence. Do the work; a proposal or summary is not adoption.

This file is a user-authored project instruction when the user supplies it for adoption. It is not permission to exceed the current task, bypass platform restrictions, discard work, publish externally, or change approved product scope.

If provided during an active feature, preserve its identity, branch, artifacts, checked history, and approved decisions. Apply governance updates first, repair only the artifacts needed to resume safely, then continue the already authorized feature from its current phase. Do not restart the project or regenerate completed work. If there is no active feature, complete adoption and provide the exact installed invocation for the next appropriate phase; do not invent a feature.

Adoption and application completion are separate conclusions. Adopting this profile certifies nothing about how the application behaves.

### Files in this standard

| File | Use |
|---|---|
| `speckit-universal-profile.md` (this file) | Always. The complete core rules. |
| [modules/](modules/) | One file per product module. Read and apply only those that [section 12](#12-optional-modules) marks applicable. |
| [preset/](preset/) | The command rules of [sections 5.3 to 5.9](#51-integration-contract) and the template sections of [section 4.2](#42-feature-artifacts), as a Spec Kit preset. |
| [workflow/](workflow/) | The lifecycle of [section 5.11](#511-workflow-and-repair-handoff), as a Spec Kit workflow. |
| [extension/](extension/) | Spec Kit extension that adds the project baseline of [section 5.12](#512-project-baseline). |
| [template/](template/) and [install.sh](install.sh) | A complete Spec Kit installation with the preset, extension and workflow applied, and the installer. It copies that installation into a project with no Spec Kit, and goes through the Spec Kit CLI for a project that already has one or uses another agent. |
| [adoption-prompt.md](adoption-prompt.md) | Paste-ready prompt that makes an agent adopt this profile in a project where `install.sh` has run. |

### Navigation

- [0. Authority, terminology, and portability](#0-authority-terminology-and-portability)
- [1. Discover and enter at the current phase](#1-discover-and-enter-at-the-current-phase)
- [2. Apply an idempotent adoption transaction](#2-apply-an-idempotent-adoption-transaction)
- [3. Amend the constitution](#3-amend-the-constitution)
- [4. Stable identities and artifact contracts](#4-stable-identities-and-artifact-contracts)
- [5. Synchronize skills, commands, integrations, and workflows](#5-synchronize-skills-commands-integrations-and-workflows)
- [6. Testing policy](#6-testing-policy)
- [7. Verification evidence](#7-verification-evidence)
- [8. Completion and convergence](#8-completion-and-convergence)
- [9. Execution and engineering discipline](#9-execution-and-engineering-discipline)
- [10. Local version control](#10-local-version-control)
- [11. Safe migration and upgrades](#11-safe-migration-and-upgrades)
- [12. Optional modules](#12-optional-modules)
- [13. Adoption audit and validation](#13-adoption-audit-and-validation)
- [14. Reusable invocation and reporting](#14-reusable-invocation-and-reporting)

## 0. Authority, terminology, and portability

1. MUST means a required rule. SHOULD means follow it unless a concrete reason is recorded. MAY means optional. A rule conditional on a module applies only if that module exists in the target product.
2. Obey the environment's instruction hierarchy and current user authorization. Resolve conflicts explicitly. This profile must not override higher-priority instructions or imply that the agent can grant itself capabilities. Preserve established repository rules unless an authorized amendment changes them.
3. Read existing instructions and inspect evidence before editing. Distinguish approved requirements, inferred assumptions, historical records, and current observations. User assertions and old documents are inputs to verify, not automatic proof.
4. Resolve every concrete choice from the target repository and approved intent: product, language, framework, roles, locales, formats, directory structure, hardware, tool versions, and thresholds. Examples in this profile and its modules are illustrative, never defaults.
5. Universal obligations cannot be dismissed as N/A: truthful execution, stable history, simplicity, search-first reuse, meaningful verification, reproducibility, secrets protection, safe local version control, and engineering discipline. Product modules may be N/A only with a concrete reason. A universal rule with unavailable prerequisites is BLOCKED, not N/A.
6. Keep governance under repository control. Prefer a durable path outside generated integration directories, such as `docs/speckit-universal-profile.md`. Use existing equivalent documentation locations when the project has them; record actual paths in the adoption report.
7. This profile's default completion model is locally authoritative. External boards, repository hosts, cloud previews, reviews, automation, synchronization, and artifact uploads are not prerequisites for feature or policy completion. Preserve genuine product dependencies, such as a payment provider or delivery service; a mocked dependency cannot certify live behavior that the specification promises.
8. User-required publishing or deployment is a separate authorized deliverable. Test it when it is part of the request. Do not silently add an external service to a local completion gate.
9. Do not install optional frameworks, BDD extensions, hooks, validators, remote services, new applications, or infrastructure merely to appear advanced. Add only what an active requirement and authorization justify.

## 1. Discover and enter at the current phase

### 1.1 Inspect and resolve project context

Inspect repository instructions, Git status and branch, Spec Kit version and installation provenance, constitution, templates, all active integrations, workflows, manifests, relevant code, architecture, test configuration, operational documentation, and current feature evidence. Do not infer installation health from filenames alone.

Record the following in `docs/spec-kit-adoption.md`, or the documented equivalent:

| Context | Required resolution |
|---|---|
| Product and scope | Purpose, current request, approved non-goals, active feature(s), superseded work |
| Layers and ownership | Authoritative data, authentication, authorization, invariants, contracts, consumers, trust boundaries |
| Actors | End users, operators/administrators, exceptional users, service accounts, ownership and scopes |
| Interfaces | Official user/operator surfaces, APIs, CLI/library contracts, existing navigation |
| Locale and accessibility | Languages, directionality, accessibility baseline, target capabilities |
| Data policy | Retention, archive, deletion, external content exceptions, correction/audit rules |
| Technology and dependencies | Manifests, locks, immutable container pins, toolchain versions, supported platforms |
| Quality gates | Exact full commands, working directories, prerequisites, expected warning policy |
| Test environments | Local services, fixtures, browsers, devices/emulators, runtime capabilities, resource budgets |
| Public contracts | Canonical API/schema/library documentation and compatibility policy |
| Agent integration | Actual skill/command paths, frontmatter/schema, workflow/hook files, generated vs local source |
| Version control | Current/default branch, unrelated user changes, safe staging policy, local identity |
| Evidence | Repository-owned evidence paths, retention/sanitization, fingerprint method, existing runs |
| Applicable modules | Which [optional modules](#12-optional-modules) apply, and the concrete reason each other one is N/A |

Use unambiguous repository evidence to answer routine questions. Ask only for decisions that materially change behavior, architecture, security, scope, or verification. Do independent work while a real blocker is unresolved. Never silently convert an unresolved product decision into an implementation assumption.

### 1.2 Start from the phase that exists

| Current state | Required entry and next action |
|---|---|
| Spec Kit absent | Inspect installed CLI/help and supported integration; initialize through its supported path without overwriting work. Record prerequisite status. This profile does not replace initialization. |
| Initialized, no constitution | Establish concrete governance before feature work. |
| Constitution or workflow exists | Amend in place and synchronize dependents; preserve dates and history. |
| Idea/specification | Preserve existing intent and IDs; add missing acceptance/verification definitions, then clarify material gaps. |
| Planning | Reconcile the current spec, perform Constitution Checks, add reuse inventory, test methods, exact gates, prerequisites, and planned NOT RUN evidence. |
| Tasks generated | Audit existing IDs/dependencies; append missing traceable tests, reuse work, gates, evidence, and convergence tasks. |
| Implementation in progress | Establish the current baseline and inspect artifacts together; continue authorized tasks after resolving critical contradictions. |
| Verification underway | Audit assertions and freshness; run missing focused/full checks on the final state and record outcomes. |
| Claimed complete or legacy feature | Analyze and converge first; preserve historical checks; append remediation for unsupported claims. |
| Defect or update to existing behavior | Preserve approved intent; identify the reproduced symptom, affected FR/AS/TR, cause, minimal repair, and regression scope. Amend intent only if the user actually approves changed behavior. |
| Superseded feature | Keep historical; identify its replacement. Do not reactivate it during a broad audit. |

Phase entry does not require mechanically rerunning every earlier step. Repair missing prerequisites and inconsistent artifacts, then proceed from the correct phase. A narrow request must retain its narrow scope; report feature-wide completion separately.

### 1.3 Record decisions and impact

For material changes, record the decision, repository evidence, alternatives that matter, approved outcome, affected artifacts, and verification consequences in existing research/plan records. Use a small decision record only if no equivalent exists. Do not create a second competing source of truth.

## 2. Apply an idempotent adoption transaction

1. Read this file and the applicable modules. Inspect all affected existing files before changing them.
2. Establish the existing state: Git status, constitution version/dates, current phase, integration health, configured quality gates, historical evidence. Record pre-existing failures without claiming responsibility or silently waiving them.
3. Map each numbered section/subsection and every applicable MUST obligation to actual files and a validation method. No applicable rule may disappear into an overall coverage percentage.
4. Amend the constitution and then synchronize templates, every installed active integration, workflows, runtime guidance, verification policy, local task conventions, and applicable operational guides. Preserve integration-specific syntax and schemas.
5. Update active feature artifacts only as needed for safe continuation. Do not mass-regenerate legacy specs, destroy checkboxes, reset evidence, or reactivate superseded scope.
6. Validate file contents, consistency, parsing/schema, internal links, placeholders, workflow resolution, and authoritative gate invocability. Run the checks appropriate to the changed files; policy-only validation cannot certify runtime behavior.
7. Review, stage, and commit under [section 10](#10-local-version-control).
8. Record per-rule adoption evidence and unresolved gaps. Report ADOPTED only under [section 13](#133-validation-methods-and-completion-gate)'s gate. Otherwise report PARTIAL with exact FAIL/BLOCKED rows.
9. Resume the already authorized active phase, or print the exact installed next invocation when no feature execution is authorized.
10. On repeated application, compare existing behavior with this profile and patch only genuine drift. Preserve equivalent implementations, IDs, dates, history, and file ownership. Do not create a version bump or duplicate task because the prompt was provided again. A second pass with no substantive drift must produce no semantic changes.

Do not stop after editing only the constitution or testing guide. Adoption requires synchronized operative skills/commands and templates, not merely a document describing desired behavior.

## 3. Amend the constitution

Use the installed constitution skill/command where available. Update the existing constitution in place. Preserve original ratification, record the actual amendment date, justify semantic versioning, and prepend a Sync Impact Report covering old/new version, changed/added/removed principles, synchronized files, pending work, and conflicts. Major bumps are for incompatible governance changes; minor for added/materially expanded governance; patch for clarifications without changed obligations.

Validate declarative MUST language, headings, dates, placeholders, consistency, and propagation to every operative dependency. There must be no unexplained constitution placeholders. Deliberately reusable template placeholders must be documented; concrete runtime guidance must resolve them.

### 3.1 Authoritative ownership and contract-first sequencing

- Assign one authoritative owner for each data shape, authentication decision, authorization rule, and business invariant. Define audiences, layer responsibility, dependency direction, and trust boundaries.
- Sequence cross-layer work from provider/authoritative contract toward consumers. Keep different trust audiences separate unless a validated design justifies combination.
- Change public contracts, examples, and behavior in the same coherent unit. Define compatibility or migration when a contract changes.
- Keep mocks behind replaceable boundaries; replacing a mock with the real dependency must not require rewriting consumers. Record what a mocked test cannot establish.

### 3.2 Authorization at the trusted boundary

- Every state-changing path must make an explicit authorization decision at the authoritative component. Hidden controls alone are not enforcement.
- Specify roles, scopes, ownership, inactive/revoked/stale behavior, and exceptional authority.
- Exercise allowed and relevant refused paths through the actual exposed API, form, action, CLI, or public entry point. Assert both the response and absence of unauthorized side effects.
- For non-server software, identify what can actually enforce the rule and the limits of that trust model. Do not invent server security for a client-only product.

### 3.3 Accessible, localized, task-oriented interfaces

- Resolve supported locale(s), directionality, platforms, accessibility baseline, and intended user capabilities.
- Require understandable task labels, visible state, sufficient contrast/targets, shallow navigation, keyboard/screen-reader behavior where relevant, and explicit loading, empty, error, retry, and recovery states.
- Validate promised layout/usability using rendered screens and the appropriate browser, simulator, physical device, accessibility tool, or operator walkthrough.
- String existence or screenshot-text matching alone does not prove dimensions, target size, focus behavior, text-direction layout, or accessibility. Use measurements and interactions relevant to the acceptance claim.

### 3.4 Data preservation, deletion, and exceptions

- Define immutable, archived, soft-deleted, hard-deletable, and retention-governed data, including correction and audit history. These are product decisions; soft deletion is not a universal default.
- Define shared-content ownership, visibility after removal, and restoration authority where the product has shared content.
- Identify external content outside local preservation guarantees, visibly label the limitation wherever it is presented, and retain local references according to policy.
- Keep exceptions narrow, explicit, derived where possible, and testable. Apply this principle to user, historical, shared, or regulated records; otherwise record why it is N/A.

### 3.5 Simplicity and explicit non-goals

- Preserve approved non-goals and settled decisions. Build the smallest complete architecture for the active requirement.
- Do not create speculative services, framework layers, future clients, or parallel applications.
- Add dependencies or infrastructure only for a current requirement; prefer the standard library or an existing dependency when sufficient.
- Record justified constitutional exceptions in plan Complexity Tracking, with rationale, impact, and verification. An exception cannot silently remove security or completion gates.

### 3.6 Mandatory DRY and reusable design

- Shared domain knowledge, validation, authorization, configuration, transformations, and UI behavior require one authoritative implementation. Search for existing helpers, services, components, policies, validators, serializers, fixtures, hooks, and utilities before adding code.
- Reuse or extend matching contracts. If shared behavior is duplicated, extract a small cohesive component with a stable interface and direct tests. Prefer composition to copied large implementations.
- Centralize security/business invariants so alternate write paths cannot maintain independent rules.
- Parameterize only observed variation. Similar syntax with different domain semantics must remain separate; explain intentional semantic duplication in the plan/review.
- Preserve layer ownership and dependency direction. Avoid circular dependencies and moving enforcement into an untrusted client.
- Refactors must preserve behavior and pass affected regressions. Reusable UI must expose needed variants, share theme tokens, and retain accessibility/localization.

### 3.7 Verification before completion

Adopt [sections 6–8](#6-testing-policy) as a constitutional principle: no story or feature is DONE without current, meaningful, passing verification of every FR and AS.

### 3.8 Reproducibility, configuration, and secrets

- Commit synchronized dependency manifests and locks in the same change; install exact locked versions for repeatable gates rather than re-resolving ranges.
- Pin tools explicitly and containers by immutable digest. Resolve compatible pins for the target project.
- Document one supported way to run each complete gate and equivalent dependency inputs across supported local environments.
- Keep credentials, signing keys, tokens, tracked secret-bearing `.env` files, personal data, and unrestricted dumps out of commits and retained evidence.
- Document configuration variable names and safe examples without secret values. Use environment variables or approved credential helpers.

### 3.9 Module principles

For each applicable [optional module](#12-optional-modules), add the governance rules that module defines, such as scoped operator administration. Record each inapplicable module as N/A with its concrete reason rather than inventing the capability.

### 3.10 Repository-wide engineering obligations

Include [sections 9–11](#9-execution-and-engineering-discipline) in governance and runtime guidance. Do not drop them because they are not acceptance-test instructions.

## 4. Stable identities and artifact contracts

### 4.1 Identity

| Identifier | Meaning | Cross-feature reference |
|---|---|---|
| `FR-001` | Functional requirement | `<feature-number>/FR-001` |
| `AS-001` | Acceptance scenario, unique within the whole feature | `<feature-number>/AS-001` |
| `TR-001` | Test requirement | `<feature-number>/TR-001` |
| `SC-001` | Measurable success criterion | `<feature-number>/SC-001` |
| `T001` | Task, local to its feature's tasks file | `[NNN] T001: <description>` |
| `CHK001` | Requirements-quality checklist item | Qualify with owning feature/checklist when needed |

Each feature may restart task numbering at T001. Bare task IDs are valid inside the owning tasks file; use `[NNN] TXXX` in commits, cross-feature artifacts, verification, and reports. Preserve suffixes and legacy IDs, such as `FR-001a` or `US1/AC2`, with stable aliases. Never silently renumber. Append above the current maximum, respecting the existing numbering convention. Preserve checked history, approved decisions, dependencies, and supersession whenever an artifact is updated.

### 4.2 Feature artifacts

Use the target's actual feature layout, ordinarily `specs/NNN-feature/`. Core artifacts are `spec.md`, `plan.md`, `tasks.md`, `verification.md`, and requirements-quality `checklists/`. Add `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` when their purpose applies. Do not create empty ceremonial artifacts.

| Artifact | Mandatory content and boundary |
|---|---|
| `spec.md` | Prioritized independently testable stories; stable FR/AS/TR/SC; edge cases; assumptions/dependencies; full FR/AS-to-TR matrix; measurable expected outcomes; binary completion gate. Keep implementation-agnostic. Classify SCs as release gates or post-launch measurements; do not invent future results. |
| `plan.md` | Real paths and boundaries; Constitution Check before/after design; reuse inventory and authoritative homes; prerequisites, fixtures, layers, selectors/commands, performance conditions, regressions, browser/device/manual evidence, and each TR's implementation location. Initialize or preserve planned verification as NOT RUN. |
| `tasks.md` | Dependency-ordered work grouped by story; tests, reuse search/extraction, implementation, focused verification/repair, related regression, final complete gates, evidence reconciliation, convergence, documentation, and coherent commits. Map test/verification work to FR/AS/TR and paths/selectors. |
| `checklists/*.md` | Completeness, clarity, consistency, measurability, and scenario coverage of written requirements. Append unique CHK IDs. They must not assert runtime behavior such as “API returns 200” or “button works.” |
| `verification.md` | The record defined in [section 7](#7-verification-evidence). Distinguish planned from executed and old from current. |
| `quickstart.md` | Reproducible setup, commands, acceptance walkthroughs, expected observations, diagnosis, evidence, and safe teardown. A document is not proof its walkthrough ran. |
| Research/data/contracts | Resolve design questions, authoritative schemas/invariants, and exposed interfaces without duplicating competing definitions. |

Task sequencing is acceptance/behavior tests → supporting tests → implementation → focused verification/repair → related regressions. Final verification reconciles all mappings and release SCs. Tests are mandatory; `[P]` or parallel markers are allowed only for truly independent work with no conflicting files, state, service, device, or resource dependencies.

### 4.3 Verification-matrix template

```markdown
| FR | AS | TR | Observable assertion | Layer / interface | Planned selector or method | Release SC |
|----|----|----|----------------------|-------------------|----------------------------|------------|
| FR-001 | AS-001 | TR-001 | <expected state/result, including side effects> | <smallest adequate layer> | <concrete test selector/observation> | <SC or explicit none> |
```

Read assertions when auditing coverage. A matching marker, test name, or matrix row is traceability, not proof of adequacy or execution.

## 5. Synchronize skills, commands, integrations, and workflows

### 5.1 Integration contract

- Work with the integration the project already uses. Do not install, add, or switch an agent integration, or create another agent's directory, unless the user asks for it.
- Discover all actual active integration paths and invocation forms. Dotted slash commands, hyphenated skills, `$skill` mentions, and shell CLI subcommands are not interchangeable. Verify installed help/schema rather than assuming a version. Official Spec Kit distinguishes agentic invocations from CLI operations; see its [Quickstart](https://github.github.com/spec-kit/quickstart.html) and [Extensions reference](https://github.github.com/spec-kit/reference/extensions.html).
- Amend every applicable active skill/command and its authoritative source template so regeneration does not restore weaker behavior. Prefer the installation's supported customization mechanism, such as a preset, over hand-editing generated files. Preserve frontmatter, required fields, invocation syntax, argument handling, feature-selection controls, provenance, and compatibility.
- Synchronize root and layer agent guidance (`AGENTS.md`, `CLAUDE.md`, or equivalents) and feature templates. Concrete runtime guidance must name actual commands and working directories.
- Inspect reusable workflow definitions, hooks, manifests, declared versions and hashes. Recompute managed metadata only through the installation's supported ownership/update process after content validation; do not rewrite integrity data merely to hide unexpected changes.
- Validate parser/schema, required files, actual registration, workflow resolution, and managed checksums where applicable. Distinguish an expected documented customization warning from a real missing/invalid integration.
- If a required capability is absent, use the supported local customization/installation mechanism within authorization, or provide the exact equivalent agent instruction and record the blocker. Do not falsely claim that a native command exists or is installed.
- Retain authorized optional external integrations, such as task conversion, without making them gates; retire active dependencies on them where they conflict with the locally authoritative model. Preserve historical links as provenance.

This standard ships its own rules for specify, clarify, plan, tasks, analyze, implement and converge as the preset in [preset/](preset/). The preset wraps each stock command with the rules, adds the sections of [section 4.2](#42-feature-artifacts) to the spec, plan and tasks templates, and adds the `verification-template` of [section 7.3](#73-required-verification-template). Install it from the target project root with `specify preset add --dev <path-to-this-standard>/preset`. Where it is installed, do not also copy the rules into the skills by hand.

### 5.2 `speckit-constitution`

Follow the amendment procedure in [section 3](#3-amend-the-constitution). Propagate to all templates, active skills/commands, runtime guidance, workflows, and affected docs. Commit the coherent governance unit.

### 5.3 `speckit-specify`

Create from the spec template only when the spec is absent. Updates preserve approved intent and the identity rules of [section 4.1](#41-identity). Produce the `spec.md` contract of [section 4.2](#42-feature-artifacts).

### 5.4 `speckit-clarify`

Ask high-impact questions one at a time, in rounds of up to five, using repository-grounded recommendations. There is no cap on the number of rounds: continue until every material point is resolved or the user defers what is left. Integrate each accepted answer immediately, remove contradictions, and reevaluate requirements quality. Clarify behavior and acceptance, not minor implementation preferences. Preserve settled answers, record resulting verification changes, and record each deferred point with what it blocks.

### 5.5 `speckit-plan`

Run Constitution Checks before and after design. Produce the `plan.md` contract of [section 4.2](#42-feature-artifacts): plan every FR/AS through TRs at the smallest adequate layer, including the real interface where the promise is made. Identify reuse candidates and authoritative shared invariants; explain intentional duplication.

### 5.6 `speckit-tasks`

Produce the `tasks.md` contract and ordering of [section 4.2](#42-feature-artifacts), mapping every FR/AS through TR to concrete work. No story-completion task may lack required behavioral coverage.

### 5.7 `speckit-analyze`

Remain read-only: no application, spec, task, evidence, or report-file mutations under this invocation. Compare constitution/spec/plan/tasks and current evidence. Independently report FR, AS, TR, and task coverage, plus release SC and platform evidence where applicable. Inspect meaningful assertions and actual interfaces, not just IDs. Flag duplicated invariants, unnecessary parallel components, ignored reuse opportunities, and critical missing mappings. Distinguish planned NOT RUN from false/stale completion. Report needed decisions without modifying files.

### 5.8 `speckit-implement`

Read intent, design, tasks, and evidence together. Establish the baseline, search for reuse, and run the loop of [section 6.2](#62-test-first-implementation-and-regression). Continue independent in-scope work around a real blocker. Check a task only when its applicable validation passes. Run the final relevant full gates, record current evidence, then invoke convergence and repair in scope until clean or genuinely blocked.

### 5.9 `speckit-converge`

Converge compares current implementation, meaningful assertions, and current evidence against spec/plan/tasks. Its only allowed file mutation is appending deduplicated remediation tasks to `tasks.md`, and it reports exactly one of `tasks_appended`, `gaps_remaining`, or `converged`. No new tasks is not equivalent to converged.

The complete rules are shipped once, in [preset/commands/speckit.converge.md](preset/commands/speckit.converge.md). The preset installs them with the other commands. The script below adds the converge rules alone, for an integration the preset does not reach:

```sh
# generic integration with a custom commands directory, such as .agent/commands
sh <path-to-this-standard>/preset/apply-converge.sh .agent/commands/speckit.converge.md

# built-in integrations
specify preset add --dev <path-to-this-standard>/preset
```

The script inserts the rules into the installed Markdown command and is safe to run again; `specify integration status` then reports that file as a modified managed file, which is the expected customization. Both routes were re-verified on specify-cli 1.1.2. Preset 2.0.0, which held only converge, was verified on specify-cli 0.13.3 with the Claude, Codex (skills), Gemini, Copilot, OpenCode, and Cursor integrations. Preset 2.1.0 and later need specify-cli 1.1.0 or later and were verified on 1.1.2 with the Codex (skills) and Claude layouts. The preset does not reach the `generic` integration. Removing the preset deletes the composed command; restore the stock one with `specify integration upgrade <integration>`.

### 5.10 `speckit-checklist`

Validate written requirements only, under the `checklists/*.md` contract of [section 4.2](#42-feature-artifacts). Preserve existing checklists and never represent checklist completion as runtime proof.

### 5.11 Workflow and repair handoff

The lifecycle is specify → review/clarify → plan → review → tasks → analyze → implement → verify → converge. Existing-feature entry follows [section 1.2](#12-start-from-the-phase-that-exists). When verification fails or convergence finds work, return to implementation, rerun affected/full verification, and converge again.

The lifecycle is shipped as the workflow in [workflow/](workflow/), installed with `specify workflow add --dev <path-to-this-standard>/workflow` and run as `speckit-pro`. It is linear with review gates, and it runs the baseline check as a step before implement, so that gate does not depend on an agent following a prompt. It does not repeat the repair loop on its own.

If the workflow engine cannot express a repair loop, stop with an honest NOT DONE result and print the exact supported implement/verify/converge invocations and feature selection. Do not declare success simply because implementation ended. Preserve the same feature directory; use `SPECIFY_FEATURE_DIRECTORY` only if supported by that installation, otherwise its verified selection mechanism.

### 5.12 Project baseline

New projects keep four kinds of project memory, each the one home for its kind of fact:

| File | Holds |
|---|---|
| `.specify/memory/constitution.md` | Rules: how we work |
| `.specify/memory/product.md` | What: one row per capability, with its state |
| `.specify/memory/architecture.md` | How: stack, parts, boundaries, architecture rules |
| `.specify/memory/decisions.md` | Why: one row per decision, never deleted |

A feature folder under `specs/` remains one change with its proof. Four laws govern the baseline:

1. One home per fact. Everything else links to it.
2. Calculate, do not maintain. A script derives each capability's owning spec and delivery state, and each part's state, from the specs, their `verification.md` and the code, and checks IDs and links.
3. The agent proposes; the user approves. Only the baseline amend command edits what the three baseline files mean; the script persists only pins, run evidence and synchronization records. Code never becomes correct because a baseline file was edited to match it.
4. Process weight follows change size. A new behavior takes the full path; a bug fix and a behavior-preserving change take shorter ones and create no spec.

The check script guards the baseline against drift:

- **Calculated views.** Ownership, delivery and part state are computed on read with `--status` or `--json`. Shared product and architecture rows are never rewritten by the checker; legacy calculated columns are ignored.
- **Citations and review.** Spec and plan citations are pinned per file. Reviewing changed pins requires `--reason`; a spec edit also requires explicit acknowledgment after reviewing its downstream plan and tasks. A targeted repin can save valid work while unrelated features remain stale.
- **Revision transitions.** One spec implements a capability. Later `**Changes**:` specs freeze the predecessor's accepted capability revision and the new revision when initially pinned. Subsequent changes name `**Previous change**`. Preserve historical evidence on its original revision; never relabel old tests as proof of a new promise.
- **Current evidence.** `--record-run --feature <feature>` executes every planned quality gate and saves a typed run ID, input digests, exit codes and hashed local logs. Bindings include spec, plan, task meaning, governing rules and decisions, constitution when present, listed code parts and local contracts. Cosmetic report edits, unfinished neighboring work and reconciliation stamps cannot renew a run.
- **Supported completion.** DONE requires approved/unblocked capabilities, accepted cited decisions, checked tasks, a verification plan, passing FR/AS/TR coverage, known statuses, complete commands and numeric counts, existing evidence, current run bindings and converged outcome. Required failures, skips and xfails block completion even with a reason. First completion obeys these checks too.
- **Code map and abandonment.** Map root tooling and hidden product code explicitly. Part state is derived from matching files; synchronization uses independent per-part records. An unfinished feature only excuses reconciliation warnings for listed parts. Inactive unfinished work is reported; `Completion: ABANDONED` provides no drift exemption. Scoped stamping requires supported DONE; global changed-code stamps require a reason.
- **Mandatory gates.** `--gate` is read-only, ignores advisory weakening, requires a baseline and accepted history base, and executes architecture-rule commands with pipeline failure handling, time and output limits. Workflow gates explicitly scope the current feature; global CI checks all features. A final workflow gate requires current DONE after implementation and convergence.
- **Context and review.** Missing/duplicate entries and malformed tables make context fail visibly. Local linked contracts are loaded with a size limit; oversized or external references must be read explicitly. Analyze and converge still judge semantics and append remediation tasks.
- **History.** Compare against an explicit accepted or PR-base revision and HEAD, with full Git history. Deleted accepted IDs and rewritten decision text fail. Retire capabilities or add superseding decision rows. Finished historical work remains valid on its original revision after retirement or a recorded transition.
- **Safe writes and recovery.** Per-feature evidence and pins, per-part stamps and initial adoption/mode use a checkout lock, compare-before-apply and recoverable journal. Invalid completion cannot be accepted in advisory mode. A missing adopted baseline fails; only non-adopter discovery is permissive. Required gates never treat absence as success.
- **Local version control.** The installer adds structural pre-commit and attribution commit-msg hooks while preserving foreign hooks. Local hooks are bypassable; CI and repository branch settings provide independent enforcement.
- **Existing code.** Recovery initializes advisory diagnostics before creating the baseline. Proposed rows require repository evidence and user approval. Adoption records an explicit accepted history base.

The script judges structure, not meaning: it can show that a record is incomplete or inconsistent, never that an assertion is adequate. Analyze, converge and the user's review still judge that.

The commands, templates, hooks, and check script are shipped in [extension/](extension/). Install them from the target project root:

```sh
specify extension add --dev <path-to-this-standard>/extension
```

It needs specify-cli 1.1.0 or later and was verified on 1.1.2 with the Codex (skills) and Claude layouts: installation, command and hook registration, and the check script, which has its own regression tests in `tests/`. Apply it to new projects; an existing project adopts it only when the user asks.

## 6. Testing policy

### 6.1 Design tests around promises

1. Every FR and AS requires meaningful TR assertions covering its specified positive, negative, boundary, authorization, failure, and recovery behavior. Every required TR needs an executable selector or specified observation method.
2. Choose the smallest useful layer: unit for domain rules; integration/contract for persistence/API interactions; actual operator request/form/action or browser tests for operator workflows; rendered/accessibility tests for UI promises; native/device tests for OS behavior.
3. Cover stale/revoked authority and transaction rollback/retry where specified. Test the response plus the resulting state and the absence of forbidden changes.
4. Seed the fixtures needed to reach negative paths. A cross-scope test requires a valid target outside the actor's scope; testing only empty lists does not exercise refusal.
5. Tests must assert promised outcomes rather than accidental implementation details. Screenshots require explicit evaluation.
6. Classify SCs explicitly. Release criteria require measured results before DONE; post-launch measures retain collection plans and are not invented as observed business outcomes.

### 6.2 Test-first implementation and regression

- Establish baseline results before changing behavior. For new behavior, write the tests before or alongside implementation and capture the expected behavioral RED before the production fix. Preserve a passing baseline for existing correct behavior; do not manufacture RED by breaking it.
- Missing devices, credentials, services, or a broken harness are BLOCKED, not expected RED and not PASS.
- Follow test → expected RED → implement → run → diagnose → fix → rerun. Implement the smallest complete fix. Diagnose failed checks rather than repeatedly retrying a missing prerequisite.
- Never alter approved behavior to satisfy a test. When intent really changes, obtain the material product decision, update artifacts, and invalidate affected evidence.
- Never weaken, delete, skip, disable, or blanket-suppress a valid check to get GREEN. Correct a demonstrably wrong test only against unchanged approved intent, with the reason recorded.
- Focused selectors support repair. Final completion requires the complete relevant configured suites and layer gates on the final state, including affected packages/plugins and the integration/device runs specified in the plan.
- A pre-existing red mandatory gate remains a completion gap. Fix it if in scope; otherwise report the blocker and what passed. Do not represent a narrow successful repair as whole-project health.
- Parallel execution is permitted only when fixtures, ports, data, devices, resources, and files do not conflict. Otherwise serialize.
- Neither blanket code coverage nor file/ID existence substitutes for behavioral verification.

### 6.3 Platform and observation adequacy

Define compile, unit/widget, integration, rendered, physical-device, accessibility, and performance evidence separately. A build cannot certify runtime; a non-native test harness cannot certify native OS integrations; a simulated platform cannot automatically certify all physical behavior. Match evidence capability to the exact claim, and add rendered, human, accessibility, performance, browser, or device observations where the claim requires them.

Required skips/xfails and absent observations block DONE. A platform may leave the product scope only through an explicit product decision recorded in the spec and dependencies, not because its hardware is unavailable.

### 6.4 BDD, coverage, and validation tooling

BDD/Gherkin is optional. Existing native test runners are sufficient when they assert the required behavior. If BDD is expressly adopted, pin its tooling, define the runner, connect the same IDs, execute scenarios, and keep the identical completion gate.

A structural validator MAY check duplicate IDs, missing FR/AS-to-TR links, orphan selectors, counts, status values, evidence links, and fingerprint freshness when justified. It cannot establish that assertions are meaningful or that screenshots prove usability. Analyze/converge must still inspect behavior. Do not claim such automation without actually implementing and validating it.

## 7. Verification evidence

### 7.1 Evidence semantics

Per-check statuses are **PASS**, **FAIL**, **NOT RUN**, and **BLOCKED** only. Planned checks start NOT RUN. Use BLOCKED for a known missing prerequisite, with cause and next step; FAIL for executed checks whose expectation failed. Historical PASS does not certify today's state.

Record exact working directory/command, exit code, passed/failed/skipped/xfailed counts when the runner provides them, and relevant evidence. If a tool uses different categories or has no counts, record its actual output and explain the mapping; do not invent numbers. Explain skips/xfails. A required skipped/xfailing behavior is not verified.

Do not claim PASS from partial output, a still-running process, timeout, missing exit status, an old log, code inspection, or a command that was merely written down. Capture the completed process result and observable assertions.

### 7.2 Tested state and freshness

Identify the actual code **and acceptance artifacts** tested: commit plus relevant dirty diff/content fingerprint, toolchain/lock inputs, configuration identity without secrets, services, fixture revision, and platform/device versions. A commit ID alone is insufficient when relevant uncommitted edits were exercised.

Maintain a small change-impact ledger: changed behavior/contract/fixture/tool input → affected FR/AS/TR/SC/platform → evidence invalidated → required reruns. After formatting or later relevant edits, rerun affected checks before final full gates. Preserve historical runs with their original status and fingerprint. Never relabel old evidence as current by changing its date.

Freeze the final relevant state for verification, review the staged diff, and commit the exact verified change. Record pre-commit evidence fingerprints accurately; do not claim a later documentation-only evidence update was itself part of an earlier runtime test. Re-run checks only where a relevant subsequent change invalidates them.

### 7.3 Required verification template

```markdown
# Verification: <feature>

Constitution: <actual version>
Profile: Spec Kit Universal Adoption and Execution Profile 3.0.0
Completion: NOT DONE
Tested revision / relevant working-tree fingerprint: <actual value>
Run date/time and timezone: <actual run time>
Environment: <locks/toolchain/services/config identity without secrets>
Platforms: <browser/device/emulator, OS/API/runtime versions>
Evidence root: <repository-owned path>

## Coverage

FRs with meaningful assertions: <covered>/<total>
ASs with meaningful assertions: <covered>/<total>
Required TRs passing: <passing>/<total>
Required release SCs met: <met>/<total>
Required task validation complete: <complete>/<total>

| FR / AS | TR | Executable selector or observation | Status | Evidence / tested state |
|---------|----|-------------------------------------|--------|-------------------------|
| <IDs> | <TR> | <path/node ID/description/method> | NOT RUN | No execution yet |

## Execution

| Working directory | Exact command | Exit code | Passed / failed / skipped / xfailed | Evidence |
|-------------------|---------------|-----------|------------------------------------|----------|
| <path> | <command> | NOT RUN | NOT RUN | <local evidence reference> |

## Additional acceptance evidence

| AS / SC | Method and platform | Expected | Observed | Status / evidence |
|---------|---------------------|----------|----------|-------------------|
| <ID> | <walkthrough/measurement> | <outcome> | Not observed | NOT RUN |

## Change-impact and freshness

| Change / input | Affected IDs and platform | Evidence affected | Required rerun / result |
|----------------|---------------------------|-------------------|-------------------------|
| <change> | <IDs> | <run/fingerprint> | <method and status> |

## Remaining gaps

<Missing assertions, failures, skips, missing/stale evidence, decisions,
blocked prerequisites, and feature-qualified remediation task IDs.>

## Convergence

Outcome: NOT RUN

<Actual assessment date and fingerprint, findings and task IDs. The Outcome
line holds exactly one of NOT RUN, tasks_appended, gaps_remaining, converged.>

## Historical runs

<Retain prior runs with their original tested states and limitations.>
```

The preset ships this template as `verification-template`; the plan command creates the record from it and the implement command fills it. Resolve template placeholders when creating concrete records. Do not require an unobserved check to PASS because the template expects a result.

### 7.4 Retention and sanitization

Keep required logs, screenshots, traces, timing measurements, archives, and other acceptance records under a planned repository-owned local evidence path. Decide explicitly which safe artifacts are committed or retained through documented local reproduction/retention. A required evidence link must resolve; do not cite an ephemeral artifact as durable proof.

Scan plain **and compressed** outputs for the material [section 3.8](#38-reproducibility-configuration-and-secrets) excludes, plus cookies, one-time codes, and temporary public endpoints, before retention/staging. Use synthetic/disposable actors and redact at capture where possible. Treat browser traces and server logs as potentially credential-bearing. Retain only what the claim needs.

## 8. Completion and convergence

### 8.1 Gates

- A story is DONE only when all its required FR/AS/TR behavior passes, release SCs are met, related regressions pass, required platform/manual observations are complete, and evidence is current.
- A feature is DONE only when every story is done, all affected layer gates pass on the final relevant state, mappings and evidence reconcile, and convergence finds no gaps.
- Otherwise the result is NOT DONE. Draft, In Progress, and Blocked may describe workflow progress but are not substitutes for DONE. Policy adoption has its own ADOPTED/PARTIAL gate in [section 13](#133-validation-methods-and-completion-gate).
- Checking tasks or checklist items, finding tests, passing lint, creating commits, or editing governance cannot individually establish feature completion.

### 8.2 Execution algorithm

1. Enter at the actual phase ([section 1.2](#12-start-from-the-phase-that-exists)).
2. Repair critical specification, constitution, plan, and mapping gaps before implementing affected behavior.
3. Analyze, implement, verify, and converge under [section 5](#5-synchronize-skills-commands-integrations-and-workflows).
4. For `tasks_appended` or `gaps_remaining`, implement existing/new in-scope work, verify again, and converge again.
5. For unavailable prerequisites or unresolved material decisions, record BLOCKED, finish independent work, and provide exact resumption steps. Repetition alone never changes BLOCKED to PASS.
6. Only `converged` with the complete gate satisfied permits DONE. Review/commit coherent work and report accurately.

The loop must terminate honestly when blocked or outside authorization; it must not expand scope indefinitely, invent behavior, or silently lower gates.

## 9. Execution and engineering discipline

### 9.1 Implementation quality

Match surrounding style, naming, architecture, idioms, and comment density. Make invariants structurally difficult to bypass. Keep focused diffs; avoid unrelated formatting/refactors. Leave no dead scaffolding or silent TODO standing in for required work. Apply the simplicity and reuse principles of [sections 3.5–3.6](#35-simplicity-and-explicit-non-goals).

### 9.2 Autonomous but scoped execution

Act when repository context supports one safe interpretation. Do not repeatedly request settled approvals. Complete authorized implementation, verification, documentation, and local commits; state blockers and out-of-scope remainder explicitly.

Parallelize independent operations, serialize dependencies, and respect resource/device contention. Prefer dedicated search, patch, repository, and platform tools over fragile shell rewriting. Inspect before overwrite/deletion. Never bypass denied access. Do not claim tool execution or results that did not happen.

### 9.3 Documentation

Update contracts, examples, configuration documentation, operational runbooks, and evidence in the same coherent change as affected behavior. Write plain operator/user guidance and precise executable developer guidance. Keep repository-relative links navigable and use supported clickable file references in reports. Never publish/distribute a file the agent has not read.

### 9.4 Security and restricted actions

Perform only authorized defensive security work. Obtain confirmation before destructive or hard-to-reverse actions and outward-facing transmission unless that exact action class is already explicitly authorized. Sending content to an external service is an outward-facing action; this profile does not authorize it by default.

Never impersonate a person/organization or fabricate a record as genuine. Use truthful identities/authorship and neutral pronouns where unknown. Keep refusals narrow and provide a safe alternative where possible.

### 9.5 Formatting, lint, types, and quality gates

Read and obey configured tools; do not add competing formatters/checkers by preference. Run formatting after edits, then rerun affected checks because relevant state changed. Run complete applicable layer gates before completion. The repository's actual commands are authoritative.

Typical lint/format/type gates per ecosystem (the repository's configured tool always wins):

- Python → ruff (`ruff check` + `ruff format`), or flake8/black/isort; mypy for types
- JS/TS → ESLint + Prettier; `tsc` for types
- Go → gofmt/goimports + go vet
- Rust → rustfmt + clippy

Honor zero-error gates and introduce no new warnings. A red CI pipeline gets fixed, never merged around; a gate that is routinely overridden guarantees nothing. Never use `--no-verify` to skip a gate. Narrow justified suppressions require a documented reason and cannot hide a correctable defect.

## 10. Local version control

1. Within current authorization, adoption of this profile includes ordinary non-destructive **local** Git history. It does not authorize publishing, destructive changes, discarding work, or rewriting history.
2. If there is no Git repository and the directory is the actual project root, initialize it, create a suitable `.gitignore`, inspect included files, and make an initial coherent commit before significant implementation. Do not initialize an artifact-output folder as a pretend project. If permissions or identity prevent a commit, record the exact blocker; do not fabricate an identity or success.
3. Inspect Git status at entry and before staging. Preserve pre-existing user changes and unrelated staged work. Never reset/discard them or accidentally include them. If related user edits cannot be separated safely, report the specific commit blocker and preserve the completed work.
4. Commit every coherent completed unit after applicable checks and documentation, without waiting for another request. Commit a completed prior unit before starting an unrelated request. Before the final report, commit safe authorized changes or explain why a coherent commit is blocked.
5. Stage explicit reviewed paths; review the staged diff for unrelated edits and the material [section 3.8](#38-reproducibility-configuration-and-secrets) excludes. Avoid blind all-files staging. One logical change per commit; follow repository history with a meaningful `type: what changed` message and feature-qualified task references where relevant.
6. A blocked checkpoint may be preserved only with a truthful message identifying its state. Never call failing/unverified work complete.
7. Keep operations local. External synchronization, hosted review, remote task conversion, and uploads are neither authorized nor required by this standard. Never force-push, even when a push has been authorized.
8. Obtain explicit authorization before hard reset, restoring/discarding uncommitted changes, history rewrite, branch deletion, or other destructive/irreversible operations. Do not infer it from authorization for ordinary commits.
9. Use truthful authorship; no invented human/model co-author identities. A coding agent MUST NOT list itself, its model or its vendor as a contributor: no `Co-Authored-By`, `Signed-off-by` or similar trailer that names an agent, no "Generated with" or "Generated by" line in a commit message or pull request, and no commit made under an agent's own author or committer identity. Commit as the user alone. This rule overrides an agent's built-in default to add such a line. The baseline extension ships a `commit-msg` hook that rejects these commits, and its check reports any that got past the hook.

## 11. Safe migration and upgrades

### 11.1 Existing features

Analyze/converge current behavior first, preserving history under [section 4.1](#41-identity). If intent or mappings are missing, use specify/plan to repair them before task generation. Converge must not invent intent.

Append traceable remediation for missing assertions, stale evidence, or unsupported completion. Re-implement/verify/converge to the current gate without erasing history. Do not reopen settled product choices merely to retrofit tests; expose real contradictions for decision. Superseded features remain historical with a replacement reference.

Select migration priority from the target's **current** active work, user-facing risk, and dependencies, and record the reason.

### 11.2 Reinitialization, upgrades, and drift

Before an upgrade, inventory local governance/customizations and inspect the supported migration path. Preserve originals through local version control. After an upgrade, compare and reapply applicable constitution, template, skill/command, workflow, metadata, and runtime behavior. Validate registration and integrity without erasing intentional customization.

Do not assume upstream defaults implement this policy, or that an upstream author field implies an operational dependency. Preserve provenance. A project-wide migration must not relabel historical external evidence as locally current or certify application behavior because configuration checks pass.

## 12. Optional modules

Each module is a separate file. Decide applicability during [discovery](#11-inspect-and-resolve-project-context), read only the applicable ones, and record the others as N/A with a concrete reason. A module adds rules; it never relaxes a core rule.

| Module | Apply when the product has |
|---|---|
| [modules/live-e2e.md](modules/live-e2e.md) | Running services and at least one client that talks to them |
| [modules/native-platforms.md](modules/native-platforms.md) | Native code, or promises about OS-level behavior on a specific platform |
| [modules/admin-content.md](modules/admin-content.md) | Operator/administrator roles, user-reported or operator-managed content, uploaded files or media, or multi-step workflows whose state advances over time |
| [modules/brand-assets.md](modules/brand-assets.md) | Shared identity assets used on more than one surface |

## 13. Adoption audit and validation

### 13.1 Mandatory report

Create or update `docs/spec-kit-adoption.md` (or the explicit repository equivalent). Include actual project context, previous/new constitution/profile versions, dates, scope, installed integrations, working branch, preserved history, conflicts/decisions, synchronization, validation commands/results, staged review/commit, next phase, and application-certification boundary.

Use one row for every numbered section/subsection and every command subsection in this profile, and for every applicable module section. Split rows further so every applicable MUST is explicitly accounted for; a section-level PASS cannot conceal a missed requirement.

```markdown
| Rule / section | Applicability and reason | Implemented in | Validation / evidence | Status |
|----------------|--------------------------|----------------|-----------------------|--------|
| <specific rule> | <applicable or concrete reason> | <actual files> | <content inspection or completed check> | <PASS/FAIL/BLOCKED/N/A> |
```

Adoption-row statuses are PASS, FAIL, BLOCKED, N/A. An applicable unvalidated rule is BLOCKED with the missing validation identified; never optimistic PASS. Individual application checks continue using [section 7.1](#71-evidence-semantics)'s statuses, including NOT RUN.

### 13.2 Required validation checklist

- [ ] Actual project/phase/feature(s), branch, user changes, and integration versions were inspected.
- [ ] Spec Kit initialization exists; any required supported initialization completed safely.
- [ ] All core sections, applicable module sections, and applicable MUST rules map to implementation and evidence.
- [ ] Existing constitution and ratification were preserved; semantic bump/amendment and Sync Impact Report are justified; no unexplained placeholders remain.
- [ ] Every principle of section 3 is concrete or legitimately N/A.
- [ ] Spec/plan/tasks/checklist templates implement section 4; verification has a supported template/guide.
- [ ] All active installed integrations implement section 5; required frontmatter and syntax remain valid.
- [ ] Authoritative integration source templates, workflow definitions, hooks, and supported manifest/checksum metadata are synchronized.
- [ ] Analyze is read-only; converge writes only appended deduplicated tasks; the lifecycle includes verification, convergence, and an honest repair handoff.
- [ ] Root/layer runtime guidance names actual full quality gates and working directories.
- [ ] Applicable module guides exist with target-specific values.
- [ ] Existing IDs, checkboxes, decisions, superseded features, and historical evidence were preserved.
- [ ] Content, not just path existence, was inspected in synchronized files.
- [ ] Relevant syntax/schema/link/placeholder/workflow/integration checks passed.
- [ ] Complete actual gate commands remain invocable; dry-run validation is labeled as such, not test execution.
- [ ] Diffs/staged paths were reviewed; no unrelated edits, secrets, or whitespace errors remain.
- [ ] Coherent safe authorized changes were committed locally, or the precise commit blocker is reported.
- [ ] Application checks are separately and accurately labeled; policy-only adoption claims no application certification.
- [ ] Repeated adoption produces no duplicate tasks, history loss, or needless semantic changes.
- [ ] Exact installed next invocation and any blocker-resolution steps are provided.

### 13.3 Validation methods and completion gate

Select checks from the installed environment: modified shell syntax parsing, JSON/YAML/frontmatter schema, supported workflow information/registration, integration status, managed hashes, placeholder scans, link checks, gate dry runs, local-only dependency scans, and diff whitespace checks. Use the actual supported equivalents and report exact results. A documented customization warning may be expected; missing/invalid operative files are not.

Report **ADOPTED** only when every applicable row and checklist requirement passes, no universal rule is N/A or blocked, relevant checks pass, the diff/staging was reviewed, and the coherent local adoption commit exists. Otherwise report **PARTIAL**, with precise gaps and current safe progress. Application tests may properly be NOT RUN for a policy-only change; that does not certify the app and does not need to become a fabricated adoption PASS.

## 14. Reusable invocation and reporting

### 14.1 Copyable instruction for a target agent

After `install.sh` has run on a project, use the full prompt in [adoption-prompt.md](adoption-prompt.md). For a project that is already adopted, this short form is enough:

```text
Read the Spec Kit Universal Adoption and Execution Profile at <path> completely,
plus only the modules its section 12 marks applicable to this repository.
Adopt it here following its section 2 adoption transaction. Report ADOPTED only
under its section 13 gate, otherwise PARTIAL with exact blockers. Then resume
the active authorized feature from its current phase, or give me the exact
installed next invocation if there is none.
```

### 14.2 Required final report from the receiving agent

Lead with adoption and requested-work outcome. State constitution/profile version, synchronized operative locations, validation actually run, commit(s), current feature completion separately, and remaining blockers. Give exact installed next invocation(s) with feature context. Keep the report concise but link to the detailed adoption/evidence files.

Never claim “best,” “100% accurate,” “fully tested,” or “complete” beyond observed evidence and the specified gate. Clearly label policy decisions, assumptions, current observations, and derived conclusions.
