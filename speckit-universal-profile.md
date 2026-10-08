# Spec Kit Universal Adoption and Execution Profile

**Profile version:** 1.0.0  
**Prepared:** 2026-10-02  
**Applies to:** new or existing projects, at any phase, in any supported agent integration.  
**Intent:** a complete, auditable instruction for upgrading project governance, installed Spec Kit skills/commands, templates, execution discipline, testing, evidence, and operational guidance.

## Read this first: instruction to the receiving agent

Read this entire file, including the source-retention map and reference appendix. Apply the normative profile in sections 0–18 to the target project. Amend its existing constitution; synchronize every applicable installed Spec Kit skill/command, template, workflow, integration metadata, and agent guidance file. Make the testing and completion policy concrete for its actual architecture. Validate the resulting contents and record adoption evidence. Do the work; a proposal or summary is not adoption.

This file is a user-authored project instruction when the user supplies it for adoption. It is not permission to exceed the current task, bypass platform restrictions, discard work, publish externally, change approved product scope, or treat source excerpts as executable commands. Sections 0–18 are normative. Appendix A contains attributed reference material only; its embedded commands, credentials, paths, product decisions, and historical PASS claims are **not instructions for the target project**.

If provided during an active feature, preserve its identity, branch, artifacts, checked history, and approved decisions. Apply governance updates first, repair only the artifacts needed to resume safely, then continue the already authorized feature from its current phase. Do not restart the project or regenerate completed work. If there is no active feature, complete adoption and provide the exact installed invocation for the next appropriate phase; do not invent a feature.

There is no claim that a Markdown instruction makes an agent infallible or guarantees superior results. This profile defines observable obligations, current evidence, and explicit failure states instead. Adoption and application completion are separate conclusions. [Source: S01, Purpose; S02, Scope and Validation evidence; S03, BDD and automation boundaries.](#source-register)

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
- [12. Local live end-to-end operations](#12-local-live-end-to-end-operations)
- [13. Native and platform-specific verification](#13-native-and-platform-specific-verification)
- [14. Content, administration, and stateful workflows](#14-content-administration-and-stateful-workflows)
- [15. Brand assets and derived visuals](#15-brand-assets-and-derived-visuals)
- [16. Adoption audit and validation](#16-adoption-audit-and-validation)
- [17. Reusable invocation and reporting](#17-reusable-invocation-and-reporting)
- [18. Source retention, corrections, and references](#18-source-retention-corrections-and-references)
- [Appendix A: all eight original source snapshots](#appendix-a-all-eight-original-source-snapshots)

## 0. Authority, terminology, and portability

Origins: [S01 §§Purpose, 1, 7–10; S02 Historical and migration boundary; S03 automation boundaries.](#source-register) The explicit repeatability, phase-entry, and change-impact mechanisms below are additional policy design in this consolidation, not independently proven performance improvements.

1. MUST means a required rule. SHOULD means follow it unless a concrete reason is recorded. MAY means optional. A rule conditional on a module applies only if that module exists in the target product.
2. Obey the environment's instruction hierarchy and current user authorization. Resolve conflicts explicitly. This profile must not override higher-priority instructions or imply that the agent can grant itself capabilities. Preserve established repository rules unless an authorized amendment changes them.
3. Read existing instructions and inspect evidence before editing. Distinguish approved requirements, inferred assumptions, historical records, and current observations. User assertions and old documents are inputs to verify, not automatic proof.
4. Do not import the source product, language, framework, feature numbers, staff model, media format, directory structure, fixed OTP, account identities, colors, hardware, tool versions, or thresholds as target defaults. Resolve all concrete choices from the target repository and approved intent.
5. Universal obligations cannot be dismissed as N/A: truthful execution, stable history, simplicity, search-first reuse, meaningful verification, reproducibility, secrets protection, safe local version control, and engineering discipline. Product modules may be N/A only with a concrete reason. A universal rule with unavailable prerequisites is BLOCKED, not N/A.
6. Keep governance under repository control. Prefer a durable path outside generated integration directories, such as `docs/speckit-universal-profile.md`. Use existing equivalent documentation locations when the project has them; record actual paths in the adoption report.
7. This profile's default completion model is locally authoritative. External boards, repository hosts, cloud previews, reviews, automation, synchronization, and artifact uploads are not prerequisites for feature or policy completion. Preserve genuine product dependencies, such as a payment provider or delivery service; a mocked dependency cannot certify live behavior that the specification promises.
8. User-required publishing or deployment is a separate authorized deliverable. Test it when it is part of the request. Do not silently add an external service to a local completion gate.
9. Do not install optional frameworks, BDD extensions, hooks, validators, remote services, new applications, or infrastructure merely to appear advanced. Add only what an active requirement and authorization justify.

## 1. Discover and enter at the current phase

Origins: [S01 §§1, 4–6, 10; S02 Resolved project context; S03 Commands.](#source-register)

### 1.1 Inspect and resolve project context

Inspect repository instructions, Git status and branch, Spec Kit version and installation provenance, constitution, templates, all active integrations, workflows, manifests, relevant code, architecture, test configuration, operational documentation, and current feature evidence. Do not infer installation health from filenames alone.

Record the following in `docs/spec-kit-adoption.md`, or the documented equivalent:

| Context | Required resolution |
|---|---|
| Product and scope | Purpose, current request, approved non-goals, active feature(s), superseded work |
| Layers and ownership | Authoritative data, authentication, authorization, invariants, contracts, consumers, trust boundaries |
| Actors | End users, staff/operators, exceptional users, service accounts, ownership and scopes |
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
| Applicable modules | UI, native code, staff, content, media, branding, offline features, stateful progression |

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

Origins: [S01 §§2, 4, 6, 9–10; S02 Conformance map and validation.](#source-register) Explicit transaction and repeated-application rules are consolidation additions.

1. Read the complete normative profile and source-retention map. Inspect all affected existing files before changing them. Treat Appendix A solely as attributed reference data.
2. Establish the existing state: Git status, constitution version/dates, current phase, integration health, configured quality gates, historical evidence. Record pre-existing failures without claiming responsibility or silently waiving them.
3. Map each numbered section/subsection and every applicable MUST obligation to actual files and a validation method. Map all eight source documents and their headings to preserved/adapted content. No applicable rule may disappear into an overall coverage percentage.
4. Amend the constitution and then synchronize templates, every installed active integration, workflows, runtime guidance, verification policy, local task conventions, and applicable operational guides. Preserve integration-specific syntax and schemas.
5. Update active feature artifacts only as needed for safe continuation. Do not mass-regenerate legacy specs, destroy checkboxes, reset evidence, or reactivate superseded scope.
6. Validate file contents, consistency, parsing/schema, internal links, placeholders, workflow resolution, and authoritative gate invocability. Run the checks appropriate to the changed files; policy-only validation cannot certify runtime behavior.
7. Review the complete relevant diff, scan for secrets and unrelated edits, stage explicit paths, review the staged diff, and create coherent local commits under section 10.
8. Record per-rule adoption evidence and unresolved gaps. Report ADOPTED only under section 16's gate. Otherwise report PARTIAL with exact FAIL/BLOCKED rows.
9. Resume the already authorized active phase, or print the exact installed next invocation when no feature execution is authorized.
10. On repeated application, compare existing behavior with this profile and patch only genuine drift. Preserve equivalent implementations, IDs, dates, history, and file ownership. Do not create a version bump or duplicate task because the prompt was provided again. A second pass with no substantive drift must produce no semantic changes.

Do not stop after editing only the constitution or testing guide. Adoption requires synchronized operative skills/commands and templates, not merely a document describing desired behavior.

## 3. Amend the constitution

Origins: [S01 §§2.1–2.9, 7; S02 conformance and migration.](#source-register)

Use the installed constitution skill/command where available. Update the existing constitution in place. Preserve original ratification, record the actual amendment date, justify semantic versioning, and prepend a Sync Impact Report covering old/new version, changed/added/removed principles, synchronized files, pending work, and conflicts. Major bumps are for incompatible governance changes; minor for added/materially expanded governance; patch for clarifications without changed obligations. Do not copy the source constitution's version or ratification date.

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
- String existence or screenshot-text matching alone does not prove dimensions, target size, focus behavior, RTL layout, or accessibility. Use measurements and interactions relevant to the acceptance claim.

### 3.4 Data preservation, deletion, and exceptions

- Define immutable, archived, soft-deleted, hard-deletable, and retention-governed data, including correction and audit history. These are product decisions; soft deletion is not a universal default.
- Define shared-content ownership, moderation eligibility, distinct-reporter rules and thresholds where applicable, visibility after removal, and restoration authority.
- Identify external content outside local preservation guarantees, visibly label the limitation wherever it is presented, and retain local references according to policy.
- Keep exceptions narrow, explicit, derived where possible, and testable. Apply this module to user, historical, shared, or regulated records; otherwise record why it is N/A.

### 3.5 Simplicity and explicit non-goals

- Preserve approved non-goals and settled decisions. Build the smallest complete architecture for the active requirement.
- Do not create speculative services, framework layers, future clients, or parallel staff applications.
- Record justified constitutional exceptions in plan Complexity Tracking, with rationale, impact, and verification. An exception cannot silently remove security or completion gates.

### 3.6 Mandatory DRY and reusable design

- Shared domain knowledge, validation, authorization, configuration, transformations, and UI behavior require one authoritative implementation. Search for existing helpers, services, components, policies, validators, serializers, fixtures, hooks, and utilities before adding code.
- Reuse or extend matching contracts. If shared behavior is duplicated, extract a small cohesive component with a stable interface and direct tests. Prefer composition to copied large implementations.
- Centralize security/business invariants so alternate write paths cannot maintain independent rules.
- Parameterize only observed variation. Similar syntax with different domain semantics must remain separate; explain intentional semantic duplication in the plan/review.
- Preserve layer ownership and dependency direction. Avoid circular dependencies and moving enforcement into an untrusted client.
- Refactors must preserve behavior and pass affected regressions. Reusable UI must expose needed variants, share theme tokens, and retain accessibility/localization.

### 3.7 Verification before completion

- Map every FR and AS to one or more TRs with meaningful observable assertions. Cover specified positive, negative, boundary, authorization, failure, and recovery behavior.
- Write new-behavior tests before or alongside implementation and run them to establish the expected behavioral failure before the production fix. Preserve a passing baseline for existing correct behavior; do not manufacture RED by breaking it.
- Missing devices, credentials, services, or a broken harness are BLOCKED, not expected RED and not PASS.
- Never weaken/delete/skip a valid assertion to get GREEN. Correct a defective test only against unchanged approved intent and record the reason.
- Use focused repair tests, then relevant full regression/layer gates on the final state. Add rendered, human, accessibility, performance, browser, or device observations where required.
- Neither blanket code coverage nor file/ID existence substitutes for behavioral verification.

### 3.8 Reproducibility, configuration, and secrets

- Commit synchronized dependency manifests and locks; install exact locked versions for repeatable gates.
- Pin tools explicitly and containers by immutable digest. Resolve compatible pins for the target project; never import the source's old versions as current recommendations.
- Document one supported way to run each complete gate and equivalent dependency inputs across supported local environments.
- Keep credentials, signing keys, tokens, tracked secret-bearing `.env` files, personal data, and unrestricted dumps out of commits and retained evidence.
- Document configuration variable names and safe examples without secret values. Use environment variables or approved credential helpers.

### 3.9 Scoped staff/operator administration

- Apply only when staff/operator and exceptional technical authority exist. Identify the official interface and approved workflows; otherwise record N/A.
- Scope reads, choice lists, related-object selectors, direct URLs, forms, bulk actions, and writes consistently at the trusted boundary.
- Reject revoked, inactive, forged, stale, and cross-scope authority, including the next write from an already active session after revocation.
- Ordinary staff cannot create/promote staff or grant themselves authority unless expressly specified. Exceptional correction powers and audit expectations must be explicit.
- Do not introduce a separate staff app until observed workflows show the existing interface cannot serve them safely, clearly, or efficiently.
- Test actual staff requests/forms/actions. Service tests supplement rather than certify the interface.

### 3.10 Repository-wide engineering obligations

Include sections 9–11's execution, documentation, style, local commits, security, formatting/types, dependencies, upgrade, and migration rules in governance and runtime guidance. Do not drop them because they are not acceptance-test instructions.

## 4. Stable identities and artifact contracts

Origins: [S01 §3; S03 artifacts, IDs and evidence; S04 all sections.](#source-register)

### 4.1 Identity

| Identifier | Meaning | Cross-feature reference |
|---|---|---|
| `FR-001` | Functional requirement | `<feature-number>/FR-001` |
| `AS-001` | Acceptance scenario, unique within the whole feature | `<feature-number>/AS-001` |
| `TR-001` | Test requirement | `<feature-number>/TR-001` |
| `SC-001` | Measurable success criterion | `<feature-number>/SC-001` |
| `T001` | Task, local to its feature's tasks file | `[NNN] T001: <description>` |
| `CHK001` | Requirements-quality checklist item | Qualify with owning feature/checklist when needed |

Each feature may restart task numbering at T001. Bare task IDs are valid inside the owning tasks file; use `[NNN] TXXX` in commits, cross-feature artifacts, verification, and reports. Preserve suffixes and legacy IDs, such as `FR-009a` or `US1/AC2`, with stable aliases. Never silently renumber. Append above the current maximum, respecting the existing numbering convention. Preserve checked history; checkboxes are not behavioral evidence.

### 4.2 Feature artifacts

Use the target's actual feature layout, ordinarily `specs/NNN-feature/`. Core artifacts are `spec.md`, `plan.md`, `tasks.md`, `verification.md`, and requirements-quality `checklists/`. Add `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` when their purpose applies. Do not create empty ceremonial artifacts.

| Artifact | Mandatory content and boundary |
|---|---|
| `spec.md` | Prioritized independently testable stories; stable FR/AS/TR/SC; edge cases; assumptions/dependencies; full FR/AS-to-TR matrix; measurable expected outcomes; binary completion gate. Keep implementation-agnostic. Classify SCs as release gates or post-launch measurements; do not invent future results. |
| `plan.md` | Real paths and boundaries; Constitution Check before/after design; reuse inventory and authoritative homes; prerequisites, fixtures, layers, selectors/commands, performance conditions, regressions, browser/device/manual evidence, and each TR's implementation location. Initialize or preserve planned verification as NOT RUN. |
| `tasks.md` | Dependency-ordered work grouped by story; tests, reuse search/extraction, implementation, focused verification/repair, related regression, final complete gates, evidence reconciliation, convergence, documentation, and coherent commits. Map test/verification work to FR/AS/TR and paths/selectors. Preserve old work when updating. |
| `checklists/*.md` | Completeness, clarity, consistency, measurability, and scenario coverage of written requirements. Preserve items and append unique CHK IDs. They must not assert runtime behavior such as “API returns 200” or “button works.” |
| `verification.md` | Actual tested state, environment, commands, exit/results/counts, per-TR evidence, manual measurements, gaps, and convergence. Distinguish planned from executed and old from current. |
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

Origins: [S01 §4; S02 installed integration and validation; S03 Commands; official references R01–R02.](#source-register)

### 5.1 Integration contract

- Discover all actual active integration paths and invocation forms. Dotted slash commands, hyphenated skills, `$skill` mentions, and shell CLI subcommands are not interchangeable. Verify installed help/schema rather than assuming a version. Official Spec Kit distinguishes agentic invocations from CLI operations. [GitHub Spec Kit, Quickstart and Extensions (R01–R02).](#authoritative-technical-references)
- Amend every applicable active skill/command and its authoritative source template so regeneration does not restore weaker behavior. Preserve frontmatter, required fields, invocation syntax, argument handling, feature-selection controls, provenance, and compatibility.
- Synchronize root and layer agent guidance (`AGENTS.md`, `CLAUDE.md`, or equivalents) and feature templates. Concrete runtime guidance must name actual commands and working directories.
- Inspect reusable workflow definitions, hooks, manifests, declared versions and hashes. Recompute managed metadata only through the installation's supported ownership/update process after content validation; do not rewrite integrity data merely to hide unexpected changes.
- Validate parser/schema, required files, actual registration, workflow resolution, and managed checksums where applicable. Distinguish an expected documented customization warning from a real missing/invalid integration.
- If a required capability is absent, use the supported local customization/installation mechanism within authorization, or provide the exact equivalent agent instruction and record the blocker. Do not falsely claim that a native command exists or is installed.
- Optional external task-conversion features are not part of this completion model. Retain authorized optional integrations without making them gates; retire active dependencies on them where they conflict with local-only policy. Preserve historical links as provenance.

### 5.2 `speckit-constitution`

Amend in place with semantic version, original ratification, current amendment date, and Sync Impact Report. Propagate to all templates, active skills/commands, runtime guidance, workflows, and affected docs. Validate language, dates, headings, placeholders, and consistency. Review and commit the coherent governance unit.

### 5.3 `speckit-specify`

Create from the spec template only when the spec is absent. Updates must preserve approved intent, dependencies, IDs, checked history, supersession, and decisions. Provide stories, FR/AS/TR/SC, matrix, edge cases, measurable outcomes, and the completion gate. Keep intent implementation-agnostic and verifiable. Commit completed coherent edits under section 10.

### 5.4 `speckit-clarify`

Ask at most five high-impact questions, one at a time, using repository-grounded recommendations. Integrate each accepted answer immediately, remove contradictions, and reevaluate requirements quality. Clarify behavior and acceptance, not minor implementation preferences. Preserve settled answers and record resulting verification changes.

### 5.5 `speckit-plan`

Run Constitution Checks before and after design. Plan every FR/AS through TRs at the smallest adequate layer, including the real interface where the promise is made. Specify actual paths, commands/selectors, fixtures, services, browser/device capability, performance measurement conditions, and complete regressions. Identify reuse candidates and authoritative shared invariants; explain intentional duplication. Initialize/preserve verification without predeclaring PASS.

### 5.6 `speckit-tasks`

Preserve task IDs and history. Treat tests as mandatory; map every FR/AS through TR to concrete work. Order tests before production implementation and verification after it. Include explicit reuse search, justified extraction/refactoring with regressions, exact complete gates, evidence, SC reconciliation, convergence, docs, and commits. No story-completion task may lack required behavioral coverage.

### 5.7 `speckit-analyze`

Remain read-only: no application, spec, task, evidence, or report-file mutations under this invocation. Compare constitution/spec/plan/tasks and current evidence. Independently report FR, AS, TR, and task coverage, plus release SC and platform evidence where applicable. Inspect meaningful assertions and actual interfaces, not just IDs. Flag duplicated invariants, unnecessary parallel components, ignored reuse opportunities, and critical missing mappings. Distinguish planned NOT RUN from false/stale completion. Report needed decisions without modifying files.

### 5.8 `speckit-implement`

Read intent, design, tasks, and evidence together. Establish the baseline, search for reuse, and follow test → expected RED for new behavior → implement → run → diagnose → fix → rerun. Reuse passing existing tests where appropriate. Continue independent in-scope work around a real blocker. Preserve acceptance intent, record results only after completion/exit, and check a task only when its applicable validation passes. Run final relevant full gates; record current evidence; invoke convergence and repair in scope until clean or genuinely blocked. A narrow task does not imply feature completion.

### 5.9 `speckit-converge`

Compare current implementation, meaningful assertions, and current evidence against spec/plan/tasks. Explicitly inspect reuse and duplicated authorization, validation, invariants, configuration, UI styling/interactions. Under this command, the **only allowed file mutation is appending deduplicated remediation tasks to `tasks.md`**. Do not modify application code, spec, plan, existing task history, or verification.

Cite matching existing open tasks rather than duplicating them. Append a new task for an unsupported historical check while preserving the old checkbox. Include relevant FR/AS/TR, affected paths, expected repair verification, and dependencies. Report exactly one outcome:

- `tasks_appended`: new uncovered remediation was appended, whether or not other existing gaps remain.
- `gaps_remaining`: no new tasks were needed, but open work, decisions, blockers, or missing/stale evidence remain.
- `converged`: no gaps remain and all required current verification passes.

No new tasks is not equivalent to converged. Return the assessed fingerprint and findings in the response. An enclosing implement/verify workflow may record that outcome in `verification.md` after the converge invocation returns, without expanding converge's write permissions.

### 5.10 `speckit-checklist`

Validate written requirements only. Preserve existing checklists, append uniquely numbered CHK items, and never represent checklist completion as runtime proof.

### 5.11 Workflow and repair handoff

The lifecycle is specify → review/clarify → plan → review → tasks → analyze → implement → verify → converge. Existing-feature entry follows section 1.2. When verification fails or convergence finds work, return to implementation, rerun affected/full verification, and converge again.

If the workflow engine cannot express a repair loop, stop with an honest NOT DONE result and print the exact supported implement/verify/converge invocations and feature selection. Do not declare success simply because implementation ended. Preserve the same feature directory; use `SPECIFY_FEATURE_DIRECTORY` only if supported by that installation, otherwise its verified selection mechanism.

## 6. Testing policy

Origins: [S01 §§2.7, 3–5, 8; S03 all sections; S05–S07 operational checks.](#source-register)

### 6.1 Design tests around promises

1. Every FR and AS requires meaningful TR assertions, and every required TR needs an executable selector or specified observation method.
2. Choose the smallest useful layer: unit for domain rules; integration/contract for persistence/API interactions; actual staff request/form/action or browser tests for operator workflows; rendered/accessibility tests for UI promises; native/device tests for OS behavior.
3. Cover specified success/refusal, boundary, stale/revoked authority, transaction rollback/retry, failures and recovery. Test response plus resulting state and absence of forbidden changes.
4. Seed the fixtures needed to reach negative paths. A cross-scope test requires a valid target outside the actor's scope; testing only empty lists does not exercise refusal.
5. Tests must assert promised outcomes rather than accidental implementation details. Screenshots alone require explicit evaluation; filenames and ID markers alone are not coverage.
6. Classify SCs explicitly. Release criteria require measured results before DONE; post-launch measures retain collection plans and are not invented as observed business outcomes.

### 6.2 Test-first implementation and regression

- Establish baseline results before changing behavior. For new behavior, capture the relevant expected behavioral RED before the production fix; harness/setup failures do not satisfy this requirement.
- Implement the smallest complete fix. Diagnose failed checks rather than repeatedly retrying a missing prerequisite.
- Never alter approved behavior to satisfy a test. When intent really changes, obtain the material product decision, update artifacts, and invalidate affected evidence.
- Correct demonstrably wrong tests with a recorded reason against approved intent. Do not blanket-suppress, disable, delete, skip, or weaken checks to evade defects.
- Focused selectors support repair. Final completion requires the complete relevant configured suites and layer gates on the final state, including affected packages/plugins and integration/device runs specified in the plan.
- A pre-existing red mandatory gate remains a completion gap. Fix it if in scope; otherwise report the blocker and what passed. Do not represent a narrow successful repair as whole-project health.
- Parallel execution is permitted only when fixtures, ports, data, devices, resources, and files do not conflict. Otherwise serialize.

### 6.3 Platform and observation adequacy

Define compile, unit/widget, integration, rendered, physical-device, accessibility, and performance evidence separately. A build cannot certify runtime; a non-native test harness cannot certify native OS integrations; a simulated platform cannot automatically certify all physical behavior. Match evidence capability to the exact claim.

Required skips/xfails and absent observations block DONE. A platform may leave the product scope only through an explicit product decision recorded in the spec and dependencies, not because its hardware is unavailable.

### 6.4 BDD, coverage, and validation tooling

BDD/Gherkin is optional. Existing native test runners are sufficient when they assert the required behavior. If BDD is expressly adopted, pin its tooling, define the runner, connect the same IDs, execute scenarios, and keep the identical completion gate. No optional BDD installation is authorized merely by this file.

A structural validator MAY check duplicate IDs, missing FR/AS-to-TR links, orphan selectors, counts, status values, evidence links, and fingerprint freshness when justified. It cannot establish that assertions are meaningful or that screenshots prove usability. Analyze/converge must still inspect behavior. Do not install or claim such automation without actually implementing and validating it.

## 7. Verification evidence

Origins: [S01 §§3, 5, 7.5; S03 Evidence format; S02 Validation evidence; S05–S07 sanitized local runs.](#source-register) The explicit freshness ledger strengthens the supplied tested-state requirement.

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
Profile: Spec Kit Universal Adoption and Execution Profile 1.0.0
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

<Actual assessment date and fingerprint; exactly one of tasks_appended,
gaps_remaining, converged; findings and task IDs. Initially NOT RUN.>

## Historical runs

<Retain prior runs with their original tested states and limitations.>
```

Resolve template placeholders when creating concrete records. Do not require an unobserved check to PASS because the template expects a result.

### 7.4 Retention and sanitization

Keep required logs, screenshots, traces, timing measurements, archives, and other acceptance records under a planned repository-owned local evidence path. Decide explicitly which safe artifacts are committed or retained through documented local reproduction/retention. A required evidence link must resolve; do not cite an ephemeral artifact as durable proof.

Scan plain **and compressed** outputs for credentials, tokens, cookies, signing material, personal data, OTPs, unrestricted dumps, and temporary public endpoints before retention/staging. Use synthetic/disposable actors and redact at capture where possible. Treat browser traces and server logs as potentially credential-bearing. Retain only what the claim needs. Do not upload evidence externally for completion.

## 8. Completion and convergence

Origins: [S01 §§4.8, 5–6; S03 loop and completion rules.](#source-register)

### 8.1 Gates

- A story is DONE only when all its required FR/AS/TR behavior passes, release SCs are met, related regressions pass, required platform/manual observations are complete, and evidence is current.
- A feature is DONE only when every story is done, all affected layer gates pass on the final relevant state, mappings and evidence reconcile, and convergence finds no gaps.
- Otherwise the result is NOT DONE. Draft, In Progress, and Blocked may describe workflow progress but are not substitutes for DONE. Policy adoption has its own ADOPTED/PARTIAL gate in section 16.
- Checking tasks, finding tests, passing lint, creating commits, or editing governance cannot individually establish feature completion.

### 8.2 Execution algorithm

1. Enter at the actual phase and preserve approved intent/history.
2. Repair critical specification, constitution, plan, and mapping gaps before implementing affected behavior.
3. Analyze consistency and meaningful coverage without writing under analyze.
4. Implement authorized tasks with reuse and test-first verification.
5. Diagnose failures, repair in scope, run focused checks and final relevant full gates, and record actual evidence.
6. Converge using current code/assertions/evidence; append only deduplicated uncovered remediation under converge.
7. For `tasks_appended` or `gaps_remaining`, implement existing/new in-scope work, verify again, and converge again.
8. For unavailable prerequisites or unresolved material decisions, record BLOCKED, finish independent work, and provide exact resumption steps. Repetition alone never changes BLOCKED to PASS.
9. Only `converged` with the complete gate satisfied permits DONE. Review/commit coherent work and report accurately.

The loop must terminate honestly when blocked or outside authorization; it must not expand scope indefinitely, invent behavior, or silently lower gates.

## 9. Execution and engineering discipline

Origins: [S01 §§7.1–7.3, 7.5–7.7; S02 local quality gates and dependencies.](#source-register)

### 9.1 Implementation quality

Match surrounding style, naming, architecture, idioms, and comment density. Prefer the simplest complete solution. Make invariants structurally difficult to bypass. Keep focused diffs; avoid unrelated formatting/refactors. Leave no dead scaffolding or silent TODO standing in for required work. Apply search-first reuse and preserve semantic differences.

### 9.2 Autonomous but scoped execution

Act when repository context supports one safe interpretation. Ask only when materially different choices affect behavior or architecture. Do not repeatedly request settled approvals. Complete authorized implementation, verification, documentation, and local commits; state blockers and out-of-scope remainder explicitly.

Parallelize independent operations, serialize dependencies, and respect resource/device contention. Prefer dedicated search, patch, repository, and platform tools over fragile shell rewriting. Inspect before overwrite/deletion. Never bypass denied access. Do not claim tool execution or results that did not happen.

### 9.3 Documentation

Update contracts, examples, configuration documentation, operational runbooks, and evidence in the same coherent change as affected behavior. Write plain operator/user guidance and precise executable developer guidance. Keep repository-relative links navigable and use supported clickable file references in reports. Never publish/distribute a file the agent has not read.

### 9.4 Security and restricted actions

Use secrets indirectly through approved mechanisms; inspect suspicious staged files. Perform only authorized defensive security work. Obtain confirmation before destructive or hard-to-reverse actions and outward-facing transmission unless that exact action class is already explicitly authorized. Sending content to an external service is an outward-facing action; this profile does not authorize it by default.

Never impersonate a person/organization or fabricate a record as genuine. Use truthful identities/authorship and neutral pronouns where unknown. Keep refusals narrow and provide a safe alternative where possible. Do not circumvent platform denials.

### 9.5 Formatting, lint, types, and quality gates

Read and obey configured tools; do not add competing formatters/checkers by preference. Run formatting after edits, then rerun affected checks because relevant state changed. Run complete applicable layer gates before completion. Python, JS/TS, Go, Rust, mobile, or other examples are illustrative; actual repository commands are authoritative.

Honor zero-error gates and introduce no new warnings. Never evade a real failure with blanket suppressions, disabled tests, ignored types, or `--no-verify`. Narrow justified suppressions require a documented reason and cannot hide a correctable defect. Fix configured red gates in authorized scope or report a completion blocker. Pin tool versions.

### 9.6 Dependencies and builds

Keep manifests and locks synchronized in the same change. Install exact committed inputs rather than re-resolving ranges during repeatable builds. Pin image digests and tool versions. Add dependencies/infrastructure only for a current requirement; prefer the standard library or an existing dependency when sufficient. Verify supported environments use equivalent inputs.

## 10. Local version control

Origins: [S01 §7.4 and reusable instruction; S04 Local workflow; S02 staged diff/commit evidence.](#source-register)

1. Within current authorization, adoption of this profile includes ordinary non-destructive **local** Git history. It does not authorize publishing, destructive changes, discarding work, or rewriting history.
2. If there is no Git repository and the directory is the actual project root, initialize it, create a suitable `.gitignore`, inspect included files, and make an initial coherent commit before significant implementation. Do not initialize an artifact-output folder as a pretend project. If permissions or identity prevent a commit, record the exact blocker; do not fabricate an identity or success.
3. Inspect Git status at entry and before staging. Preserve pre-existing user changes and unrelated staged work. Never reset/discard them or accidentally include them. If related user edits cannot be separated safely, report the specific commit blocker and preserve the completed work.
4. Commit every coherent completed unit after applicable checks and documentation, without waiting for another request. Commit a completed prior unit before starting an unrelated request. Before the final report, commit safe authorized changes or explain why a coherent commit is blocked.
5. Stage explicit reviewed paths; review the staged diff. Avoid blind all-files staging where unrelated/unreviewed work may exist. One logical change per commit; follow repository history with a meaningful `type: what changed` message and feature-qualified task references where relevant.
6. A blocked checkpoint may be preserved only with a truthful message identifying its state. Never call failing/unverified work complete.
7. Keep operations local. External synchronization, hosted review, remote task conversion, and uploads are neither authorized nor required by this standard.
8. Obtain explicit authorization before hard reset, restoring/discarding uncommitted changes, history rewrite, branch deletion, or other destructive/irreversible operations. Do not infer it from authorization for ordinary commits.
9. Use truthful authorship; no invented human/model co-author identities. Inspect for secrets and sensitive data before committing.

## 11. Safe migration and upgrades

Origins: [S01 §§6, 9–10; S02 Historical and migration boundary; S03 existing-feature commands.](#source-register)

### 11.1 Existing features

Preserve old identifiers, checkboxes, evidence, approved decisions, dependencies, and supersession. Analyze/converge current behavior first. If intent or mappings are missing, use specify/plan to repair them before task generation. Converge must not invent intent.

Append traceable remediation for missing assertions, stale evidence, or unsupported completion. Re-implement/verify/converge to the current gate without erasing history. Do not reopen settled product choices merely to retrofit tests; expose real contradictions for decision. Superseded features remain historical with a replacement reference.

Select migration priority from the target's **current** active work, user-facing risk, and dependencies. The source files name different feature priorities in different snapshots; none is a universal ordering. Preserve the reason for target selection instead of copying feature numbers.

### 11.2 Reinitialization, upgrades, and drift

Keep this profile outside generated directories where feasible. Before an upgrade, inventory local governance/customizations and inspect the supported migration path. Preserve originals through local version control. After an upgrade, compare and reapply applicable constitution, template, skill/command, workflow, metadata, and runtime behavior. Validate registration and integrity without erasing intentional customization.

Do not assume upstream defaults implement this policy, or that an upstream author field implies an operational dependency. Preserve provenance. A project-wide migration must not relabel historical external evidence as locally current or certify application behavior because configuration checks pass.

## 12. Local live end-to-end operations

Origins: [S05 all sections; S06 runtime limitations; S07 end-to-end and phone guidance.](#source-register)

Apply this module to products with running services and clients. Produce or amend a generic equivalent of `docs/live-testing.md`, linked to native/content guides where present. Separate setup, reachability, compile/runtime, acceptance observations, diagnostics, evidence, and teardown.

### 12.1 Prerequisites and topology

- Start the actual configured backend/services with safe local configuration. Seed disposable actors and realistic files/objects through the project-supported path; verify required buckets/permissions or equivalent services.
- Record exact locked SDK/toolchain components, revisions, archive checksums where the runner supports them, OS/browser/device identifiers, acceleration, and fixture inputs.
- Resolve API **and asset/media** addresses from the client/device's network perspective. A host precheck does not prove device access. Confirm actual target-side reachability, signed/public access policy, manifests/segments if relevant, and environment-specific transport restrictions.
- Use supported local networking by default. Scope any cleartext development exception narrowly; do not weaken production transport policy.
- Validate prerequisite failures before diagnosing the app. Reachability failure identifies a setup/dependency gap, not automatically a client defect.
- Prefer bounded startup/health helpers with readiness deadlines, actionable diagnostics, and explicit teardown. Do not assume the source's competing helper paths exist.

### 12.2 Acceptance walkthrough

1. Run the installed app/client against the local test stack and establish the actual user role/scope.
2. Visit required hierarchy/navigation, content, offline/runtime, and operator surfaces. Check relevant locale/directionality, state/recovery, and no crashes; capture sanitized rendered evidence.
3. Exercise positive and negative authorization through the actual interface. Correlate the response/server record with user-visible feedback and resulting state. A server refusal does not alone prove the user sees an actionable reason.
4. For downloadable content, verify progress/completion and correct control-state changes; disable **all relevant transport** and verify the network is actually unavailable, then open/play each promised type from local storage. Merely disabling cellular data is insufficient if another transport remains usable.
5. Attempt a new download offline. Assert the approved user message, queued behavior, automatic resume/retry on reconnection, and resulting content integrity where promised.
6. Exercise live refresh after operator updates, manual refresh, background/resume, and active-context changes. Assert that context labels, displayed descendants, caches, and navigation reconcile together; stale descendant pages must not expose the previous context if the specification promises their closure.
7. Record measurements and evidence per AS/TR/SC. Do not inherit source run results.

### 12.3 Repeatable E2E coordinator

Where the project has an existing end-to-end command, preserve and document it. If the current requirements justify building one, use isolated test-only actors/data, real permitted operator submissions, client refresh, sanitized diagnostics/screenshots/timings, and teardown. Constrain credentials and destinations; reject accidental production targets. Do not expose tokens/passwords through CLI arguments or retained traces. Keep exact commands project-specific in the resulting runbook.

### 12.4 Local phones and optional tunnels

Use a reachable private address, supported device forwarding, or another approved local route as appropriate. Treat API and object storage as separate endpoints when the topology requires it. Build-time endpoint configuration binds a build to that configuration; record it without retaining sensitive/transient hostnames.

An external tunnel/preview is optional exploratory infrastructure, subject to explicit authorization for external exposure. Do not open one just because Appendix A shows it. If authorized, stop it afterward, restore service URL configuration, and remove transient endpoints from retained artifacts. It is not a default completion dependency.

### 12.5 Success criteria and teardown

Map separately: each platform's visible behavior; download/offline use on promised platforms; allowed/refused upload/write paths; device-to-service/asset reachability; and reproducibility of the documented process. Stop emulators/VMs and dispose only of identified test-owned data after capture. Preserve persistent development environments; distinguish stop from destructive remove.

## 13. Native and platform-specific verification

Origins: [S06 all sections; S05 platform strategy; official Android/Apple references R03–R06.](#source-register)

### 13.1 Capability matrix

Record the target's actual environment rather than the source workstation's claims:

| Platform/environment | Build/compile | Unit/package | Native integration | Rendered UI | Physical OS behavior | Prerequisites / evidence |
|----------------------|---------------|--------------|--------------------|-------------|----------------------|--------------------------|
| <actual target> | <check status> | <check status> | <check status> | <check status> | <check status> | <versions, resources, method> |

Compilation, local unit/widget tests, native runtime, visual rendering, and physical-device acceptance are different claims. Mark required unavailable capability BLOCKED. Do not remove a supported platform without an explicit product decision.

### 13.2 Android or equivalent local emulator

- Pin the SDK/system image/tool inputs required by the target. Verify acceleration, device discovery, bounded boot readiness, and the intended build variant.
- Run app/package static checks, non-device plugin tests, and device integration selectors from their correct directories. Root tests must not silently omit separately configured packages.
- Resolve host networking correctly. For the Android Emulator's documented virtual router, `10.0.2.2` aliases the host loopback; it is not a universal physical-phone or arbitrary-emulator address. [Android Developers, Network address space (R03).](#authoritative-technical-references)
- Capture screenshots and native logs where relevant, but do not claim screenshot text proves layout or compile success proves runtime.
- Document start/wait/headless/stop operations supported by the actual helpers. Historical boot times, AVD names, API levels, and successful APK builds are not guarantees for another machine.

### 13.3 Apple/iOS or equivalent proprietary platform

- Use an available, authorized, supported local build environment and current compatible toolchain. Verify platform licensing/support and the user's actual hardware; do not default to a non-Apple virtualization recipe.
- For iOS build/simulator work, install/select full compatible Xcode, required SDKs and runtimes, dependencies, and accepted license prerequisites. The standalone macOS Command Line Tools package is not a substitute for Xcode-only `xcodebuild`/`simctl` tooling. [Apple, Xcode command-line tool reference and Installing the command-line tools (R04–R05).](#authoritative-technical-references)
- Transfer the project locally through an authorized route, excluding generated build/cache output and keeping secrets confined. Use exact committed dependency inputs. Do not require a remote clone as the only route.
- Resolve backend connectivity from that environment. Run configured analysis/unit checks, platform builds, and simulator integration separately. An unsigned build demonstrates only the relevant build claim; it does not certify install/signing, rendering, or physical behavior.
- If a VM can compile but cannot provide required graphics/simulator functionality, retain compile evidence and mark rendered/device checks BLOCKED. Do not equate a booted VM with a working simulator.
- Use a locally installed signed development build where physical behavior requires it. Verify the actual account/signing prerequisites rather than assuming every development test needs a paid account. Some hardware-specific features are unavailable in simulation. [Apple, Running your app on simulated or physical devices (R06).](#authoritative-technical-references)
- Define explicit physical observations for promised background/lock-screen audio controls, media visibility, backup exclusion, and any other OS integrations. Verify current platform capability; do not assume the source's two checks are the only hardware-dependent ones for every project.

### 13.4 Resource, lifecycle, and setup discipline

Budget actual RAM, CPU, storage, acceleration, backend load, and rendering capabilities before starting environments. Serialize heavy sessions if concurrent execution is infeasible. Source estimates of 8 GB/2 GB/16 GB and installer/boot durations are historical examples, not universal requirements.

Use a supported diagnostic/readiness check before creation. Document first-boot manual steps when applicable, persistent environment identity, start/stop, local access, and destructive removal separately. Never copy default VM passwords into a target runbook or retained evidence. Missing hardware/setup remains BLOCKED; optional cloud previews cannot replace locally authoritative required evidence under this profile.

## 14. Content, administration, and stateful workflows

Origins: [S07 all sections; S05 live upload/content coordinator; S01 §§2.2, 2.4, 2.9.](#source-register)

Apply only the modules the target product actually has. Produce or amend an operator-oriented content/runbook equivalent without leaking implementation detail into ordinary product screens.

### 14.1 Identity, staff provisioning, and scope

Distinguish end-user authentication/provisioning from staff authentication. A student/user creation form may not provision an operator account; document the actual supported route, password/credential prompts, and idempotent update behavior where provided.

Prefer least-privileged scoped operators to technical superusers. Define who may create/promote staff and grant exact scopes; test no-assignment behavior, permitted reads/writes, refusal outside scope, revocation during an existing session, and stale authority.

If authority is tied to time/context/entity combinations, document exact assignment, active-versus-historical edit rules, separate historical moderation permissions, and whether assignments carry forward. Do not assume rollover. Exceptional corrections require explicit authority and audit policy.

### 14.2 Moderation, removal, and restoration

Resolve report thresholds from approved policy; do not inherit the source's two-report threshold. If distinct reporters are required, enforce uniqueness. Determine whether even exceptional roles must meet eligibility. Test reversible visibility/removal, eligible staff inspection, restoration, retained history, and protection against duplicate reports or bypasses.

### 14.3 Membership, enrollment, progression, and correction

For stateful enrollment/progression or analogous workflows, specify authoritative invariants: membership creates required related records exactly once; all prerequisite outcomes exist before advancement; repeats/retries create only required follow-up records; terminal stages do not create phantom next-stage containers; final success records completion automatically when promised.

Define final versus provisional outcomes, failure boundary cases, idempotence, transactions, retries, exceptional correction with reason/history, and reconciliation of only records caused by the corrected outcome. Derive exact counts, hierarchy, stage limits, and graduation rules from the target's approved domain. The source's course/final-level rules are examples, not universal product behavior.

### 14.4 Hierarchy and supported operator surfaces

Document actual creation dependencies from parent to child and how to obtain stable identifiers. Identify supported operator pages for users, structure, material, links, reports, deactivation/reassignment, and moderation. Identify which file types can be uploaded in the official form and which require preprocessing; reject unsupported input clearly rather than allowing a delayed runtime failure.

### 14.5 Material ingestion and storage contracts

- Resolve supported formats, storage-key semantics, URL assembly, manifests, segments, MIME types, permissions, duration/page metadata, and rendering/playback clients. Do not impose HLS on a project that supports direct files or another protocol.
- Where HLS is required, distinguish a playlist/segment directory contract from a raw media-file key. Validate preprocessing and manifests before attachment. The source product expects a particular `master.m3u8` layout; HLS itself is not a universal mandate for that exact filename. [Source S07; RFC Editor, RFC 8216 (R07).](#authoritative-technical-references)
- Prefer an existing ingestion helper that validates, transforms/transcodes, uploads, and attaches coherently. Document inferred kind and explicit override, metadata extraction and optional tooling, replacement/update semantics, and where preprocessing tools run.
- Keep tools in the correct environment according to architecture; a host-side transcoder in the source is not a universal ban on containerized processing.
- Verify the API record and fetched content, referenced playlists/segments, actual playback/opening, and representative clients. HTTP success plus expected MIME type is a reachability precheck, not proof that a client can decode, play, download, or open it.
- Seed real representative media/assets where these behaviors are promised. Mock-only payloads cannot certify actual playback or offline storage.

### 14.6 Refresh, offline behavior, and testing authentication

Only expose active-context content according to approved rules. Test refresh after admin/operator changes, foreground/background transitions, context activation, simultaneous label/hierarchy updates, and closure of invalid descendant routes.

Test download controls, progress, completed play/open state, genuine airplane/offline behavior, and automatic recovery for new offline requests. Preserve approved localized feedback; do not hardcode the source's Arabic message in an unrelated project.

Use disposable local accounts and supported development authentication. If an existing debug OTP/login bypass is intentionally present, verify its production rejection and prevent capture in evidence. This profile does not authorize adding a universal bypass, copying the source's fixed OTP or phone number, or harvesting production login codes. Keep credentials/tokens/cookies out of commands and retained outputs.

## 15. Brand assets and derived visuals

Origins: [S08 all sections; S01 §§2.3, 2.6.](#source-register)

Apply when a project has shared identity assets. Do not invent a brand requirement for a product without one.

1. Identify the editable canonical source, shipped vector/export, and each derived raster/native representation. Define reproducible export commands, dimensions, tool versions, transparency, and ownership. Regenerate derived files when the canonical export changes; do not independently hand-edit them.
2. Preserve approved geometry, motif, stroke/outline structure, and seamless edge continuity where those are identity constraints. Color and opacity may vary only within approved tokens. Do not substitute the source's eight-point star for another project's identity.
3. Share assets/theme tokens across official client and operator surfaces where required. Centralize reusable tiling/tint components rather than duplicating styling logic.
4. Verify alpha masking/tint behavior, vector rendering, light/dark variants, fallback colors, transparency, seams, scale, and accessibility on actual supported renderers. Do not assume embedding styles cross isolated asset boundaries; test the chosen delivery mode.
5. Record surface-specific colors, opacity, tile size, units, and reading constraints in a design-token/surface table. Keep decoration faint enough for readability and large enough for its geometry to remain legible, using project-specific rendered evidence.
6. The source's 600×600 raster, 150/200 px, 150/180 dp, 4.5/18/13/10% opacity, approximate 120 px legibility floor, and green/gold/cream choices remain attributed examples in Appendix A. They are not generic design defaults or validated thresholds for another asset.
7. Validate regenerated exports and affected surfaces in the same coherent unit. Preserve editable provenance and explain intentional format differences.

## 16. Adoption audit and validation

Origins: [S01 §9; S02 all conformance/validation sections; S03 automation boundaries.](#source-register)

### 16.1 Mandatory report

Create or update `docs/spec-kit-adoption.md` (or the explicit repository equivalent). Include actual project context, previous/new constitution/profile versions, dates, scope, installed integrations, working branch, preserved history, conflicts/decisions, synchronization, validation commands/results, staged review/commit, next phase, and application-certification boundary.

Use one row for every numbered section/subsection and every command subsection in this profile. Split rows further so every applicable MUST is explicitly accounted for; a section-level PASS cannot conceal a missed requirement. Include source-heading retention coverage for all eight supplied documents, using section 18 and Appendix A.

```markdown
| Rule / section | Applicability and reason | Implemented in | Validation / evidence | Status |
|----------------|--------------------------|----------------|-----------------------|--------|
| <specific rule> | <applicable or concrete reason> | <actual files> | <content inspection or completed check> | <PASS/FAIL/BLOCKED/N/A> |
```

Adoption-row statuses are PASS, FAIL, BLOCKED, N/A. N/A requires a concrete product reason and is forbidden for universal rules. An applicable unvalidated rule is BLOCKED with the missing validation identified; never optimistic PASS. Individual application checks continue using section 7's statuses, including NOT RUN.

### 16.2 Required validation checklist

- [ ] Actual project/phase/feature(s), branch, user changes, and integration versions were inspected.
- [ ] Spec Kit initialization exists; any required supported initialization completed safely.
- [ ] All normative sections and applicable MUST rules map to implementation and evidence.
- [ ] All eight sources and their headings are preserved/adapted, with no omitted product-specific detail masquerading as a generic default.
- [ ] Existing constitution and ratification were preserved; semantic bump/amendment and Sync Impact Report are justified.
- [ ] No unexplained concrete-governance placeholders remain.
- [ ] Ownership, authorization, UI/localization, data, simplicity, DRY, verification, reproducibility, staff scope, and engineering rules are concrete or legitimately N/A.
- [ ] Spec/plan/tasks/checklist templates implement the artifact contract; verification has a supported template/guide.
- [ ] All active installed integrations implement their applicable behaviors; required frontmatter and syntax remain valid.
- [ ] Authoritative integration source templates, workflow definitions, hooks, and supported manifest/checksum metadata are synchronized.
- [ ] Analyze remains read-only; converge writes only appended deduplicated tasks; the enclosing workflow records its result correctly.
- [ ] Verification/convergence and honest repair handoff exist in the lifecycle.
- [ ] Root/layer runtime guidance names actual full quality gates and working directories.
- [ ] Local feature-qualified task conventions exist; external conversion/services are not completion gates.
- [ ] Reproducibility pins/locks, secrets/evidence rules, and supported local environment guidance are present.
- [ ] Applicable native/live/content/brand guides preserve required operational behavior with target-specific values.
- [ ] Existing IDs, checkboxes, decisions, superseded features, and historical evidence were preserved.
- [ ] Content—not just path existence—was inspected in synchronized files.
- [ ] Relevant syntax/schema/link/placeholder/workflow/integration checks passed.
- [ ] Complete actual gate commands remain invocable; dry-run validation is labeled as such, not test execution.
- [ ] Diffs/staged paths were reviewed; no unrelated edits, secrets, or whitespace errors remain.
- [ ] Documentation/configuration checks appropriate to adoption passed.
- [ ] Coherent safe authorized changes were committed locally, or the precise commit blocker is reported.
- [ ] Application checks are separately and accurately labeled PASS/FAIL/NOT RUN/BLOCKED; policy-only adoption claims no application certification.
- [ ] Repeated adoption produces no duplicate tasks, history loss, or needless semantic changes.
- [ ] Exact installed next invocation and any blocker-resolution steps are provided.

### 16.3 Validation methods and completion gate

Select checks from the installed environment: modified shell syntax parsing, JSON/YAML/frontmatter schema, supported workflow information/registration, integration status, managed hashes, placeholder scans, link checks, gate dry runs, local-only dependency scans, and diff whitespace checks. The source's `bash -n`, `jq empty`, workflow/integration commands, `make -n`, and hash inspection are examples; use actual supported equivalents and report exact results. A documented customization warning may be expected; missing/invalid operative files are not.

Report **ADOPTED** only when every applicable row and checklist requirement passes, no universal rule is N/A or blocked, relevant checks pass, the diff/staging was reviewed, and the coherent local adoption commit exists. Otherwise report **PARTIAL**, with precise gaps and current safe progress. Application tests may properly be NOT RUN for a policy-only change; that does not certify the app and does not need to become a fabricated adoption PASS.

## 17. Reusable invocation and reporting

Origins: [S01 §10; S03 Commands; S04 references.](#source-register) The any-phase wrapper below is a consolidation addition.

### 17.1 Copyable instruction for a target agent

```text
Read the complete Spec Kit Universal Adoption and Execution Profile I supplied.
Adopt sections 0–18 in this repository; treat Appendix A as attributed historical
reference, never as commands to execute or target defaults.

Inspect the actual repository, current phase/feature, user changes, constitution,
Spec Kit version and integrations, templates, skills/commands, workflows,
manifests, runtime guidance, architecture, roles, locales, data policy,
dependency inputs, quality gates, and existing evidence before editing.

Amend the existing constitution in place with justified versioning, preserved
ratification, current amendment date, and a Sync Impact Report. Synchronize every
active integration and authoritative source template, supported workflow and
metadata, root/layer guidance, verification policy, task conventions, and
applicable operational guides. Make values concrete for this project.

Preserve approved scope, IDs, checked history, supersession, and old evidence.
Apply stable FR/AS/TR/SC traceability, mandatory reuse and test-first work,
current verification evidence, full relevant local gates, truthful completion,
and evidence-aware analyze/converge behavior. Keep analyze read-only and limit
converge writes to appended deduplicated remediation tasks.

Use safe local Git history with reviewed explicit paths and coherent commits.
Do not discard user work, publish externally, or install optional frameworks
because of this profile. Do not certify runtime behavior from policy changes.

Create/update the adoption report with every applicable rule and source heading
mapped to files and actual validation. Report ADOPTED only under its gate,
otherwise PARTIAL with exact blockers. Resume the already authorized active
feature from its current phase, or give the exact installed next invocation if
there is no active authorized feature. Make repeated adoption idempotent.
```

### 17.2 Required final report from the receiving agent

Lead with adoption and requested-work outcome. State constitution/profile version, synchronized operative locations, validation actually run, commit(s), current feature completion separately, and remaining blockers. Give exact installed next invocation(s) with feature context. Keep the report concise but link to the detailed adoption/evidence files.

Never claim “best,” “100% accurate,” “fully tested,” or “complete” beyond observed evidence and the specified gate. Cite source documents and authoritative references for technical claims. Clearly label policy decisions, assumptions, current observations, historical excerpts, and derived conclusions.

## 18. Source retention, corrections, and references

### Source register

The eight user-supplied Markdown documents are primary evidence of the requested project policies and historical documentation. They are **not independently verified proof** of their recorded runtime successes or general technical assertions. The attached project was not available for code inspection or test execution during this consolidation. All original text is retained in Appendix A, with a SHA-256 integrity record for each snapshot. Normative decisions in this document are policy prescriptions, not empirical performance claims.

| ID | Supplied filename | Preserved snapshot | Main normative destinations |
|----|-------------------|--------------------|-----------------------------|
| S01 | `portable-speckit-standard.md` | [S01 snapshot](#source-s01) | §§0–11, 16–17; governance, commands, quality, commits, migration |
| S02 | `spec-kit-adoption.md` | [S02 snapshot](#source-s02) | §§1–2, 5, 11, 16; resolved context, conformance and actual validation pattern |
| S03 | `spec-kit-testing.md` | [S03 snapshot](#source-s03) | §§4–8, 11, 17; artifact/evidence semantics, loop, BDD |
| S04 | `issue-conventions.md` | [S04 snapshot](#source-s04) | §§4.1, 10–11; feature-qualified local task identity/history |
| S05 | `live-testing.md` | [S05 snapshot](#source-s05) | §§6–7, 12–14; local runtime strategy, media/offline/upload, fixtures, teardown |
| S06 | `native-testing.md` | [S06 snapshot](#source-s06) | §§6, 12–13; compile/runtime/device distinction, tooling, resources, lifecycle |
| S07 | `adding-content.md` | [S07 snapshot](#source-s07) | §§3, 12, 14; administration, progression, media ingestion, refresh, login, offline |
| S08 | `brand-pattern.md` | [S08 snapshot](#source-s08) | §§3.3, 3.6, 15; canonical/derived visuals, geometry, theme, surface constraints |

### 18.1 Detailed source-heading retention map

| Source and source headings | Retention/adaptation |
|----------------------------|----------------------|
| S01 Purpose / Required outcome | Full adoption rather than summary; no accuracy guarantee; intent-to-evidence chain; §§0, 2, 4–8 |
| S01 §1 Discover | Complete discovery table and target-specific values; §1 |
| S01 §§2–2.9 Constitution | In-place versioning/report and all nine principles; §3. All concrete Rewaq choices remain examples. |
| S01 §3 IDs / spec / plan / tasks / checklists / verification | Stable aliases, folder contract, matrix, tests-first tasks, quality-only checklists, complete evidence template; §§4, 7 |
| S01 §4 and all nine named command subsections | Integration-specific synchronization and distinct permissions/behaviors; §5. Missing capabilities require supported equivalents, not claims. |
| S01 §5 Completion | Binary gate and implement/verify/converge repair loop; §8 |
| S01 §6 Migration | Historical preservation, remediation, supersession, no invented intent; §11 |
| S01 §§7–7.7 Engineering | All style/reuse, execution, documentation, local Git, security, formatting/types, dependencies rules; §§9–10 |
| S01 §8 BDD / coverage | Optional tooling and structural-validator limits; §6.4 |
| S01 §9 Adoption | Per-rule conformance, content inspection, checks, local commit, no false app proof; §16 |
| S01 §10 Reusable instruction / upgrade note | Complete any-phase invocation and drift prevention; §§11.2, 17 |
| S02 Resolved context | All variables retained in generalized discovery; §1.1; original exact table in Appendix A |
| S02 Conformance map | All numbered principles, artifact/command and engineering rows represented in §§2–16; new adoption report must contain actual target results |
| S02 Validation checklist | Ratification, justified bump, sources, syntax, metadata, local workflow, local task identity, diff/commit and no runtime certification; §16 |
| S02 Validation evidence | Shell/JSON/hash/workflow/integration/dry-run/placeholder/local-service-dependency/diff checks are examples in §16.3, not copied PASS |
| S02 Historical/migration | Author provenance vs dependencies, historical evidence, superseded feature, current active migration selection, preserved iOS scope; §§11, 13 |
| S03 Artifact purposes / IDs | Complete FR/AS/TR/SC roles, assertion inspection, scoped allowed/refused example, service/interface distinction; §§4, 6 |
| S03 Evidence format | All fields, statuses, counts, local/compressed sanitization, freshness, observations and convergence; §7 |
| S03 Commands / existing feature / gates | Correct installed agent syntax, retained feature context, migration entry, complete root/mobile/plugin/device gates; §§1, 5–6, 11, 17 |
| S03 BDD/automation | Optional framework, no invented validator, no retroactive certification, local authority; §§0, 6.4, 16 |
| S04 Canonical reference / Local workflow | All task numbering, cross-feature qualification, history, append-only IDs, evidence separation and reviewed local commits; §§4.1, 10 |
| S05 Strategy / Prerequisites | Local compile vs rendered/device, optional previews, pinned local SDK, realistic seed/services, physical OS checks; §§12–13 |
| S05 Android Path A | API/media URL topology, prechecks, bounded emulator helpers, RTL/rendering evidence, real offline use, isolated coordinator; §12 |
| S05 iOS Path B | Exact inputs, local analysis/unit/build, reachable backend, working rendering, cross-platform offline, explicit BLOCKED; §13 |
| S05 Upload / Recorded run | Allowed/refused scopes, server and UI outcomes, negative-target fixtures, visible denial message; §§6.1, 12.2, 14.1. Exact dated log/status and repaired task retained only as historical source text. |
| S05 Teardown / SC mapping | Stop/reset/dispose test-owned data, separate visible/offline/upload/reachability/reproducibility criteria; §§12.4–12.5 |
| S06 Intro/platform status/RAM | Native harness limits, actual capability matrix, resource-aware serial sessions; §13 |
| S06 Android/local commands | Pin inputs, readiness/device discovery, host addressing, package/static/integration gates; §13.2 |
| S06 iOS host prep/first boot/toolchain | Supported authorized environment, diagnostics, manual setup, persistent lifecycle, local transfer, dependencies/Xcode, network, build vs simulator; §§13.3–13.4. Original Docker-OSX recipe archived, not prescribed. |
| S06 Expectations / Quick reference | Separate compile/rendered/physical evidence, missing resources BLOCKED, start/wait/stop and destructive remove distinction; §13 |
| S07 First fact / create / staff | Actual media-key contract, operator/student identities, idempotent provisioning, least privilege, exact scopes, revoke/rollover/historical rules; §§14.1, 14.4–14.5 |
| S07 Reports/removal | Distinct-report threshold, exceptional roles, reversible hide/restore; §14.2; exact source threshold in archive |
| S07 Enrollment/progression | Create-once related records, complete outcomes, constrained repeats/terminal stage, graduation, reasoned historical correction/reconciliation; §14.3; exact academic numbers in archive |
| S07 Hierarchy / Admin pages | Dependency order, stable IDs, supported pages/form kinds, direct PDF versus preprocessing; §§14.4–14.5 |
| S07 Attach | Existing ingestion helper, format inference/override, metadata/page count, idempotent replacement, transcode location; §14.5 |
| S07 Check / active context / coordinator | API/material prechecks, actual playback, active context, refresh/resume and stale descendants, isolated credential-safe E2E; §§12.2–12.3, 14.5–14.6 |
| S07 Download E2E | Progress/control transition, actual offline playback, offline new request and reconnect recovery; §§12.2, 14.6 |
| S07 Real phone / Logging in | Reachable device endpoints, build-time URLs, optional authorized tunnel and teardown, test-only login and production rejection; §§12.4, 14.6; original OTP/phone remain source data only |
| S08 Identity / Three files | Approved canonical geometry/seamless joins, editable/vector/raster provenance, regeneration command pattern, alpha tint; §15 |
| S08 Colour / Surface table / constraints | Embedding/theme/fallback validation, shared component, surface color/opacity/unit/scale table, readability/legibility; §15. All exact source values retained in archive. |

### 18.2 Corrections and unresolved historical claims

1. **Media precheck is not playback proof.** S07 equates HTTP 200 plus playlist MIME with playback. This profile requires actual client playback/opening and relevant manifest/segment checks. RFC 8216 defines playlist and media-segment relationships; the need for runtime evidence is the testing policy's derived conclusion, not a quote from the RFC. [RFC Editor, RFC 8216 (R07); S03 meaningful assertions.](#authoritative-technical-references)
2. **Standalone Command Line Tools are not the complete iOS build/simulator toolchain.** S06 offers them as an alternative for CLI builds. For the iOS work described, use compatible full Xcode and its required SDKs/runtimes. Apple lists `xcodebuild` and `simctl` among tools that ship only with Xcode. [Apple, R04–R05.](#authoritative-technical-references)
3. **Actual offline state must be verified.** S05's cellular-disable example alone does not establish that all transport is absent. Section 12 requires actual network isolation and local playback, derived from the source's offline acceptance promise; it does not prescribe a universal device command.
4. **Historical workstation capability is not a platform guarantee.** S05 records a VM graphics limitation; S06 contains broader simulator expectations and an older cloud-preview cross-reference. Use the target capability matrix and explicit BLOCKED outcomes, preserving local authority. Simulator/hardware adequacy must match the claim. [Apple, R06; S05–S06.](#authoritative-technical-references)
5. **A virtualization recipe is not support or legal authorization.** S06's non-Apple macOS approach remains archived. This profile requires checking supported/licensed target options; it provides no legal conclusion or authorization to copy that setup.
6. **Recorded PASS/fixes remain attributed historical claims.** The adoption report, Android upload run, build/boot timings, source account credentials, exact feature priorities, source framework versions, and source author fields were not independently re-executed/verified. They must not become current target evidence.
7. **Source defaults are not universal policy.** Exact roles, Arabic/RTL, HLS, soft deletion, report thresholds, progression limits, colors, geometry and tile-size claims remain in the appendix. Their transferable invariants are normative only when the target product requires the module.
8. **Integration syntax is version-dependent.** Agent invocations are not shell commands; verify the installed integration. Missing converge or another required behavior is a capability gap to resolve or hand off honestly. [GitHub Spec Kit, R01–R02.](#authoritative-technical-references)
9. **Converge write limits are retained.** Its report is returned to the caller; any verification-record update belongs to the enclosing implement/verify workflow. This reconciles the original append-only command rule with the evidence template without silently allowing extra converge mutations.

### Authoritative technical references

These primary references were checked when preparing this file. They support the specific technical claims above, not a claim that this policy has been empirically proven to maximize agent performance. Recheck applicable official guidance against the installed versions when adopting.

| ID | Organization / publication | Link and purpose |
|----|----------------------------|------------------|
| R01 | GitHub, Spec Kit Documentation | [Spec-Driven Development Quickstart](https://github.github.com/spec-kit/quickstart.html): phase workflow and integration invocation guidance |
| R02 | GitHub, Spec Kit Documentation | [Extensions](https://github.github.com/spec-kit/reference/extensions.html): optional capabilities, registration, initialized-project prerequisites and version-aware integration behavior |
| R03 | Google, Android Developers | [Network address space](https://developer.android.com/studio/run/emulator-networking-address): emulator topology and host-loopback alias |
| R04 | Apple Developer Documentation | [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference): Xcode-only tool requirements |
| R05 | Apple Developer Documentation | [Installing the command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools): standalone package scope |
| R06 | Apple Developer Documentation | [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices): simulator/physical capabilities and account setup |
| R07 | RFC Editor, R. Pantos and W. May (Informational, Independent Submission) | [RFC 8216, HTTP Live Streaming, §§3–4 and 6](https://www.rfc-editor.org/rfc/rfc8216.html): playlists, media segments, and client/server protocol responsibilities |

## Appendix A: all eight original source snapshots

**Reference-only archive.** The blocks below reproduce the supplied source bytes as UTF-8 text. They preserve all source detail, including product-specific examples and historical claims. Their relative links refer to the original repository, not this standalone file; use the source register and normative sections above for navigation and target application. Do not execute archived commands, reuse archived credentials, or treat archived PASS as current evidence. Where a source claim conflicts with sections 0–18, use the normative profile and the stated correction.

### Source S01

Source: user-supplied `portable-speckit-standard.md`. Original bytes: 36585. SHA-256: `2fbe8a3628e50f2d3be7f4ce67d12fb2d0b3538e0b8d7686368954651098a60f`.

````markdown
# Portable Spec Kit Standard

**Profile version**: 3.0.0

**Source snapshot**: Rewaq constitution 4.0.0 and repository workflow through
commit `c8cc9ac`, plus the Global Engineering Rules and solo local-version-control
policy adopted with profile 3.0.0

## Purpose

This document is a reusable installation brief for a new or existing Spec Kit
project. Copy this file into the target repository and ask the coding
agent to apply it. It captures the complete working method developed in this
repository: constitution governance, artifact traceability, test-first delivery,
evidence-based completion, convergence, safe migration of old features,
multi-layer ownership, authorization, accessibility, reproducibility, mandatory
DRY/reuse, mandatory local version control, and repository hygiene.

This is not a replacement for `specify init`. Initialize Spec Kit first, then
apply this standard to the generated project. Do not blindly copy product or
technology names from another repository.

This entire file is normative. An adopting agent MUST read it completely and
implement every applicable MUST rule; it may not select only the testing section
or summarize away operational requirements. Literal “100% accuracy” cannot be
guaranteed by a prompt or agent. Instead, this standard makes conformance
auditable: the agent MUST create `docs/spec-kit-adoption.md`, map every section
of this file to changed files and validation evidence, and MUST NOT claim full
adoption while any applicable item is missing, unverified, or blocked.

## Required outcome

After adoption, the project MUST have one coherent chain:

```text
product intent
    → constitution
    → FR-* functional requirements
    → AS-* acceptance scenarios
    → TR-* test requirements
    → dependency-ordered test and implementation tasks
    → executable tests and required human/device observations
    → verification.md evidence
    → convergence review
    → DONE or NOT DONE
```

An implementation task, commit, checklist, test filename, or static code review
does not by itself prove that a feature works.

## 1. Discover the target project before changing it

The adopting agent MUST inspect the repository and resolve these values. It MAY
infer an answer when the repository makes it unambiguous; otherwise it MUST ask
only questions that materially affect implementation or verification.

| Variable | Meaning | Example only |
|----------|---------|--------------|
| `<PRODUCT>` | Product or service name | Learning platform |
| `<LAYERS>` | Backend, clients, staff UI, libraries, infrastructure | Django API + Flutter app |
| `<OWNER_BY_LAYER>` | Which layer owns each responsibility | Server owns authorization |
| `<USER_GROUPS>` | End users, staff roles, operators, service accounts | Student, scoped staff, superuser |
| `<LOCALES>` | Default languages and layout directions | Arabic and RTL |
| `<DATA_POLICY>` | Retention, deletion, archive, and external-data rules | Soft deletion |
| `<QUALITY_GATES>` | Exact full commands and working directories | `make check` |
| `<DEPENDENCY_POLICY>` | Lock files, image pins, supported toolchain | Digest-pinned images |
| `<API_CONTRACT_PATH>` | Canonical API documentation, if applicable | `docs/api.md` |
| `<AGENT_FILES>` | Installed Spec Kit command/skill locations | `.agents/skills/` |
| `<DEFAULT_BRANCH>` | Branch used for ordinary work | Current checked-out branch |

Do not impose Django, Flutter, Arabic, a staff console, soft deletion, or any
other product choice on a project that does not require it. The principles below
are portable patterns; their concrete values come from the target project.

## 2. Constitution requirements

Use `speckit-constitution` to amend the existing constitution. Do not replace an
existing constitution with a generic copy. Preserve its ratification date,
record today's amendment date, use semantic versioning, and prepend a Sync
Impact Report listing changed principles, synchronized files, and follow-up work.

The constitution MUST make the following principles explicit. A genuinely
inapplicable product module may be recorded as not applicable with a concrete
reason. DRY/reuse, verification, reproducibility/secrets, simplicity, and the
repository-wide engineering rules are universal and cannot be marked N/A.

### 2.1 Layer ownership and sequencing

- Assign one authoritative owner for data shape, authentication, authorization,
  and business invariants.
- Define each client or interface's audience and trust boundary.
- Sequence cross-layer work from the authoritative contract/provider toward its
  consumers.
- Keep interfaces for different trust audiences separate unless the plan records
  a validated reason to combine them.
- Require API or public-library contracts to change in the same unit as the
  behavior they describe.
- Permit mocks only behind a replaceable boundary; swapping the mock for the real
  dependency must not require rewriting consumers.

### 2.2 Server-side or authoritative authorization

- Enforce permissions at the trusted boundary, never only by hiding controls.
- Give every state-changing path an explicit authorization decision.
- Define roles, scopes, ownership, inactive/revoked behavior, and exceptional
  authority in the specification.
- Test allowed and relevant rejected paths through the actual exposed interface.
- Assert that refused operations leave no unauthorized side effects.

For a non-server project, “trusted boundary” means the authoritative component
that can actually enforce the rule, not whichever UI happens to display it.

### 2.3 Accessible, localized, task-oriented interfaces

- Record the default locale, text direction, accessibility baseline, supported
  platforms, and target user capabilities.
- Require clear task-oriented labels, visible state, adequate contrast and target
  sizes, shallow navigation, keyboard/screen-reader behavior where relevant, and
  explicit loading, empty, error, and recovery states.
- Validate promised layout and usability through the appropriate rendered UI,
  browser, simulator, device, accessibility tool, or staff walkthrough.
- Do not treat a string-existence unit test as proof of layout or usability.

### 2.4 Data preservation and deletion policy

- Define which records are immutable, archived, soft-deleted, hard-deletable, or
  governed by retention rules.
- Define ownership and moderation thresholds for shared content.
- Identify externally hosted data that cannot carry the same preservation
  guarantee, label that exception everywhere users see it, and retain the local
  reference according to policy.
- Keep exceptions narrow, explicit, derived where possible, and testable.

This module is mandatory when the product stores user, historical, regulated, or
shared content. Its concrete policy is a product decision, not a Spec Kit default.

### 2.5 Simplicity and non-goals

- Preserve explicit non-goals as scope boundaries.
- Do not construct speculative infrastructure or future applications without an
  active, approved specification.
- Prefer the smallest architecture that meets the validated requirements.
- Record justified constitutional exceptions in the plan's Complexity Tracking
  section; an exception cannot silently waive testing or security gates.

### 2.6 DRY and reusable design

DRY is mandatory: each piece of domain knowledge, validation, authorization,
configuration, transformation, or user-interface behavior MUST have one
authoritative implementation. Before adding code, the agent MUST search for an
existing helper, service, component, hook, validator, serializer, policy,
fixture, or utility and reuse or extend it when its contract matches.

- Centralize security and business invariants. Two write paths MUST NOT maintain
  independent copies of the same rule.
- Extract genuinely shared behavior into a focused reusable component with a
  clear name, stable interface, and direct tests.
- Prefer composition and small cohesive units over copying and editing a large
  implementation.
- Parameterize only real, observed variation. Do not build a speculative generic
  framework for one use case.
- Similar-looking code that represents different business rules MUST remain
  separate; DRY applies to shared knowledge and behavior, not incidental syntax.
- Reuse MUST preserve layer ownership and dependency direction. A shared module
  must not create a circular dependency or leak a trusted rule into an untrusted
  client.
- When duplication is intentionally retained, the plan or code review MUST state
  the different semantics that make sharing unsafe.
- Refactoring for reuse MUST keep behavior stable and pass all affected tests.

Reusable UI components MUST expose the variants actually needed by their
consumers, use the project's design/theme tokens, preserve accessibility and
localization behavior, and avoid duplicated styling or interaction logic.

### 2.7 Requirements are verified before completion

- Every `FR-*` and `AS-*` MUST map to one or more `TR-*` requirements with
  meaningful observable assertions.
- Every user story MUST cover its specified positive, negative, boundary,
  authorization, failure, and recovery behavior.
- Tests for new behavior MUST be written before or alongside implementation and
  run first to establish the expected behavioral failure.
- Existing correct behavior MAY reuse an existing test and establish a passing
  baseline; never break it artificially to manufacture a red test.
- A broken harness, unavailable service, missing device, or missing credential is
  BLOCKED, not the expected red state and never PASS.
- Do not delete, weaken, skip, or change expected behavior merely to make a test
  green. A demonstrably defective test may be corrected only against unchanged
  approved intent, with the reason recorded.
- Run focused tests while repairing, then run all relevant regression suites and
  layer quality gates on the final state.
- Use human, visual, accessibility, performance, browser, or physical-device
  evidence when automation alone cannot prove the promised outcome.
- Do not replace behavioral coverage with a blanket code-coverage percentage.

### 2.8 Reproducible environments and secrets

- Pin language dependencies in committed lock files.
- Regenerate locks whenever dependency declarations change.
- Pin container images by immutable digest and tools by explicit version; do not
  use floating `latest` tags for repeatable gates.
- Document one supported way to run each complete quality gate.
- Require every supported local environment to use equivalent dependency inputs.
- Keep credentials, signing keys, tokens, personal data, and unrestricted dumps
  out of commits and verification evidence.
- Document configuration variable names in an example environment file without
  adding values or secrets.

### 2.9 Scoped staff or operator administration

When the product has ordinary staff and technical superusers:

- Ordinary staff MUST see and change only data within explicitly assigned scopes.
- The trusted backend MUST filter reads, choices, related-object selectors,
  direct URLs, form submissions, bulk actions, and writes by the same scope.
- Revoked, inactive, forged, cross-scope, and stale assignments MUST be rejected.
- A technical superuser MAY retain cross-scope and exceptional-correction powers,
  but those powers and audit expectations MUST be explicit.
- The official staff interface MUST be identified. Do not build a separate staff
  application until validated workflows demonstrate that the current interface
  cannot serve them clearly, safely, or efficiently.
- Test real staff requests/forms/actions. Service tests alone do not certify the
  staff interface.

If the project has no staff/operator interface, mark this module not applicable
in the constitution rather than inventing one.

## 3. Stable identifiers and artifact contract

Identifiers are local to a feature directory:

- `FR-001`: functional requirement.
- `AS-001`: acceptance scenario.
- `TR-001`: test requirement.
- `SC-001`: measurable success criterion.
- `T001`: implementation task.
- `CHK001`: requirements-quality checklist item.

Cross-feature references MUST include the feature number, such as
`012/FR-004`. Never silently renumber existing IDs. Preserve legacy IDs and map
them through stable aliases when retrofitting an existing specification.

Every feature directory SHOULD contain:

```text
specs/NNN-feature/
├── spec.md
├── plan.md
├── research.md             # when planning needs it
├── data-model.md           # when data is involved
├── contracts/              # when public contracts are involved
├── quickstart.md           # executable/manual acceptance walkthrough
├── tasks.md
├── verification.md         # planned checks and actual evidence
└── checklists/             # quality of requirements, not test results
```

### `spec.md`

MUST include prioritized, independently testable stories; globally unique `AS-*`
IDs within the feature; explicit edge cases; `FR-*`; `TR-*`; a complete
FR/AS-to-TR Verification Matrix; measurable `SC-*`; assumptions/dependencies;
and a binary Completion Gate. Classify success criteria as release gates or
post-launch measurements. Never invent future business results.

### `plan.md`

MUST identify the real project paths, technical boundaries, fixtures,
prerequisites, test layers, exact commands/selectors, full regression scope,
required manual/device/browser evidence, performance methods, and where each TR
will be implemented. It MUST initialize or preserve `verification.md` with
planned checks marked NOT RUN; it must never predeclare a pass.

### `tasks.md`

MUST be dependency ordered and grouped by story. Each story uses:

```text
acceptance/behavioral tests
    → supporting unit/integration tests
    → implementation
    → focused verification and repair
    → related regression verification
```

Every test and verification task includes its FR/AS/TR IDs and concrete paths or
selectors. The final phase runs all relevant suites, records evidence, reconciles
all mappings and success criteria, and performs convergence. Tests are not
optional. Parallel markers may be used only for work that is truly independent.

### `checklists/*.md`

Checklists are “unit tests for the written requirements.” They ask whether the
requirements are complete, clear, consistent, measurable, and cover the needed
scenarios. They MUST NOT contain implementation checks such as “the API returns
200” or “the button works.” A checked checklist never proves the code works.

### `verification.md`

This is the execution record. It MUST identify the tested revision or working
tree fingerprint, date, environment, platforms/devices, exact commands, working
directories, exit codes, pass/fail/skip/xfail counts, per-TR results, required
observations, gaps, and convergence outcome. Use only PASS, FAIL, NOT RUN, or
BLOCKED for individual checks. Historical evidence remains labeled with the
state it tested; changed behavior requires fresh evidence.

Use this portable structure:

```markdown
# Verification: <feature>

Constitution: <version>
Completion: NOT DONE
Tested revision / working-tree fingerprint: <value>
Date: <YYYY-MM-DD>
Environment: <dependencies, services, OS/browser/device>

## Coverage

FRs with meaningful assertions: <covered>/<total>
ASs with meaningful assertions: <covered>/<total>
Required TRs passing: <passing>/<total>

| FR / AS | TR | Executable selector | Status | Evidence |
|---------|----|---------------------|--------|----------|
| <IDs> | <TR> | <test path/node ID/description> | NOT RUN | <reason> |

## Execution

| Working directory | Exact command | Exit code | Passed / failed / skipped / xfailed | Evidence |
|-------------------|---------------|-----------|------------------------------------|----------|
| <path> | <command> | NOT RUN | NOT RUN | <reference> |

## Additional acceptance evidence

| Scenario / SC | Method and platform | Expected | Observed | Status / evidence |
|---------------|---------------------|----------|----------|-------------------|
| <ID> | <walkthrough/measurement> | <outcome> | Not observed | NOT RUN |

## Remaining gaps

<missing tests, failures, blockers, and remediation task IDs>

## Convergence

<date, assessed state, outcome, findings, and task IDs; initially NOT RUN>
```

Do not record secrets or unnecessary personal data.

## 4. Required behavior of each Spec Kit command

Apply these rules to every installed integration, including skill-based and
command-based integrations. Preserve integration-specific frontmatter and syntax
while keeping the substantive behavior synchronized.

If the installation includes a reusable workflow definition, synchronize it as
well. Where the workflow engine supports the needed steps, its lifecycle SHOULD
be specify → review/clarify → plan → review → tasks → analyze → implement →
verify → converge. If it cannot express the repair loop, it MUST stop with an
honest outcome and print the exact implement/converge command to run next rather
than declaring completion after implementation alone.

### `speckit-constitution`

- Update the existing constitution in place.
- Use semantic versioning and preserve the original ratification date.
- Prepend a Sync Impact Report.
- Propagate changed rules to templates, all installed Spec Kit commands/skills,
  runtime agent guidance, and relevant project documentation.
- Validate placeholders, dates, headings, declarative language, and consistency.

### `speckit-specify`

- Create the spec template only when `spec.md` does not exist.
- When updating, preserve existing requirements, IDs, history, dependencies,
  supersession decisions, and approved product decisions.
- Generate stable AS, FR, TR, and SC IDs, the Verification Matrix, and Completion
  Gate.
- Keep the spec implementation-agnostic while making outcomes testable.

### `speckit-clarify`

- Ask at most five high-impact questions, one at a time.
- Prefer recommendations grounded in repository context.
- Write each accepted answer into the spec immediately and remove contradictions.
- Re-evaluate the requirements-quality checklist after updates.
- Clarify behavior and acceptance intent, not minor implementation preferences.

### `speckit-plan`

- Run the Constitution Check before and after design.
- Plan traceable tests for every FR and AS at the smallest useful layer.
- Include actual interface tests where the promise is made.
- Name exact commands, paths, fixtures, external services, browsers/devices, and
  measurable performance conditions.
- Identify existing reusable helpers/components and the authoritative home of
  each shared invariant. Justify any intentional semantic duplication.
- Create or preserve `verification.md`, initially NOT RUN.

### `speckit-tasks`

- Treat tests as mandatory.
- Map every FR and AS through TR IDs to concrete test work.
- Put tests before implementation and verification after it.
- Include an explicit pre-implementation reuse search and, when duplication
  exists, focused extraction/refactoring tasks with regression coverage.
- Include the complete quality gates and convergence in the final phase.
- Never create a story-completion task that lacks complete test coverage.

### `speckit-analyze`

- Remain read-only.
- Check constitution, spec, plan, and task consistency.
- Independently measure FR coverage, AS coverage, TR coverage, and task coverage;
  do not hide one missing dimension inside an overall percentage.
- Inspect the actual assertions and planned interface, not only matching IDs.
- Flag duplicated business/security rules, unnecessary parallel components, or
  plans that ignore an existing suitable abstraction.
- Treat a missing required test mapping as critical.
- Distinguish expected NOT RUN status before implementation from a false or stale
  completion claim after implementation.
- Report ambiguities and decisions needed without changing files.

### `speckit-implement`

- Read spec, plan, tasks, and verification evidence together.
- Establish the existing baseline, then follow test → expected RED → implement →
  run → diagnose → fix → rerun for new behavior.
- Search the repository before adding helpers/components; reuse or extend the
  authoritative implementation and remove newly introduced semantic duplication.
- Continue independent work when one scenario has an external blocker.
- Never change approved acceptance intent silently.
- Record actual results only after commands exit.
- Mark a task complete only when its associated verification passes.
- Run full relevant gates on the final state.
- Perform a convergence review and iterate on in-scope remediation until clean or
  genuinely blocked. A narrow task request must not be reported as whole-feature
  completion.

### `speckit-converge`

- Compare the current code, meaningful test assertions, and current evidence with
  spec, plan, and tasks.
- Check DRY/reuse explicitly, especially duplicated authorization, validation,
  domain invariants, configuration, and UI interaction/styling behavior.
- Do not modify implementation or specification artifacts.
- Its only permitted write is appending deduplicated remediation tasks to
  `tasks.md`.
- If an open task already describes a gap, cite it instead of duplicating it.
- Preserve checked task history; append a remediation task for an unsupported
  old completion claim.
- Report exactly one outcome:
  - `tasks_appended`: uncovered work was appended.
  - `gaps_remaining`: existing open work or missing evidence remains.
  - `converged`: no gaps remain and all required current verification passes.
- “No new tasks” is not synonymous with “converged.”

### `speckit-checklist`

- Validate requirement quality only.
- Preserve existing checklists and append uniquely numbered `CHK*` items.
- Never use checklist completion as implementation evidence.

## 5. Completion algorithm

Use this loop for every feature:

```text
speckit-specify
    → speckit-clarify
    → speckit-plan
    → speckit-tasks
    → speckit-analyze
    → speckit-implement
    → execute focused and full verification
    → speckit-converge
        ├── tasks_appended/gaps_remaining → implement and verify again
        └── converged                    → DONE
```

A story is DONE only when all of its required FR/AS/TR verification passes,
applicable release success criteria are met, related regressions pass, and its
required observations are complete. A feature is DONE only when every story is
done, all affected layer gates pass on the final state, evidence is current, and
convergence finds no gaps. Otherwise it is NOT DONE. Draft, In Progress, and
Blocked are useful workflow states but never aliases for DONE.

## 6. Existing-feature migration

Do not retroactively mark existing features as compliant merely because this
standard was installed.

1. Preserve old task checkboxes, identifiers, evidence, and decisions as history.
2. Run analyze and converge against the current implementation.
3. If intent or mappings are missing, update the spec and plan before generating
   new tasks; convergence must not invent product behavior.
4. Append traceable remediation tasks for missing tests, stale evidence, or
   unsupported completion claims.
5. Re-run implement and convergence until the current state meets the gate.
6. Keep explicitly superseded features historical. Record which newer feature
   replaces them and do not reactivate them during a broad audit.
7. Retrofitting verification must not reopen already approved product decisions
   unless implementation evidence exposes an actual contradiction.

## 7. Mandatory repository-wide engineering rules

These are default rules for every adopting project. A more specific, explicit
user instruction or established repository rule takes precedence when it
conflicts. The agent MUST identify and report the conflict; it must not silently
ignore either instruction.

### 7.1 Code quality and reuse

- Match surrounding style, naming, architecture, comment density, and idioms.
- Apply the mandatory DRY and reusable-design rules in section 2.6. Search before
  creating new code; prefer an existing suitable helper or component.
- Prefer the simplest complete solution to the actual requirement.
- Make invariants structurally difficult to bypass.
- Leave no dead scaffolding or silent TODO in place of required work.
- Keep diffs focused. Do not reformat or refactor unrelated code.

### 7.2 Execution discipline

- Act when the available context supports one safe interpretation. Ask only when
  materially different interpretations would change behavior or architecture.
- Preserve settled decisions and do not repeatedly ask the user to approve them.
- Finish the complete authorized task, including verification and documentation.
  State every blocker and out-of-scope remainder explicitly.
- Run independent operations in parallel and serialize genuine dependencies.
- Prefer dedicated repository, search, patch, and platform tools over fragile
  shell rewriting.
- Inspect before overwriting or deleting. Never work around denied access.
- Report outcomes faithfully. A failure, skip, timeout, partial log, or command
  without an exit status cannot be reported as a pass.

### 7.3 Documentation

- Update contracts, examples, configuration documentation, and operational guides
  in the same coherent change as the behavior that affects them.
- Write for the document's audience: plain language for non-technical readers and
  precise, executable detail for developers and operators.
- Use navigable relative links inside the repository and clickable file/line
  references in agent reports when supported.
- Never publish or distribute a file that the agent has not read.

### 7.4 Mandatory version control and commits

Local version control and coherent commits are mandatory. The presence of this
adopted standard is durable authorization for the agent to create ordinary,
non-destructive local Git history under the rules below; it does not authorize
discarding work, rewriting history, or publishing the repository externally.

- If the project has no Git repository, run `git init`, create a suitable
  `.gitignore`, inspect the files, and make an initial coherent commit before
  significant implementation work.
- Inspect `git status` before beginning work and again before staging. Existing
  changes belong to the user unless proven otherwise; preserve them and never
  mix unrelated work into the agent's commit.
- Commit every coherent unit automatically after its applicable checks and
  documentation are complete. Do not wait for the user to ask for a commit.
- Before beginning an unrelated request, commit any completed coherent unit from
  the prior request so unrelated work cannot accumulate together.
- Before the final response, commit all safe, authorized changes made for the
  request. If a genuine blocker prevents a coherent commit, leave user work
  untouched and report the exact blocker instead of claiming completion.
- Stage explicit reviewed paths. Never use a blind all-files stage when unrelated
  or unreviewed files may be present. Review the staged diff before committing.
- Use one logical change per commit and a meaningful `type: what changed` message
  consistent with repository history.
- Never describe failing or unverified work as complete. If a blocked checkpoint
  must be preserved, its message and report MUST truthfully identify that state.
- This standard authorizes local repository operations only. External repository
  synchronization, hosted review systems, and hosted automation are outside its
  completion model and cannot be required as evidence.
- Obtain explicit confirmation before hard resets, restoring or discarding
  uncommitted work, history rewrites, branch deletion, or any other
  destructive/irreversible Git operation.
- Use truthful authorship. Do not add a co-author identity for a person or model
  that did not perform the work.

### 7.5 Security, safety, and restricted actions

- Never commit secrets, tokens, keys, credentials, tracked `.env` files, personal
  data, or unrestricted production dumps. Inspect any suspicious staged file.
- Reference secrets indirectly through environment variables or approved
  credential helpers.
- Treat the trusted backend/authoritative component as the security boundary and
  test allowed and forbidden behavior.
- Perform only authorized, defensive security work.
- Obtain confirmation before hard-to-reverse or outward-facing actions unless
  the current repository/user instructions durably authorize that exact class of
  action. Sending content to an external service counts as publishing it.
- Never impersonate a real person or organization or fabricate a record presented
  as genuine.
- Keep safety refusals narrow and offer the nearest safe alternative.
- Use neutral pronouns when a person's pronouns are unknown.

### 7.6 Linting, formatting, types, and quality gates

- Read and obey the project's existing formatter, linter, type-checker, build,
  and test configuration. Do not introduce a competing tool by preference.
- Run the formatter after edits and then rerun affected checks because formatting
  changes the state being verified.
- Run the complete applicable layer gates before completion. Typical equivalents
  include Ruff/Black/mypy for Python, ESLint/Prettier/TypeScript for JS/TS,
  gofmt/goimports/go vet for Go, and rustfmt/clippy for Rust; the repository's
  configured commands are authoritative.
- Zero errors is the bar where a gate is configured for zero errors. Do not leave
  new warnings behind.
- Never use blanket suppressions, `--no-verify`, disabled tests, or ignored type
  errors to evade a genuine failure. A narrow suppression requires a documented
  reason and must not hide a correctable defect.
- Fix a red configured quality gate rather than declaring completion around it.
- Pin tool versions so local results are reproducible across supported machines.

### 7.7 Dependencies and builds

- Keep dependency manifests and lock files synchronized in the same change.
- Install exact committed versions from lock files rather than resolving ranges
  during a supposedly reproducible build.
- Pin containers by immutable digest and other tools by explicit version.
- Add dependencies or infrastructure only for a current requirement. Prefer the
  standard library or an existing dependency when it meets the need.

## 8. BDD, coverage, and automation boundaries

BDD/Gherkin is optional. Adopt it only when executable scenarios improve the
feature, pin its tooling, and run it through the same TR and completion gate.
Existing unit/integration/UI runners are sufficient when they assert the required
behavior. Installing this standard does not itself execute tests, prove coverage,
or certify old features. An optional future validator may check that
all FR and AS IDs appear in the matrix and evidence, but it cannot judge whether
test assertions are meaningful; analyze/converge still must inspect them.

## 9. Adoption validation checklist

The adopting agent MUST create `docs/spec-kit-adoption.md` and record one row for
every numbered section and command subsection in this standard:

```markdown
| Standard section | Applicability and reason | Implemented in | Validation | Status |
|------------------|--------------------------|----------------|------------|--------|
| 2.6 DRY and reusable design | Applicable | <files> | <inspection/check> | PASS |
```

Only PASS, FAIL, BLOCKED, and N/A are valid. N/A requires a concrete product
reason and is forbidden for the universal rules identified in section 2. The
agent MUST inspect the resulting file contents, not merely confirm that paths
exist. It MUST verify and report at least:

- [ ] The target project was already initialized with Spec Kit.
- [ ] Existing constitution content and its ratification date were preserved.
- [ ] The constitution has a justified semantic version and Sync Impact Report.
- [ ] No unexplained template placeholders remain in the constitution.
- [ ] Mandatory DRY/reuse is present in the constitution, templates, planning,
      tasks, analysis, implementation, and convergence behavior.
- [ ] Spec, plan, tasks, and checklist templates implement this contract.
- [ ] Every installed Spec Kit integration implements the command behaviors above.
- [ ] Installed workflow definitions include the verification/convergence gates
      or document their explicit manual handoff.
- [ ] Integration-specific frontmatter and invocation syntax remain valid.
- [ ] Root agent/runtime guidance names the actual project quality gates.
- [ ] A portable verification guide or this document remains in the repository.
- [ ] Diffs contain no secrets, unrelated edits, or whitespace errors.
- [ ] Documentation/config validation passes.
- [ ] Every safe authorized change was committed locally as a coherent unit and
      its staged diff was reviewed.
- [ ] Application tests are reported accurately as PASS, FAIL, NOT RUN, or
      BLOCKED; policy changes alone are never described as application proof.

Full adoption may be reported only when every applicable row and checklist item
passes, no universal row is N/A, the diff has been reviewed, and the mandatory
commit has been created. Otherwise report partial adoption and list exact gaps.

## 10. Reusable instruction for a new project

After initializing Spec Kit and copying this file into the new repository, give
the coding agent this request:

```text
Read docs/portable-speckit-standard.md completely and adopt all of it in this
project. Treat every applicable MUST as a hard requirement, not a suggestion.

First inspect the existing repository, Spec Kit version/integrations,
constitution, templates, command or skill files, runtime agent guidance,
architecture, roles, locales, data-retention rules, dependency strategy, and
actual quality-gate commands. Preserve existing product decisions and history.
If this directory is not yet a Git repository, initialize it, add a suitable
.gitignore, and make an initial commit before significant work.

Use speckit-constitution to make the portable principles concrete for this
project. Synchronize the spec, plan, tasks, and checklist templates and every
installed Spec Kit integration. Implement stable FR/AS/TR/SC traceability,
mandatory test-first tasks, verification.md evidence, evidence-aware analyze and
converge behavior, reproducibility, authorization, accessibility, scope,
secrets, and safe existing-feature
migration rules where applicable. Make DRY and reusable components mandatory:
search for existing implementations first, centralize shared knowledge and
security/business invariants, reuse or extract focused components, avoid
speculative abstraction, and test refactors.

Make version control mandatory. Commit every coherent verified unit without
waiting for me to request it, review explicit staged paths first, keep unrelated
user work out of commits, and never commit secrets. Keep repository operations
local; do not require an external repository service, hosted review, hosted
automation, or external synchronization for adoption or feature completion.
Never perform a destructive Git operation without explicit confirmation.

Do not copy technology- or product-specific Rewaq choices unless this repository
actually uses them. Do not overwrite existing specs or renumber established IDs.
Do not install optional BDD tooling unless requested. Do not claim that
application behavior passes merely because workflow files were updated.

Validate all synchronized files, report any project decisions that still need my
answer, and create docs/spec-kit-adoption.md mapping every section and command
subsection of the portable standard to its implementation and validation
evidence. Do not claim full or 100% adoption unless every applicable row passes
and no universal requirement is missing, unverified, or blocked. Commit the
completed adoption locally as a coherent unit and provide the exact next Spec
Kit command for beginning or auditing the first feature.
```

Keep this document outside generated Spec Kit directories when possible so a
future Spec Kit reinitialization or upgrade does not overwrite it. After any
upgrade, compare and reapply the local constitution, templates, and command/skill
behavior rather than assuming upstream defaults include these changes.
````

### Source S02

Source: user-supplied `spec-kit-adoption.md`. Original bytes: 11362. SHA-256: `20d25dff36e769aa79600974fd7d41c183e0bccc15642523150a9f291918425f`.

````markdown
# Spec Kit Profile 3.0.0 Adoption

**Project**: Rewaq

**Adopted profile**: `docs/portable-speckit-standard.md` 3.0.0

**Constitution**: 5.0.0

**Date**: 2026-09-15

**Scope**: Governance, templates, installed Codex skills, local workflow,
runtime guidance, and operational documentation. No application behavior was
changed or certified by this adoption.

## Resolved project context

| Variable | Rewaq value |
|----------|-------------|
| Product | Arabic-first academic content and community learning platform |
| Layers | Django/DRF backend and official Django Admin; Flutter student client; reserved future staff client |
| Ownership | Django owns data, authentication, authorization, and academic invariants; clients consume its contracts |
| Users | Guest, registered student, scoped Level Administrator, developer super-administrator |
| Locales | Arabic default, full RTL; accessible task-oriented staff and student interfaces |
| Data policy | Soft deletion and historical preservation, with the documented external-material exception |
| Local quality gates | Root `make check`, `make admin-e2e`, `make mobile-content-e2e`; mobile `fvm flutter analyze` and `fvm flutter test` plus affected plugin/device suites |
| Dependencies | Digest-pinned containers and exact committed Python/Flutter locks |
| API contract | `docs/api.md` |
| Installed integration | `.agents/skills/speckit-*/SKILL.md` |
| Working branch | Current local branch (`master` at adoption) |

## Conformance map

| Standard section | Applicability and reason | Implemented in | Validation | Status |
|------------------|--------------------------|----------------|------------|--------|
| Required outcome | Universal artifact-to-evidence chain | Constitution VI and Verification Protocol; templates; skills | Traceability and DONE/NOT DONE wording inspection | PASS |
| 1. Project discovery | Required for concrete adoption | This document; root/layer guidance | Repository paths, roles, gates, pins, and locale inspected | PASS |
| 2. Constitution requirements | Universal governance | `.specify/memory/constitution.md` | Version 5.0.0, ratification preserved, dated Sync Impact Report | PASS |
| 2.1 Layer ownership and sequencing | Multi-layer product | Constitution I; plan/tasks guidance | Backend-first ownership text inspection | PASS |
| 2.2 Authoritative authorization | Backend is trusted boundary | Constitution II/VI/VIII | Allowed/refused actual-interface requirements retained | PASS |
| 2.3 Accessible localized interfaces | Arabic student/staff interfaces | Constitution III; plan/spec templates | Arabic/RTL and rendered evidence requirements retained | PASS |
| 2.4 Data preservation | User and historical content | Constitution IV | Soft-delete and external-material exception preserved | PASS |
| 2.5 Simplicity and non-goals | Universal | Constitution V; plan Complexity Tracking | Non-goals and exception process preserved | PASS |
| 2.6 DRY and reusable design | Universal | Constitution IX; plan/tasks templates; plan/tasks/analyze/implement/converge skills; `CLAUDE.md` | Search-first, centralized-invariant, extraction, and regression rules inspected | PASS |
| 2.7 Verification before completion | Universal | Constitution VI; verification protocol; templates and skills | FR/AS/TR mapping, RED/GREEN, evidence, and convergence rules inspected | PASS |
| 2.8 Reproducibility and secrets | Universal | Constitution VII/X; plan/tasks/implement guidance | Local pins, locks, sanitized local evidence, and secret rules inspected | PASS |
| 2.9 Scoped staff administration | Product has ordinary staff and a technical superuser | Constitution VIII | Scope and actual Admin interface coverage retained | PASS |
| 3. Stable identifiers and artifact contract | Every feature uses local IDs | Templates, `docs/spec-kit-testing.md`, `docs/issue-conventions.md` | FR/AS/TR/SC/T/CHK conventions inspected | PASS |
| 3 `spec.md` | Required feature intent | Spec template and specify skill | Mandatory stories, IDs, matrix, SCs, completion gate | PASS |
| 3 `plan.md` | Required design and verification plan | Plan template and plan skill | Exact local commands, reuse inventory, fixtures, evidence | PASS |
| 3 `tasks.md` | Required executable work order | Tasks template and tasks skill | Tests-first, reuse search, local gates/evidence, convergence, commit | PASS |
| 3 `checklists/*.md` | Requirements quality only | Checklist template and checklist skill | CHK items remain distinct from behavioral evidence | PASS |
| 3 `verification.md` | Current execution record | Plan/implement/converge skills; testing guide | PASS/FAIL/NOT RUN/BLOCKED and local evidence contract | PASS |
| 4. Installed command behavior | All installed commands synchronized | `.agents/skills/` and local workflow | Skill content and lifecycle inspection | PASS |
| 4 `speckit-constitution` | Governance amendments | Constitution skill | In-place versioning, synchronization, local commit rules | PASS |
| 4 `speckit-specify` | Create/update feature intent | Specify skill | Preserves IDs/history; local-verifiable completion | PASS |
| 4 `speckit-clarify` | Resolve material ambiguity | Clarify skill | One-at-a-time integration and local commit rules | PASS |
| 4 `speckit-plan` | Design and verification planning | Plan skill | Constitution checks, reuse inventory, local evidence | PASS |
| 4 `speckit-tasks` | Dependency-ordered execution | Tasks skill | Mandatory tests/reuse/local gate/final convergence tasks | PASS |
| 4 `speckit-analyze` | Read-only consistency review | Analyze skill | Independent coverage and DRY/local-authority checks | PASS |
| 4 `speckit-implement` | Test-first implementation loop | Implement skill | Reuse search, local evidence, convergence, local commits | PASS |
| 4 `speckit-converge` | Evidence-aware gap closure | Converge skill | Append-only, deduplication, DRY, local evidence outcomes | PASS |
| 4 `speckit-checklist` | Requirements-quality checklist | Checklist skill | Append-only CHK workflow and no behavior claims | PASS |
| 5. Completion algorithm | Universal | Workflow, constitution, testing guide | Specify through converge with explicit repair handoff | PASS |
| 6. Existing-feature migration | Existing feature history is substantial | Constitution Existing Feature Adoption; specify/analyze/converge skills | Preserves IDs/checks/evidence and superseded Feature 008 | PASS |
| 7. Repository-wide engineering rules | Universal | Constitution IX/X; `CLAUDE.md`; installed skills | Rule-by-rule inspection | PASS |
| 7.1 Code quality and reuse | Universal | Constitution IX; runtime/skill guidance | Search-first and focused-diff rules present | PASS |
| 7.2 Execution discipline | Universal | Runtime guidance and skills | Accurate outcomes, scoped action, blocker rules | PASS |
| 7.3 Documentation | Universal | Constitution workflow and skills | Same-unit contract/evidence synchronization | PASS |
| 7.4 Local version control | Universal | Constitution X; `CLAUDE.md`; writing skills | Explicit reviewed staging, coherent local commits, no external synchronization | PASS |
| 7.5 Security and restricted actions | Universal | Constitution II/VI/VII/X; runtime guidance | Secrets and trusted-boundary rules retained | PASS |
| 7.6 Quality gates | Backend/mobile project | Constitution Technology/Workflow; `Makefile`; runtime guidance | Exact authoritative local gates named | PASS |
| 7.7 Dependencies and builds | Containers and two language ecosystems | Constitution VII; layer guidance | Locks and immutable image pins retained | PASS |
| 8. BDD and automation boundaries | Universal; BDD optional | Testing guide and skills | Native test runners remain sufficient; no tooling added | PASS |
| 9. Adoption validation | Required audit record | This document | Rows and checklist below | PASS |
| 10. Reusable adoption instruction | Portable standard must remain reusable | `docs/portable-speckit-standard.md` | Profile stays outside generated directories and local-only | PASS |

## Validation checklist

- [x] The repository was already initialized with Spec Kit.
- [x] Existing constitution content and the 2026-07-21 ratification date were preserved.
- [x] Constitution 5.0.0 has a justified major bump and a Sync Impact Report.
- [x] No unexplained constitution template placeholders remain.
- [x] Mandatory DRY/reuse appears in the constitution, templates, planning,
      tasks, analysis, implementation, convergence, and runtime guidance.
- [x] Spec, plan, tasks, and checklist templates implement the artifact contract.
- [x] Every retained installed Spec Kit skill implements its applicable profile behavior.
- [x] The local workflow includes clarify, analyze, implement, and converge with an explicit repair handoff.
- [x] Integration-specific frontmatter and invocation syntax remain valid.
- [x] Runtime guidance names the actual local project quality gates.
- [x] External task conversion was retired; feature-qualified local task references remain documented.
- [x] The portable verification guide remains in the repository.
- [x] Documentation/configuration validation passed for the adoption commit.
- [x] The staged diff was reviewed and committed as one coherent local unit.
- [x] No external synchronization was attempted.
- [x] No application test was represented as passing because of this policy-only change.

## Validation evidence

| Command | Result | Meaning |
|---------|--------|---------|
| `bash -n .specify/scripts/bash/common.sh .specify/scripts/bash/create-new-feature.sh` | PASS | Modified shell helpers parse |
| `jq empty .specify/integrations/codex.manifest.json` | PASS | Integration manifest is valid JSON |
| Manifest SHA-256 comparison against every retained skill | PASS | All managed skill hashes match their current files |
| `specify workflow info speckit` | PASS | Version 2.0.0 resolves all ten local lifecycle steps |
| `specify integration status` | PASS with expected customization warning | Codex is active; no missing/invalid/unchecked manifest files; seven shared files are intentionally locally modified |
| `make -n check` | PASS | The authoritative backend gate remains invocable |
| Constitution placeholder scan | PASS | No unexplained all-capital placeholder remains |
| Active hosted-service dependency scan | PASS | No active operational instruction requires external repository hosting, review, synchronization, or upload |
| `git diff --check` | PASS | No whitespace errors |

Application tests were **NOT RUN** because this adoption changes governance,
templates, workflow metadata, and documentation only. Existing application
evidence retains the status and revision it originally recorded.

## Historical and migration boundary

Upstream author fields in retained skill frontmatter and dated system-design
snapshots are provenance, not operational dependencies. Existing feature
artifacts retain their task IDs, checked history, and past external results.
When an affected feature is next reviewed for completion, its spec, plan, tasks,
and verification record must be migrated to constitution v5 without relabeling
old evidence as current.

Feature 003 is the first active migration. Feature 006 retains iOS product scope;
its local simulator/device completion posture requires an explicit product
decision if suitable local Apple hardware remains unavailable.
````

### Source S03

Source: user-supplied `spec-kit-testing.md`. Original bytes: 8147. SHA-256: `e5d25425b45c9ff3be1f4361ff7e66f4df483b45859c6d7d0614502dd43b968c`.

````markdown
# Testing with Spec Kit

For a project-independent blueprint that can be copied after initializing Spec
Kit in another repository, see [Portable Spec Kit Standard](portable-speckit-standard.md).

The project constitution v5 makes completion depend on observed behavior and
authoritative local evidence.
The loop is: specify → clarify → plan → tasks → analyze → implement → tests →
converge. When verification fails or convergence finds gaps, implement fixes,
rerun verification, and converge again. A missing prerequisite is recorded as
BLOCKED; it never becomes a passing check through repeated attempts.

## What each artifact proves

| Artifact | Purpose |
|----------|---------|
| `spec.md` | Defines FR requirements, AS scenarios, TR test requirements, SC measurements, and the completion gate |
| `plan.md` | Selects verification layers, commands, fixtures, platforms, and regression scope |
| `tasks.md` | Orders tests, implementation, verification, and remediation work |
| `checklists/*.md` | Checks the quality of the written requirements only |
| `verification.md` | Records actual execution and per-TR evidence for the tested state |
| Convergence report | Compares artifacts, current code, test assertions, and evidence; identifies remaining gaps |

Checking a task, finding a test file, passing lint, or inspecting code does not
prove an acceptance scenario. A test must exercise the relevant behavior and
assert the promised outcome. A verification matrix is a traceability aid, not
an assertion that tests have run.

## IDs and verification

Use feature-local `FR-001`, `AS-001`, `TR-001`, and `SC-001` identifiers.
Write `012/FR-009a` for a cross-feature reference. Preserve existing identifiers;
legacy `US1/AC2` can serve as a stable scenario alias during adoption.

For example, a scoped Admin workflow can specify:

- `AS-001`: an assigned administrator submits a valid membership and receives
  confirmation; one membership and all required enrollments exist.
- `AS-002`: an administrator submits another scope's batch identifier; the
  request is refused and no membership or enrollment changes.
- `TR-001` and `TR-002` implement those assertions through the actual Admin
  request path. Service tests supplement them for transaction rollback/retries.

Keep FR/AS/TR references in test names, docstrings, or markers. In the evidence
matrix map them to concrete runnable selectors, such as pytest node IDs or
Flutter test files and test descriptions. Read the assertions when auditing
coverage; matching identifiers alone are insufficient.

Choose the smallest useful test layer. Use unit tests for domain rules,
integration/contract tests for database and API behavior, and Admin requests or
browser tests for staff workflows. Add visual/RTL and physical-device evidence
where the promised outcome requires them. A passing screenshot-text assertion
cannot prove control width, touch-target size, or keyboard behavior.

## Evidence format

`speckit-plan` starts `specs/NNN-feature/verification.md` with planned checks
marked NOT RUN. `speckit-implement` records actual results. Use this structure:

```markdown
# Verification: feature name

Constitution: <version>
Completion: NOT DONE
Tested revision / working-tree fingerprint: <identify code and artifacts>
Date: <actual run date>
Environment: <container/dependencies, browser/device/OS as applicable>

## Coverage

FRs with meaningful test assertions: <covered>/<total>
ASs with meaningful test assertions: <covered>/<total>
Required TRs passing: <passing>/<total>

| FR / AS | TR | Executable selector | Status | Evidence |
|---------|----|---------------------|--------|----------|
| <IDs> | <ID> | <test path and selector> | NOT RUN | No execution yet |

## Execution

| Working directory | Exact command | Exit code | Passed / failed / skipped / xfailed | Evidence reference |
|-------------------|---------------|-----------|------------------------------------|--------------------|
| <directory> | <command> | NOT RUN | NOT RUN | <local log or artifact path> |

## Additional acceptance evidence

| Scenario / SC | Method and platform | Expected | Observed | Status / evidence |
|---------------|---------------------|----------|----------|-------------------|
| <ID> | <walkthrough or measurement> | <outcome> | Not observed | NOT RUN |

## Remaining gaps

<Missing tests, failing cases, blocked prerequisites, and remediation task IDs>

## Convergence

<Date, assessed state, outcome, remaining findings and task IDs; initially NOT RUN>
```

Use PASS, FAIL, NOT RUN, or BLOCKED per check. Explain skips and xfails;
required ones block DONE. Keep historical runs labeled with their tested state.
New code or changed acceptance criteria require updated relevant verification.
Do not put passwords, tokens, student data, or unrestricted raw dumps in evidence.
Keep required logs, screenshots, traces, archives, and measurements under the
planned repository-owned local evidence path. Scan ordinary and compressed
artifacts for sensitive values before retaining them. External hosting,
automation, review, synchronization, work-item, and artifact-upload services are
never completion gates.

## Commands

Invoke these skills in the IDE, one at a time, retaining the same feature
directory. These are agent requests, not shell commands:

```text
$speckit-specify
SPECIFY_FEATURE_DIRECTORY=specs/NNN-feature
Define the feature with stable FR/AS/TR IDs, a verification matrix, success
measurements, and the constitution v5 completion gate.
```

Then use `$speckit-clarify` for unresolved behavior, `$speckit-plan` for test
architecture, `$speckit-tasks` for tests before implementation, and
`$speckit-analyze` for consistency and verification coverage.

```text
$speckit-implement
SPECIFY_FEATURE_DIRECTORY=specs/NNN-feature
Implement the mapped acceptance tests and feature behavior. Diagnose and fix
failures, run full relevant suites, and record actual evidence in verification.md.
Do not claim DONE while any required verification is missing or blocked.
```

```text
$speckit-converge
SPECIFY_FEATURE_DIRECTORY=specs/NNN-feature
Audit current behavior, FR/AS/TR coverage, actual test assertions, and current
verification evidence. Append only uncovered remediation work; reference
existing open tasks instead of duplicating them. Do not modify application code.
```

For an existing feature, begin with analyze/converge. If the matrix or plan is
missing, update those artifacts with specify/plan before generating test tasks.
Preserve prior work, IDs, and approved product decisions. Exclude superseded
Feature 008 from active implementation. Start adoption with Features 009 and 012
because they govern the staff interface currently being exercised.

From the repository root, the backend's complete gate is `make check` with the
configured Docker environment. Focused pytest runs are useful during repair but
do not replace the final complete gate. In `apps/mobile`, run
`fvm flutter analyze` and `fvm flutter test`, plus the affected plugin suites
from their package directory and required integration/device runs as specified
in the feature plan. Keep physical device and browser prerequisites explicit.

## BDD and automation boundaries

The pasted proposal also suggests a community BDD extension. Gherkin scenarios
may be used if a feature benefits from executable Given/When/Then definitions;
they must map to the same FR/AS/TR IDs and run as real tests. No new framework
or extension is required for this policy: existing pytest and Flutter runners
can implement these acceptance tests. No BDD extension or new hooks are installed
by this amendment. If one is adopted later, pin it, define its runner in the
plan, and keep the same completion gate.

These constitution, template, and skill changes guide agent work. They do not
add an automatic coverage validator and cannot retroactively prove that existing
features pass. New feature tests and durable local evidence still have to be
implemented and executed. Any retained hosted workflow is optional historical
infrastructure and cannot substitute for or block the documented local gates.
````

### Source S04

Source: user-supplied `issue-conventions.md`. Original bytes: 1528. SHA-256: `c71b1aef893269d2e308bcfd60356d505e7243be05571fc24e6d517e18c7b2ec`.

````markdown
# Local Task Identity Conventions

Feature work is tracked in the repository under `specs/NNN-feature/tasks.md`.
No external work-item service is required for planning, execution, verification,
or completion.

## Canonical reference: `[NNN] TXXX`

Every feature restarts task IDs at `T001`. A task referenced outside its own
`tasks.md` therefore MUST include the feature number:

```text
[NNN] TXXX: <short description>
```

- `NNN` is the feature directory number, such as `001` or `003`.
- `TXXX` is the task ID inside that feature, such as `T001` or `T092`.

Examples:

- `[001] T001: Create the Django project skeleton`
- `[003] T092: Reconcile the local Android evidence`

Within the owning `tasks.md`, the bare `TXXX` remains canonical because the
feature context is already unambiguous. Cross-feature specifications, plans,
verification records, commit messages, and reports use `[NNN] TXXX`.

## Local workflow

1. Preserve task IDs and checked history when regenerating tasks.
2. Append new task IDs after the current maximum; never renumber old work.
3. Record behavioral results in the feature's `verification.md`, not in the task
   checkbox itself.
4. Commit each coherent verified unit locally using explicit reviewed paths.
5. Do not require an external board, review service, repository host,
   synchronization step, or uploaded artifact to establish completion.

Historical references from earlier workflows may remain in historical evidence,
but they do not change current task identity or completion status.
````

### Source S05

Source: user-supplied `live-testing.md`. Original bytes: 7513. SHA-256: `fbf47c82e9d96e2ac63619a3d78f3671ff5dd1672e0c1e5d9915425c529d1364`.

````markdown
# Live end-to-end mobile testing (feature 006)

How to run the Rewaq app against a local backend and prove the download and
upload services on locally controlled Android and Apple environments. This is
the durable copy of `specs/006-testing/quickstart.md`.

> **Sibling runbook:** `docs/native-testing.md` covers compiling the native code
> (Android emulator and iOS via a local macOS environment). This file is about
> *running and verifying* the app end-to-end.

## The strategy (decision on record)

- **iOS compile verification → local macOS environment.** The documented macOS
  VM can compile iOS, but its lack of Metal means it cannot certify rendered
  simulator behavior. A local Apple Silicon/Intel Mac or physical iPhone is
  required for those observations; without one they remain BLOCKED.
- **Optional cloud previews are non-authoritative.** They may aid exploration,
  but neither an account nor an uploaded build is a completion prerequisite.
- **Android → local emulator**, driven through the bounded
  `scripts/emulator.sh` helper and `adb`.
- **A real iPhone with a locally installed development build is only needed later**,
  and *only* for the two
  OS-integration checks a Simulator can't show — background audio on the **lock screen**
  and **hidden-from-Gallery / backup-excluded** (feature 005 device checks). That route
  may require an Apple Developer account and a locally produced signed build —
  deferred until those checks matter for release.

## Prerequisites

- Backend up: `cp .env.example .env && docker compose up` (web `:8000`, Postgres, MinIO `:9000`).
- Seed applied with **real media**: `docker compose exec web python manage.py seed_demo`
  (uploads the committed `seed_assets/`; `ensure_buckets` runs on web start and opens
  anonymous reads).
- Android: the exact SDK components in `e2e/android/sdk-lock.env`, hardware
  KVM, FVM, and Flutter 3.44.7. The isolated runner verifies every revision and
  archive checksum.
- iOS: the local macOS environment documented in `docs/native-testing.md`; a
  physical iPhone or local Mac with a working Simulator for rendered/device checks.

---

## Path A — Android (local, no tunnel needed)

The emulator reaches the host at `10.0.2.2`, and the app already permits cleartext to
that dev host (`network_security_config.xml`), so no tunnel is required.

1. Point the backend's media URLs at the host as the emulator sees it, and restart the
   API so URLs are rebuilt:
   ```sh
   MEDIA_CDN_BASE_URL=http://10.0.2.2:9000/rewaq-media docker compose up -d web
   docker compose exec web python manage.py seed_demo
   ```
2. **Reachability precheck** (must pass before launching the app):
   ```sh
   curl -fsSI "http://localhost:9000/rewaq-media/demo/notes.pdf" | head -1        # 200
   curl -fsS  "http://localhost:9000/rewaq-media/demo/v1/hls/index.m3u8" >/dev/null # 200
   ```
   If these fail it's the backend/seed, not the app — fix that first.
3. Build/run on the emulator:
   ```sh
   scripts/emulator.sh start
   scripts/emulator.sh wait
   cd apps/mobile && fvm flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000
   ```
4. **US4 visual (SC-002):** navigate the main screens; confirm Arabic RTL, no crash.
   Capture with `adb exec-out screencap -p > shot.png`.
5. **US2 download (SC-003):** open a seeded item → tap download → progress reaches 100%.
   Then disable the network (`adb shell svc data disable` / airplane mode) and open it —
   video/audio plays or the PDF opens from local storage.

For the repeatable current-term content workflow, run
`make mobile-content-e2e` from the repository root. It seeds disposable actors
and two sessions, performs valid scoped Django Admin submissions in a
credential-confined Playwright coordinator, refreshes the running app, and
retains sanitized screenshots, diagnostics, and timing evidence. It accepts no
production data, credential, token, or caller-selected backend URL.

---

## Path B — iOS (local macOS environment)

1. Start or connect to the local macOS environment using
   `docs/native-testing.md`.
2. Copy the repository into that environment and install the exact committed
   Flutter/Dart dependencies.
3. Run `flutter analyze`, `flutter test`, and
   `flutter build ios --no-codesign` from `apps/mobile`.
4. On a local Mac with a working Simulator, start the backend on a reachable
   private address, boot the Simulator, and run the required integration tests.
5. **US1 visual (SC-001):** confirm the home/hierarchy, study-material, and
   offline-player screens render in Arabic RTL; retain a sanitized screenshot in
   the feature's local evidence directory.
6. **US2 download on iOS (SC-003 cross-platform):** repeat the download and
   offline-open check locally.

If the available VM cannot run the Simulator and no local device/Mac is
available, steps 4–6 are **BLOCKED**, not PASS. An optional external preview may
help diagnose layout but does not change that local completion state.

---

## Upload (both paths, live) — US3 / SC-004

1. Sign in as the seeded demo student (phone `0500000001`, level 1).
2. Upload permitted peer material **at level 1** → expect success, visible in the app.
3. Attempt an upload scoped to **level 2** (the second seeded level) → expect `403`
   surfaced in the app.

The `401`/`201`/`403` boundary is already proven automatically by
`apps/backend/apps/peer_material/tests/test_upload_auth.py`; this is the *live*
confirmation.

### Recorded run — 2026-07-31, Android emulator (`rewaq_test`, API 35)

Performed against the local stack with the release APK built for
`API_BASE_URL=http://10.0.2.2:8000`. Read the backend log alongside the screen —
the log is the evidence, the screen is the confirmation a student would see.

| Step | Backend log | In the app |
|---|---|---|
| Upload at **level 1** (own level) | `POST /api/lessons/1/peer-material/` → **`201`**, then the list `GET` | the file appears with the uploader's name and `0` upvotes |
| Upload at **level 2** (out of level) | `POST /api/lessons/5/peer-material/` → **`403`** | Arabic reason shown: *«لا يمكنك الرفع أو النشر إلا في دروس مستواك المسجَّل.»*, nothing added to the list |

Two things this run is worth remembering for:

- **Level 2 had no lessons**, so there was nothing to attempt an out-of-level
  upload against until one was seeded. A fresh database needs a lesson outside
  the test student's level or SC-004's rejected half cannot be exercised at all.
- The upload control is deliberately **not hidden** on an out-of-level lesson.
  That is Principle II: the client is not the security boundary, so the check
  being observable here is the point, not a leak.

The run also caught the `403`'s reason never reaching the student (a generic
"try again later"), now fixed — see 007 T027.

---

## Teardown

Stop emulators/VMs and remove disposable seeded data after the run. If an
optional tunnel was used for exploratory testing, stop it, do not commit its
hostname, and reset the backend media base with `docker compose up -d web`.

## Success-criteria mapping

| Check | Criterion |
|---|---|
| Path B step 5 | SC-001 (iOS visible) |
| Path A step 4 | SC-002 (Android visible) |
| Path A step 5 / Path B step 6 | SC-003 (download + offline playback) |
| Upload section | SC-004 (upload allowed + rejected) |
| Local reachability prechecks | SC-005 (backend/media reachable from the test device) |
| This document | SC-006 (reproducible from docs) |
````

### Source S06

Source: user-supplied `native-testing.md`. Original bytes: 6246. SHA-256: `92b092373abce48962794d838dcfb76cce1d995f1b7aba779063bdb9dfdf43da`.

````markdown
# Native testing — Android & iOS from this Linux workstation

Feature **005 (offline_media plugin)** is the first work in this repo with real
**native code** (Kotlin/Media3 on Android, Swift/AVFoundation on iOS). Unlike
everything before it, it **cannot** be verified on the Linux desktop build or in
the Flutter widget-test harness — it needs a device/emulator per platform.

This doc is the runbook for standing that up. Helper scripts live in
[`tools/`](../tools).

> For **running the app end-to-end** against a live backend (watch it on iOS via
> Appetize + Android emulator, and verify the download/upload services), see the
> companion runbook [`live-testing.md`](./live-testing.md) (feature 006).

| Platform | How | Status on this box |
|---|---|---|
| **Android** | Local x86_64 emulator, KVM-accelerated | ✅ working |
| **iOS** | macOS in a KVM container (Docker-OSX), Xcode inside | ⚙️ VM tooling ready; macOS install is a manual first-boot step |

> **RAM reality (16 GB host):** the macOS VM wants ~8 GB and the Android emulator
> ~2 GB. You cannot run both (plus the backend Docker stack) at once. **Do iOS
> and Android sessions separately** — stop the Android emulator before booting the
> macOS VM.

---

## Android (local emulator)

Already installed: SDK, `emulator`, the `system-images;android-35;google_apis;x86_64`
image, and an AVD named **`rewaq_test`** in `~/.android/avd`. `~/.zshrc` puts the
SDK tools (incl. `emulator/`) on `PATH`.

```bash
# boot the emulator (windowed) and wait until it's ready
tools/android-emu.sh start &      # or `headless` for a local automated run
tools/android-emu.sh wait

# from the app, deploy to it — note the Android-emulator loopback host:
cd apps/mobile
fvm flutter run -d emulator-5554 --dart-define=API_BASE_URL=http://10.0.2.2:8000
```

- `10.0.2.2` is the emulator's alias for the **host** `localhost`, so it reaches
  the backend running in Docker on this machine.
- Plugin unit tests (no device): `fvm flutter test packages/offline_media`.
- Plugin integration tests (device): `fvm flutter test integration_test -d emulator-5554`.
- Gate: `fvm flutter analyze` must be zero errors (app **and** the plugin package).

Verified working: emulator boots in ~15 s on KVM; `flutter devices` lists it; a
debug APK builds via Gradle.

---

## iOS (macOS in a KVM container — Docker-OSX)

Because Xcode only runs on macOS, we virtualize macOS locally with Docker-OSX.
The host already has KVM
and Docker; the [`tools/macos-vm.sh`](../tools/macos-vm.sh) helper wraps the
`docker run` incantation.

> **Legal note:** Apple's macOS EULA restricts running macOS to Apple-branded
> hardware. Virtualizing it on non-Apple hardware is your decision; this doc only
> documents the mechanics.

### One-time host prep

```bash
sudo pacman -S xorg-xhost          # needed so the VM window can use your X server
tools/macos-vm.sh doctor           # checks KVM, docker, X11, xhost, RAM, image
```

`doctor` must be all-green before `create`. If RAM is short, stop the Android
emulator (`tools/android-emu.sh stop`) and optionally the backend
(`docker compose stop` in `apps/backend`).

### First boot — install macOS (manual, ~1 hour)

```bash
tools/macos-vm.sh create           # boots the macOS installer in a QEMU window
```

Inside the VM window:

1. Pick **Disk Utility** → select the largest (~un-formatted) disk → **Erase**,
   format **APFS**, name it e.g. `Macintosh HD` → quit Disk Utility.
2. Choose **Reinstall macOS** → install onto that disk. macOS downloads from
   Apple during this step; it reboots a few times. Leave the window focused.
3. Create a local user when prompted. Skip Apple-ID sign-in if you don't need the
   App Store yet.

The VM persists as a **named container** (`rewaq-macos`) — it is *not* `--rm`, so
`stop`/`start` keep the installed macOS. `tools/macos-vm.sh rm` destroys it.

```bash
tools/macos-vm.sh start            # reboot into the installed macOS later
tools/macos-vm.sh ssh              # shell in (user: user / pass: alpine), port 50922
```

### Inside macOS — toolchain + project

1. **Xcode**: install from the App Store (needs an Apple ID) *or* install the
   Command-Line Tools (`xcode-select --install`) if only CLI builds are needed.
   Accept the license: `sudo xcodebuild -license accept`.
2. **Flutter**: install Flutter for macOS (`git clone` the SDK, add to `PATH`),
   then `flutter doctor` and accept iOS/CocoaPods prompts (`sudo gem install cocoapods`).
3. **The project**: get the repo into the VM — simplest is `git clone` inside the
   VM, or copy over SSH:
   ```bash
   # from the Linux host, push the repo into the running VM:
   rsync -e 'ssh -p 50922' -a --exclude build --exclude .dart_tool \
     "./" user@localhost:~/rewaq/
   ```
4. **Build & test iOS** (inside the VM):
   ```bash
   cd ~/rewaq/apps/mobile
   flutter pub get
   flutter build ios --no-codesign --dart-define=API_BASE_URL=http://<host-ip>:8000
   # simulator integration tests:
   open -a Simulator
   flutter test integration_test -d <booted-simulator-id>
   ```
   Use the host's LAN IP (not `localhost`) for `API_BASE_URL` so the VM reaches the
   backend, or run the backend inside/alongside as needed.

### Expectations & limits

- **Performance:** with only ~8 GB for the VM on a 16 GB host, Xcode builds and
  the Simulator will be **slow** and may swap. Fine for "does it compile / do the
  plugin tests pass"; painful for rapid iteration.
- **Background / lock-screen / backup-exclusion** checks (US2/US5) are best proven
  on a **physical iPhone**; the Simulator doesn't exercise all of them.
- If the local VM proves too heavy and no local Mac is available, iOS compile or
  simulator evidence is **BLOCKED**. Do not replace the missing local platform
  with a hosted completion requirement.

---

## Quick reference

```bash
# Android
tools/android-emu.sh start & ; tools/android-emu.sh wait
fvm flutter run -d emulator-5554 --dart-define=API_BASE_URL=http://10.0.2.2:8000
tools/android-emu.sh stop

# iOS (macOS VM)
tools/macos-vm.sh doctor
tools/macos-vm.sh create      # first time (installs macOS interactively)
tools/macos-vm.sh start       # subsequent boots
tools/macos-vm.sh ssh
tools/macos-vm.sh stop
```
````

### Source S07

Source: user-supplied `adding-content.md`. Original bytes: 8328. SHA-256: `0f8a6d755b78cd3284199c178430282ceeeaa6eb9708f55826119fb837ca65e9`.

````markdown
# Adding real lessons, videos, and PDFs

How to get your own material into Rewaq, instead of the four demo lessons
`seed_demo` creates.

## The one thing to know first

**Rewaq streams HLS, not MP4.** A video's `storage_key` is a *directory* holding
`master.m3u8` plus its segments, and the app builds the stream URL as
`<storage_key>/master.m3u8`. Point a lesson at a `.mp4` and it will list
normally, open normally, and fail the moment a student presses play — a failure
that looks like a broken app rather than a bad key.

`tools/add-media.sh` handles this: it transcodes, uploads, and attaches in one
step, and refuses inputs that would produce a lesson that only breaks later.

## 1. Create the lesson

Structure lives in the Django admin — <http://localhost:8000/admin/>.

```sh
make superuser        # once — pick your own password
```

### Staff accounts

Staff are **not** created through the admin's "add user" page — that page makes
*students*, who never have a password because they sign in with a one-time code.
Someone who needs the admin needs a real password.

```sh
docker compose exec web python manage.py ensure_roles      # once
docker compose exec web python manage.py create_staff \
    --phone 0501234567 --name "أ. محمد" --role "مديرو المستويات"
```

It prompts for the password. Re-run it on the same phone to change the password
or role — it updates rather than failing.

| Account | Can do |
|---|---|
| `مديرو المستويات` | Operational work for explicitly assigned term-and-level combinations: students, subjects, lessons, study material, and reported content |
| `--superuser` | Technical configuration, staff accounts and assignments, every term/level, and exceptional corrections |

After creating a Level Administrator, the super-administrator opens
**تعيينات مديري المستويات** and assigns their exact term and level, for example
*Winter 2026 → Tamheedy 2*. Without an assignment the staff member sees an
Arabic explanation and cannot change data. Assignments never carry into a new
term automatically; create a new assignment for the next term. Revoking one
blocks the administrator's next write, even if they are already signed in.

Level Administrators can work only inside their assigned term-and-level pairs.
They cannot create staff, grant themselves access, or view another team's data.
Ordinary curriculum and material edits are limited to an assigned current term.
Past-term moderation requires a separate assignment for that exact historical
term and level.

Reported questions and peer uploads need **two reports from different students**
before any account, including the super-administrator, can remove them. Removal
is reversible: it hides the item from students while keeping it available to an
eligible staff member for restoration.

Prefer `مديرو المستويات` over `--superuser`. Only a super-administrator can
assign scopes or promote staff.

### Academic enrollment and progression

Create a **دفعة** inside the assigned term and level, then add students to its
memberships. Their level subjects are enrolled once automatically. Record each
course result as a final pass or fail; after every course has a result, apply
the student's progression outcome. One or two final-level failures create only
the required repeats in the next term—there is no level-nine batch. When all
of those repeats pass, graduation is recorded automatically. Only a
super-administrator may correct a progression outcome, and the correction must
include a reason; it preserves the old outcome and reconciles only its
resulting enrollments.

Create in this order (each needs the one above it):

**Session** → **Level** → **Subject** → **Lesson**

Note the lesson's **id** from the URL (`/admin/hierarchy/lesson/7/change/` → `7`).

### What else the admin covers

| Page | Use |
|---|---|
| Users | Create a student (phone + level, no password), reassign a level, deactivate |
| Study material | Titles, instructor, kind, external links; **upload a PDF directly** |
| Peer material | Review reports and remove uploads after two distinct student reports |
| Forum questions / answers | Review reported questions and remove eligible questions after two distinct reports |

**A PDF can be uploaded straight from the study-material form.** Video and audio
cannot, and the form will tell you so: they need HLS conversion, which is what
step 2 is for.

## 2. Attach the material

```sh
# video — any format ffmpeg reads
tools/add-media.sh --lesson 7 --title "محاضرة التجويد ٦" \
    --instructor "الشيخ محمد" ~/lectures/six.mp4

# audio
tools/add-media.sh --lesson 8 --title "درس صوتي" ~/lesson.m4a

# PDF
tools/add-media.sh --lesson 9 --title "مذكرة التجويد" ~/notes.pdf
```

Kind is inferred from the extension; pass `--kind` to override. Duration (and a
PDF's page count, if `pdfinfo` is installed) is read from the file. Re-run it on
the same lesson to replace the material — that is the way to fix a bad upload.

Requires `ffmpeg` **on your machine**, not in the container; the backend image
has no reason to carry a transcoder.

## 3. Check it before testing on a phone

```sh
curl -s localhost:8000/api/lessons/7/study-material/
```

Take the `stream_url` and fetch it — a `200` with content type
`application/vnd.apple.mpegurl` means the app will play it. Anything else is
the content, not the app, and is worth fixing before you go looking for a bug
on the device.

Only content in the backend's active session appears in the app. After saving
a level, subject, lesson, or study-material change in Django Admin, pull down on
the corresponding app screen. If the app was backgrounded, returning to it
refreshes the active session, hierarchy, material, forum, peer files, and recent
updates. Activating another session replaces the displayed session label and
hierarchy together; stale descendant pages are closed.

To prove this without using a development or production account, run
`make mobile-content-e2e`. The command creates isolated test-only accounts and
content, performs the Admin submissions, and stores sanitized evidence. Never
put a password, token, cookie, production database, or temporary tunnel URL in
the command or retained evidence.

## Testing the download path end to end

1. Open the lesson in the app → **Study material** tab.
2. The card's control shows a download glyph. Tap it (or the button below).
3. Watch it fill; when it finishes, both controls become **play**.
4. Turn on **airplane mode** and play it — this is the actual proof.
5. Tap download on a *different* lesson while offline: it should say
   **"لا يوجد اتصال بالإنترنت — سنُكمل التنزيل تلقائياً عند عودة الاتصال."**
   and start by itself when you come back online.

## Testing on a real phone, off USB

The phone cannot reach `localhost` on your laptop. `tools/tunnel.sh` opens two
public HTTPS tunnels — one for the API, one for the object store — and prints
the two values to use:

```sh
tools/tunnel.sh
# then, with the printed MinIO URL:
MEDIA_CDN_BASE_URL=https://<minio-tunnel>/rewaq-media docker compose up -d web
# and build the app against the printed API URL:
cd apps/mobile
fvm flutter build apk --release --dart-define=API_BASE_URL=https://<api-tunnel>
adb install -r build/app/outputs/flutter-apk/app-release.apk
```

For a local emulator instead of a physical phone, use
`scripts/emulator.sh start`, `scripts/emulator.sh wait`, and the stable host
address `http://10.0.2.2:8000`; do not use or retain a tunnel URL.

Both URLs change every time cloudflared restarts, and the APK bakes the API one
in at build time — so a build is tied to the session that produced it. Fine for
testing, not something to hand to a student.

## Logging in while testing

`ConsoleSmsBackend` writes the one-time code to the container log:

```sh
docker compose logs web | grep -i "رمز الدخول"
```

Or skip the hunt: in development, **246810** works as the code for any
registered account. Request a code as normal, then enter it. It is refused
outright unless `DEBUG` is on, so it cannot follow you into production.

The demo student seeded by `seed_demo` is **0500000001**, registered at level 1.
````

### Source S08

Source: user-supplied `brand-pattern.md`. Original bytes: 2393. SHA-256: `1cf3077a61803700d1c71a174dcfedaa34c4683478754daf55bb0baf94a60068`.

````markdown
# The Rewaq pattern

One tile — an eight-point khātam star in continuous strapwork — carried by both
the app and the admin panel, so a student and a teacher are plainly looking at
one product.

It is **seamless**: every band that leaves an edge re-enters on the opposite
one, so it repeats without a join. Nothing else about it is negotiable either;
the geometry is the identity. Colour and opacity are free.

## The three files

| File | What it is |
|---|---|
| [tools/pattern-tile.drawio.svg](../tools/pattern-tile.drawio.svg) | The editable original. Open it in draw.io to change the shape. |
| [apps/backend/static/admin/img/pattern.svg](../apps/backend/static/admin/img/pattern.svg) | The outlined export — strokes flattened to one filled path. This is what ships. |
| [apps/mobile/assets/images/pattern_tile.png](../apps/mobile/assets/images/pattern_tile.png) | A 600×600 raster of the same, for Flutter. |

The PNG is derived, so regenerate it whenever `pattern.svg` changes:

```sh
rsvg-convert -w 600 -h 600 --background-color=none \
    apps/backend/static/admin/img/pattern.svg \
    -o apps/mobile/assets/images/pattern_tile.png
```

Its ink colour never reaches the screen — Flutter tints the tile through its
alpha — so the green baked into the SVG is harmless here.

## Colour

The SVG carries its own colour, because an SVG used as a CSS `background-image`
is an isolated document: `currentColor` has nothing to inherit and the page's
stylesheet cannot reach inside it. A `prefers-color-scheme` media query *can*
see through, which is how one file is green on the cream admin and gold on the
dark one. A browser that ignores it keeps the green.

Flutter does not have that problem — `RewaqPattern.tile()` takes a colour and an
opacity and masks the tile with it.

## Where it appears

| Surface | Colour | Opacity | Tile |
|---|---|---|---|
| Admin, any page | green / gold | 4.5% | 150px |
| Admin sign-in | green / gold | 18% | 200px |
| App home header | gold on green | 13% | 150dp |
| App sign-in and code entry | green on cream | 10% | 180dp |

Two rules learned the hard way. **Keep it faint** — this is masonry behind text,
and text that competes with it is text nobody reads. And **keep the tile large**
enough that the star reads as a star; below about 120px the strapwork collapses
into noise and the whole thing just looks like a dirty background.
````
