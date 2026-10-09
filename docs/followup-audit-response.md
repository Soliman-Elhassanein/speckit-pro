# Response to the two follow-up audits

Reviewed `tmp/speckit-pro-audit (copy 1).md` and
`tmp/speckit-pro-followup-audit.md` against the working tree based on `66e2cbb`.
Most reproduced defects are valid. Their proposed remedies are not interchangeable:
verification, historical authority, reconciliation and semantic review need separate contracts.
This implementation advances the profile/preset to 3.0.0, baseline extension to 0.6.0,
and workflow to 1.2.0. It changes the persistence and completion contract.

For the broader inspiration, design tradeoffs and deferred scope, see the
[design rationale](design-decisions-and-rationale.md).

## First audit

| Finding | Decision and implementation |
|---|---|
| A1: targeted repin blocked by another feature | Fixed. Valid feature pins can be saved independently; other feature errors remain visible. Global structural/history errors still block acceptance. |
| A2: unrelated feature blocks implementation | Fixed with explicit `--feature <folder>` / `--feature current`. Workflow and command forms scope feature diagnostics. CI remains global intentionally. |
| A3: amended promise deadlocks Changes spec | Fixed with a frozen predecessor/from/to transition. Historical accepted proof stays on the old promise; the new feature proves the new revision. Subsequent changes name Previous change. |
| A4: cosmetic verification edits renew evidence | Fixed. A typed run binds artifact, baseline, contract and code digests. Report edits cannot renew it. |
| A5: committed deletion becomes invisible | Fixed against an accepted or PR-base commit plus HEAD. Rejected the proposed scan of every historical ID; see below. |
| A6: parallel features rewrite shared cells/state | Fixed. Ownership, delivery and part state are calculated on read. Feature evidence is stored per feature; synchronization stamps are per part. Independent features no longer edit neighboring product rows. |
| A7: lowercase failure outside Coverage passes | Fixed. Unknown statuses, including lowercase variants, fail; failure detection is case-insensitive. |
| A8: skips/xfails pass | Fixed. Nonzero required skip/xfail counts or matching run output block completion. A reason alone does not waive a required check. |
| A9: nonexistent plain evidence path passes | Fixed. Plain paths and Markdown links must resolve inside the repository. Machine logs must also match their hashes. |
| A10: unescaped pipe truncates a command | Fixed. Table widths are validated before commands are considered. Escape pipes; Bash uses pipefail. |
| A11: every angle-bracket token is a placeholder | Fixed. Known template markers are checked; actual component names such as `<LoginBanner>` remain valid evidence text. |
| A12: nested contract spec.md becomes a feature | Fixed. Feature discovery visits shallow folders first and excludes descendant spec.md files beneath an established feature. Independent nested feature roots remain supported. |
| A13: premature “pinned” success message | Fixed. Write messages follow successful transactions. Dry-run messages explicitly describe proposed writes/commands. |
| A14: ordinary tooling is unmapped by default | Added a Tooling map to the architecture template. Shared Verification inputs explicitly bind tooling to every feature. Projects retain responsibility for their actual paths and hidden deployment/CI folders. |
| A15: abandoned work hides drift; unfinished stamping | Added ABANDONED and inactivity diagnostics. Abandoned features provide no drift exemption. Scoped stamps require supported DONE; stamps never renew tests. |
| A17: branch hook runs before intake | Baseline before_specify now has priority 1, registered by the pinned CLI. The CLI hook executor sorts it before ordinary priority-10 hooks. Generated agent prompts do not explicitly require sorting; direct agent execution must honor priorities as described in the adoption guide. This does not create a workflow-routing engine. |
| A18: decisions lacks version line | Added Version and Last amended to the decisions template. Version classification remains an approved amendment responsibility. |
| A19: enforcement claims overstate implementation | Rewrote the profile, command contract, adoption prompt and README. Required gates, advisory recovery, evidence limits and branch settings are explicit. No claim of automated semantic correctness or automatic branch protection. |

The audit skips A16; no finding has been silently omitted under that number.

## Second audit

| Finding | Decision and implementation |
|---|---|
| R01: reports substitute for a new run | `--record-run` executes every planned quality gate, writes an identified run and hashed logs, and binds the inputs. Markdown execution commands, directories and evidence must match it. |
| R02: deleting an adopted baseline disables gates | Missing product.md fails when adoption state, pins or repository history establish adoption. `--gate` requires it even for a non-adopter. |
| R03: advisory weakens mandatory gates and acceptance | Mandatory gates always block and reject mutation/recovery combinations before any action. Advisory diagnostics cannot accept invalid DONE evidence. |
| R04: empty commands/evidence/counts/plan accepted | Complete quality-gate schema, verification plan, numeric execution counts, existing logs and typed observations are required. Invalid or unknown statuses fail. Manual evidence needs method, platform, expected/observed result and a digest. |
| R05: missing completed pins and governing changes ignored | Completed pins must exist and be valid. Run bindings cover governing rules, decisions, constitution, parts and local contracts; changes invalidate current completion. Historical proof is checked against its preserved accepted record. |
| R06: stamping changed code restores verification | Code fingerprints are independent of reconciliation stamps. Neither stamps nor active neighboring features excuse stale current evidence. |
| R07: Changes evolution blocked | Accepted predecessor transitions preserve historical revisions rather than reanchoring old tests. Tests cover preparation, completion and multiple sequential changes. |
| R08: first DONE bypasses open questions/decisions | Approval, open-question and cited-decision checks apply before first or renewed current acceptance. |
| R09: weak CI/history and no final gate | CI fetches full history, supplies the PR base, and runs `--gate --strict`. Gates execute architecture-rule checks. Workflow adds a final scoped `--require-done` gate. |
| R10: context suppresses errors/contract contents | Context reports structural errors and returns failure for incomplete authority. Local contracts are loaded up to 64 KiB; larger and external references are explicitly identified for separate reading. |
| R11: valid JSON with wrong shape crashes | Validate nested state and run schemas; report controlled diagnostics. Corrupt accepted state must be restored, not deleted to erase history. Invalid state is not overwritten by a mode change. |
| R12: file renames are not a transaction | Added a checkout lock, unique temporary files, fsync, compare-before-apply, a rollback journal and interruption recovery. Gates refuse interrupted transactions until recovery. File additions during validation also abort acceptance. |
| R13: advisory initialization before product is ineffective | Explicit recovery mode can initialize before a baseline exists. Discovery remains permissive only for a non-adopter. |
| R14: failed upgrade removes existing preset | Validate incoming manifests before removal; snapshot installation files and restore them on failed CLI steps. CLI diagnostics remain visible. Registry rewriting uses JSON rather than path-sensitive sed substitution. |

## Positions I defend

**An explanation for a skipped test is not verification.** The first audit's suggested
“passes with a reason” would certify a requirement that was not checked. The second
correctly rejects that remedy. This implementation keeps every planned gate required.
If a project wants optional checks or approved exceptions, that needs an explicit
requirement-level policy; prose alone cannot convert a missing result into PASS.

**Every historical draft is not an accepted baseline.** Scanning all IDs ever committed
would forbid removing reverted proposals and would make shallow history a different
policy. An accepted revision or PR base is the meaningful comparison. Missing configured
history fails visibly. Local adoption defaults to HEAD; CI supplies its comparison explicitly.
A completely erased adoption trail cannot be discovered from absent local state alone;
required gates still fail when the baseline is missing.

**Reconciliation does not establish test freshness.** An active feature can explain why
code moved, and a stamp can record a reviewed synchronization point. Neither proves
that the completed feature was tested against the changed code. Current run digests
remain mandatory even when drift routing considers the change expected.

**Old tests must stay attached to their old promise.** Repinning an old owner onto a new
capability to unblock a Changes feature would falsify its historical meaning. Frozen
transitions avoid that. Historical treatment requires accepted evidence for all named
capabilities in the feature; mixed historical/current features are checked conservatively.
New promises need new evidence.

**A runner improves provenance without proving semantics.** The original blanket claim
that software cannot establish whether a command ran was too broad: this runner executes
commands and collects exit status and logs. Local editable records are still not trusted
attestation. The checker cannot judge assertion adequacy or whether a human observation
was truthful. Analyze, converge and user review retain that responsibility.

**Hooks and YAML do not configure a protected merge boundary.** Structural pre-commit
feedback is useful, but bypassable. Foreign hooks are preserved and integration guidance
is printed. The sample CI needs the project's runtime/services and repository settings
must require its job. Automatically copying YAML would not establish branch protection,
and assuming a generic runtime would make valid projects fail for setup reasons.

**More lifecycle machinery is a separate product choice.** Roadmaps, release/rollback
stages, external feature roots, PowerShell and larger ADR layouts are deferred. A durable
semantic-analysis findings artifact may be useful, but a fabricated/stale zero count would
not prove clean analysis. The existing analysis review remains a human gate; this change
makes no claim that the script independently proves semantic analysis or convergence.
Those additions do not substitute for the reproduced correctness fixes.

## Migration and practical limits

1. Preserve existing pins and historical evidence. Existing DONE reports require a v3 run
   before they count as current verification. Do not delete corrupt accepted records to reset them.
2. Establish an accepted base with `--write --base <commit>`. CI uses the PR base and full history.
3. Review stale pins with `--repin <feature>/spec.md` or plan.md and `--reason`. Spec changes
   additionally require `--feature <feature> --acknowledge --reason` after downstream review.
4. Execute `--record-run --feature <feature>` on final inputs. Copy its exact commands and
   log paths into verification.md, complete coverage and convergence, then accept with
   `--write --feature <feature>` and check `--gate --require-done --feature <feature>`.
5. Migrate a predecessor on its still-current promise before amending that promise and
   preparing a Changes spec. A legacy historical report cannot be invented into new proof.
6. Old Delivery/Owning spec/State columns are ignored. New templates omit them. Old
   synchronization hashes may need a reviewed stamp because hashing now uses actual
   working-file bytes and handles Unicode filenames safely.

Bindings cover mapped parts, shared Verification inputs and repository-owned local
contracts. Ignored files, external services and unmapped configuration require deliberate
scope and review. Spec/plan prose changes conservatively invalidate their entire artifact;
checkbox bookkeeping and report-only edits do not. Required gates run declared executable
rules, not every feature's full quality gates; freshness uses saved input bindings.

Transactions serialize participating checker processes and detect intervening edits before
application. Uncoordinated editors do not honor that lock; it is not a distributed database
or a guarantee against arbitrary simultaneous external writes. Installer rollback covers
failed CLI/file-install steps, not global `--with-cli` changes or new Git metadata. Avoid
concurrent installers in one target; interruption by an uncatchable kill is outside its rollback.

## Validation

- All **88 tests passed** on Python 3.11 with `SPECKIT_REAL_CLI=1`, including
  all 13 adapted first-audit regression cases, follow-up evidence/state transitions,
  concurrent writes, interrupted recovery, real pinned-CLI Codex/Claude installs,
  updates, no-CLI installation and injected failure at every CLI installation stage.
- Tests invoke the exact shipped workflow shell gates and CI shell command,
  checking success, unsupported completion and missing baseline failures.
- Subprocess-aware line coverage with coverage.py 7.16.2: checker **95.21%**,
  transaction storage **96.72%**, bounded runner **85.00%**; combined **94.92%**.
  The first audit's 95% checker criterion is met. CI enforces that threshold for
  the checker, and reports the helper coverage separately. Coverage includes
  scan/touched paths; these percentages do not establish semantic correctness.
- Full template rebuilt using Spec Kit **1.1.2**. A repeated rebuild matched all
  **77 files** byte-for-byte and preserved their executable modes. Generated
  Python caches are excluded, and registry timestamps are normalized.
- Source/template comparisons, Python 3.11 syntax, shell syntax, YAML parsing
  and `git diff --check` passed.

Run regression/installer checks with:

```sh
SPECKIT_REAL_CLI=1 python3 -m unittest discover -s tests -v
```

For subprocess-aware coverage, install coverage.py 7.16.2, set
`SPECKIT_CHECKER_SOURCE` to the absolute extension/scripts directory, and use
`tests/coverage.ini` (the exact commands are in `.github/workflows/tests.yml`).
Real-CLI smoke tests require the pinned CLI on PATH; ordinary test runs skip that
one method if SPECKIT_REAL_CLI is unset. The reported final run skipped none.
