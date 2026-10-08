# Module: Operator administration, managed content, and stateful workflows

- **Part of:** [Spec Kit Universal Adoption and Execution Profile](../speckit-universal-profile.md)
- **Apply when:** the product has operator/administrator roles, user-reported or operator-managed content, uploaded files or media, or multi-step workflows whose state advances over time. Apply only the sections whose subject exists in the product; record the rest N/A with the reason.

The core profile still governs: authorization follows its section 3.2, testing and evidence follow sections 6–8, and every threshold, count, role, and format comes from the target's approved domain.

Produce or amend an operator-oriented runbook without leaking implementation detail into ordinary product screens.

## 1. Constitution principle: scoped operator administration

Add this principle when operator roles and exceptional technical authority exist. Identify the official operator interface and approved workflows.

- Scope reads, choice lists, related-object selectors, direct URLs, forms, bulk actions, and writes consistently at the trusted boundary.
- Reject revoked, inactive, forged, stale, and cross-scope authority, including the next write from an already active session after revocation.
- Ordinary operators cannot create/promote operators or grant themselves authority unless expressly specified. Exceptional correction powers and audit expectations must be explicit.
- Do not introduce a separate operator application until observed workflows show the existing interface cannot serve them safely, clearly, or efficiently.
- Test actual operator requests/forms/actions. Service tests supplement rather than certify the interface.

## 2. Identity, operator provisioning, and scope

Distinguish end-user authentication/provisioning from operator authentication. Document the actual supported route for creating each kind of account, its credential prompts, and idempotent update behavior where provided.

Prefer least-privileged scoped operators to technical superusers. Define who may create/promote operators and grant exact scopes; test no-assignment behavior, permitted reads/writes, refusal outside scope, revocation during an existing session, and stale authority.

If authority is tied to a period, context, or entity, document exact assignment, current-versus-historical edit rules, any separate permissions for historical records, and whether assignments carry forward. Do not assume they do.

## 3. Reported content, removal, and restoration

Resolve report thresholds from approved policy. If distinct reporters are required, enforce uniqueness. Determine whether even exceptional roles must meet eligibility. Test reversible visibility/removal, eligible operator inspection, restoration, retained history, and protection against duplicate reports or bypasses.

## 4. Stateful multi-step workflows

For workflows whose state advances in steps, such as onboarding, orders, approvals, or subscriptions, specify authoritative invariants: entering a state creates its required related records exactly once; all prerequisite outcomes exist before advancement; repeats/retries create only the required follow-up records; a terminal state creates no further records; completion is recorded automatically when promised.

Define final versus provisional outcomes, failure boundary cases, idempotence, transactions, retries, exceptional correction with reason/history, and reconciliation of only the records caused by the corrected outcome.

## 5. Structure and supported operator surfaces

Document actual creation dependencies from parent to child records and how to obtain stable identifiers. Identify the supported operator pages for accounts, structure, content, links, reports, and deactivation/reassignment. Identify which file types can be uploaded in the official form and which require preprocessing; reject unsupported input clearly rather than allowing a delayed runtime failure.

## 6. File and media ingestion and storage contracts

- Resolve supported formats, storage-key semantics, URL assembly, manifests, segments, MIME types, permissions, metadata such as duration or page count, and rendering/playback clients. Use the formats and protocols the project actually supports.
- For segmented streaming formats, distinguish a playlist/segment directory contract from a single media-file key, and validate preprocessing and manifests before attachment. For HLS, see [RFC 8216](https://www.rfc-editor.org/rfc/rfc8216.html) for the playlist and media-segment relationship.
- Prefer an existing ingestion helper that validates, transforms/transcodes, uploads, and attaches coherently. Document inferred kind and explicit override, metadata extraction and optional tooling, replacement/update semantics, and where preprocessing tools run.
- Keep tools in the correct environment according to the target architecture.
- Verify the API record and fetched content, referenced playlists/segments, actual playback/opening, and representative clients. HTTP success plus expected MIME type is a reachability precheck, not proof that a client can decode, play, download, or open it.
- Seed real representative files/media where these behaviors are promised. Mock-only payloads cannot certify actual playback or offline storage.

## 7. Visibility, offline behavior, and test authentication

Expose content only according to approved visibility rules. Exercise refresh, download, offline use, and recovery through the acceptance walkthrough in [live-e2e.md](live-e2e.md#2-acceptance-walkthrough), steps 4–6, and preserve the approved user-facing messages.

Use disposable local accounts and supported development authentication. If a debug login bypass is intentionally present, verify its production rejection and prevent capture in evidence. This module does not authorize adding a bypass or harvesting production login codes. Keep credentials/tokens/cookies out of commands and retained outputs.
