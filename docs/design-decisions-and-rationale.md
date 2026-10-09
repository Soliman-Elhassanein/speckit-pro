# Why speckit-pro is designed this way

Recorded: 2026-10-09. Covers profile/preset 3.0.0, baseline extension 0.6.0 and
workflow 1.2.0, tested with Spec Kit 1.1.2.

This document explains the project's design decisions, their inspiration, expected
benefits, tradeoffs, rejected approaches and deferred work. It describes the current
design; it does not promise a gap-free development process or commit to a roadmap.
The [profile](../speckit-universal-profile.md) and shipped commands remain the operative
contracts. The [audit response](followup-audit-response.md) records individual fixes
and disagreements; the [adoption guide](installation-and-adoption-scenarios.md)
explains installation and use.

## The original problem and inspiration

The original request was to keep an evolving, versioned whole-product document and
an architecture document beside Spec Kit's constitution. Each feature should consult
the product before specification and the architecture before planning, ask about
conflicts, retain the answers, and continue the familiar Spec Kit flow. Existing code
also needed a recovery path that distinguished observed behavior from approved intent.

The design discussions compared community approaches to project memory, architecture,
decisions, citations, drift and consolidation. The table below records selected
conceptual influences and how speckit-pro adapted them. The links point to fixed
revisions examined during research, rather than making claims about those projects'
latest versions. These are influences, not required companion installations.

| Inspiration and source | Relevant idea | How speckit-pro adapted it |
|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit/tree/v1.1.2) | Feature specifications, plans, tasks, and supported customization through presets/extensions/workflows. | Keep the normal lifecycle and package the stricter rules through those surfaces instead of maintaining a core CLI fork. |
| [Spec Roadmap template](https://github.com/srobroek/speckit-roadmap/blob/f67f7905c8c47cff8627b5533414934561478023/templates/roadmap-template.md) | Versioned project memory with goals, dependencies, decisions, scope and unresolved questions. | Keep a compact product capability index. Separate approval from calculated delivery; the product baseline governs intent rather than serving only as a non-binding roadmap. |
| [ProductShape apply logic](https://github.com/juangcarmona/productshape/blob/a475158bb83bd2078233ac8fb10643a0ee1249e6/packages/core/src/apply.ts) | Human approval, baseline-revision compatibility and explicit application preconditions. | Require approval for semantic amendments and validate state before acceptance. Keep a smaller Markdown baseline instead of importing its full product-model/change system. |
| [Architecture Governance repinning](https://github.com/ashbrener/spec-kit-arch-governance/blob/5ac80346a3aa31595f03e7fe192fd44bb61ec518/scripts/repin.py) | Scoped, explicit repinning with a proposed result separate from application. | Pin the governing entries used by each artifact; require review reasons for changed pins. A pin refresh is acknowledgment, not new verification. |
| [Canon drift canonization](https://github.com/maximiliamus/spec-kit-canon/blob/64b7b0897f8344c2325eab9e2b4642d1caaed2f1/extension/commands/drift-canonize.md) | Resolve drift before applying changes to authoritative memory. | Use reconciliation to expose differences and route approved amendments. Do not automatically redefine intent to match implementation. |
| [Archive consolidation command](https://github.com/stn1slv/spec-kit-archive/blob/b9233a18a9d3f1f45b28fe3c066cfcd405a239e9/commands/archive.md) | Preserve source attribution when consolidating feature knowledge. | Link compact project entries to feature detail and preserve historical records. Do not create competing canonical copies of every spec and plan. |
| [Blueprint Index state checks](https://github.com/ogil109/spec-kit-blueprint/blob/43c332998d5d893c8d8ab83dbd55d3f38416e686/scripts/bash/lib/state-check.sh) | Deterministic mapping/freshness diagnostics and an explicit distinction between structural failures and softer drift signals. | Add architecture-part mappings, scoped drift checks, advisory recovery and required gates. Mandatory gates still block even when recovery preferences are advisory. |

The audits supplied another important influence: executable counterexamples. They
showed that strong instructions could coexist with a checker accepting insufficient
evidence, stale promises or broken upgrades. The v3 changes prioritize enforcing the
existing completion contract over adding more lifecycle stages. The audit response
preserves that finding-by-finding reasoning without requiring unpublished scratch notes.

## Decisions, benefits and tradeoffs

### 1. Give each kind of fact one authoritative home

The constitution owns working rules, product.md owns approved behavior,
architecture.md owns technical structure, and decisions.md owns the reasons and
rejected alternatives. Feature detail remains under specs/.

This follows the original product/architecture proposal and the community memory
approaches above. It should make conflicts easier to locate and reduce duplicated
truth. The cost is maintaining links and deciding which document owns a fact.
Compact decision rows keep the baseline small; long explanations belong in linked
research/design records rather than being squeezed into a table.
[Baseline templates](../extension/templates/).

### 2. Keep approved intent separate from observed delivery

A proposed or approved capability does not imply working implementation. Ownership,
delivery and part state are calculated on read from feature records; the checker
does not maintain shared status cells in the product/architecture files.

This responds to the original approval-versus-delivery distinction and the audit's
parallel-write conflicts. It should reduce misleading status and shared-file churn.
It requires adequate feature artifacts and mappings, and does not eliminate genuine
conflicts when two branches change the same approved intent.
[Status and ownership contract](../extension/commands/speckit.baseline.check.md).

### 3. Change baseline meaning only through an approved amendment

Recovery proposes inferred facts; reconciliation exposes differences; amendment
applies approved semantic changes. Implementation cannot approve itself by rewriting
the baseline. Decisions keep rejected alternatives and supersession history.

This adapts approval and drift-resolution ideas from ProductShape and Canon. It should
preserve user control and prevent the same settled question returning in each feature.
It adds review effort for material changes. Ordinary choices within approved scope
remain governed by the profile; an approval field is not cryptographic proof of who
approved it. [Amendment rules](../extension/commands/speckit.baseline.amend.md).

### 4. Load the context relevant to the current step

Specification consults product intent, product decisions and blocking questions;
planning consults the stack, affected parts, governing decisions and contracts.
Scoped retrieval must still include required global context.

The aim is to carry whole-project authority into per-feature work without loading
every historical document every time. The benefit is more focused context; the cost
is maintaining reliable scope mappings. Large/external contracts need separate
reading, and semantic conflict detection still requires judgment.
[Context command](../extension/commands/speckit.baseline.context.md).

### 5. Keep identities stable and preserve the promise historical tests proved

Do not silently renumber requirements/tasks, erase checked history, or repin an old
completed feature onto a newly amended promise. Changes features record predecessor
transitions while accepted historical evidence stays attached to its original inputs.

This combines traceability with the audits' changed-promise counterexamples. It should
make later changes explainable without pretending old tests verified new behavior.
The cost is a more explicit migration/revision protocol; legacy DONE reports need
new v3 evidence before becoming current verification.
[Identity and migration rules](../speckit-universal-profile.md#4-stable-identities-and-artifact-contracts),
[migration details](followup-audit-response.md#migration-and-practical-limits).

### 6. Bind completion evidence to the actual tested inputs

The runner executes planned quality gates, records exit codes and hashed logs, and
binds them to artifacts, governing entries, mapped code and local contracts. Shared
Verification inputs bind tooling to all features. DONE requires consistent, current
evidence, supported coverage and convergence.

The audits demonstrated that prose, cosmetic report edits and synchronization stamps
could otherwise hide stale results. Input bindings should expose that staleness. The
cost is rerunning checks when relevant inputs change; broad shared mappings can be
conservative. Editable local records do not establish trusted provenance, and passing
commands do not establish that assertions test the right behavior.
[Verifier contract](../extension/commands/speckit.baseline.check.md),
[runner](../extension/scripts/baseline_runtime.py).

### 7. Separate deterministic checks from semantic review

Python/Git checks validate IDs, schemas, pins, history, mappings and evidence bindings.
Analyze, architecture review, converge and user review assess whether the design and
assertions satisfy the promise. Declared executable architecture rules can supplement
that review.

This makes enforcement claims match the implementation. It provides repeatable
structural feedback while keeping responsibility for meaning explicit. It does not
automatically prove security, test adequacy, architectural correctness or production
outcomes. [Analysis](../preset/commands/speckit.analyze.md),
[architecture review](../extension/commands/speckit.baseline.review.md).

### 8. Use convergence to expose remaining work without rewriting intent

Converge can append traceable remediation to tasks.md. It returns tasks_appended,
gaps_remaining or converged; appending nothing is insufficient to claim success.
Its write limit protects application code, approved intent and existing history.

This addresses incomplete work hidden behind checked boxes or an empty findings list.
It should make repair handoffs clearer, at the cost of another review pass. The shipped
workflow is linear; repair and re-verification need an explicit return to implementation.
[Convergence command](../preset/commands/speckit.converge.md).

### 9. Adopt at the phase that actually exists

New projects establish approved intent. Existing codebases recover and reconcile it.
Existing Spec Kit projects retain their integration and artifacts. Behavior-preserving
fixes/small changes use lighter paths; optional product modules apply only when relevant.

This avoids a costly restart simply because a tool was installed. It should preserve
useful history and make adoption practical across the four scenarios. Recovery still
needs evidence and decisions; advisory mode does not waive required completion gates.
[Adoption scenarios](installation-and-adoption-scenarios.md),
[phase-entry rules](../speckit-universal-profile.md#12-start-from-the-phase-that-exists).

### 10. Package supported customization and make updates recoverable

Use a preset, extension and workflow, pin the tested CLI, and generate the prepared
installation reproducibly. CLI-backed installation keeps an existing agent setup;
manifest validation and snapshots restore managed files after failed installation
steps. Checker writes use a checkout lock, compare-before-apply and a recovery journal.

This uses Spec Kit's customization surfaces and addresses reproduced upgrade/write
failures. It should reduce upgrade damage and partial state. It adds filesystem and
version constraints: POSIX locking, a tested CLI pin, and no guarantee against arbitrary
external concurrent edits. Installer rollback does not undo global CLI changes or Git
metadata. [Installer](../install.sh), [transaction storage](../extension/scripts/baseline_store.py).

### 11. Keep local completion distinct from publishing and deployment

Local hooks provide feedback; configured CI can enforce repository gates. Branch
protection requires repository settings. Publishing/deployment becomes a separate
deliverable when requested. Agents must not add themselves as contributors.

The goal is reproducible local development with explicit responsibility for external
actions and authorship. It avoids requiring a hosting provider for ordinary feature
completion. It also means local DONE is not RELEASED, operational validation, or a
protected merge. [Local authority](../speckit-universal-profile.md#0-authority-terminology-and-portability),
[version-control policy](../speckit-universal-profile.md#10-local-version-control).

## Approaches deliberately rejected

These are current policy choices, not missing features to work around.

| Approach | Why it was rejected | Benefit of the chosen policy / cost |
|---|---|---|
| Accept a required skip/xfail because its explanation sounds reasonable | An explanation does not verify the promised behavior. | Missing verification stays visible; unavailable prerequisites can block completion. Optional checks would need an explicit requirement-level policy. |
| Update approved intent automatically to match code | Implementation would become its own approval authority. | Preserve accepted behavior; material deviations require review or code repair. |
| Let a stamp, repin or edited report renew successful tests | These record acknowledgment/reconciliation, not execution against changed inputs. | Avoid stale completion claims; relevant changes need a new run. |
| Treat every ID ever committed as permanently accepted | Drafts and reverted proposals are not all governing history. | Compare against an accepted/PR base and HEAD; preserve and fetch the configured comparison history. |
| Certify semantic correctness from matching IDs, checkboxes or a zero findings count | Structural consistency cannot judge assertions or omitted behavior. | Keep semantic review explicit; the checker cannot independently certify the whole application. |
| Copy a complete prepared setup over an existing Spec Kit installation | It can replace the agent, custom hooks and other tooling. | Integrate through supported CLI operations; existing projects require the CLI. |

The [audit response](followup-audit-response.md#positions-i-defend) gives the concrete
counterexamples and reasoning behind these choices.

## Work not implemented, and why

This table distinguishes deliberate scope boundaries from unresolved gaps. The reasons
describe the current engineering tradeoffs, grounded in the shipped design and audit
response; they do not invent undocumented historical motives. Revisit conditions are
criteria for discussion, not scheduled commitments.

| Item | Current status and reason | What would justify revisiting it |
|---|---|---|
| First-class release, rollback and production-outcome loop | Outside the current local completion model. No universal deployment/observability environment is supplied. Application plans may still define rollout requirements. | An approved operational workflow with provider, evidence, permissions and rollback contracts. |
| Automatic workflow repair loop | Not implemented; the linear workflow hands gaps back to implementation. No unconditional retry can resolve a blocked decision or prerequisite. | Bounded retries, persisted outcomes, resumability and tests for failures/blockers. |
| Generated roadmap/stakeholder views | Deferred. The capability index and calculated status already supply the underlying facts; another manually maintained status document would duplicate them. | A derived view with clear consumers and no independent authority. |
| Separate delta proposal/apply/archive engine | Proposed during design, not shipped as a full change-object lifecycle. Approved amendments, reconciliation and Changes transitions cover current needs. | Durable proposals, dependency accounting and atomic semantic application beyond existing checker-state transactions. |
| Full ADR files as the mandatory default | Compact decisions.md rows are shipped; linked detail remains possible. Requiring an ADR tree for every choice adds maintenance. | Decisions that consistently exceed the compact format or a team's established ADR convention. |
| Persistent semantic-analysis findings gate | Analyze remains a read-only review command. A stored zero count alone would be easy to stale or fabricate. | A findings schema bound to assessed inputs, explicit resolution history and reviewed acceptance rules. |
| Native Windows/PowerShell and external feature roots | Not supported by the current Bash/POSIX checker and repository-local specs contract. Windows uses WSL. | Dedicated portability work and end-to-end tests for locking, paths, hooks and evidence. |
| Generic adapters for other development tools | Not implemented. Installation recognizes Spec Kit; another tool needs explicit artifact ownership and schema mapping. | A named target tool, a tested adapter and agreement about authoritative artifacts. |
| Trusted remote runner/attestation | Local records are editable. Adding trust requires an identity/security/infrastructure design beyond input hashing. | A defined threat model and verified provenance channel. |
| Automatic branch protection and application CI provisioning | The supplied scaffold cannot know every project's runtime/services or repository settings. | An explicitly authorized repository/provider integration with concrete configuration. |
| Guaranteed direct-agent hook ordering | Known integration gap: priorities are registered and the CLI executor sorts, but generated prompts do not explicitly require the sort. | Tested priority handling in every supported agent path; until then follow the adoption guide's explicit ordering instruction. |
| Complete conflict-free parallel semantic amendments | Per-feature evidence reduces shared writes, and checker transactions protect local state. Approved baseline edits can still conflict across branches; semantic amendment commands are not a distributed transaction system. | A baseline proposal/merge protocol with dependency-aware conflict resolution. |

Brand assets, admin/content behavior, native platforms and live end-to-end verification
are [optional modules](../modules/), not forgotten requirements. A module's relevance
comes from the actual product; installing every possible framework or service is not
part of adoption.

## Evidence and maintenance

The [audit validation record](followup-audit-response.md#validation) reports 88 passing
tests, checker coverage and repeatable template generation. The [adoption guide's
validation](installation-and-adoption-scenarios.md#research-validation) records four
disposable installation/gate scenarios. These support specific implementation claims;
they do not measure productivity gains or certify interactive agent semantics.
Benefits in this document are design expectations, not benchmark results.

When a material design choice changes, update this rationale, the operative contract
and affected tests/docs together. Preserve superseded reasoning and link its replacement.
Do not make future capability claims by editing this overview alone.
