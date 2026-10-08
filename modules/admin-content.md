# Module: Staff administration, content, and stateful workflows

- **Part of:** [Spec Kit Universal Adoption and Execution Profile](../speckit-universal-profile.md)
- **Apply when:** the product has staff/operator roles, moderated or operator-managed content, uploaded media, or stateful enrollment/progression. Apply only the sections whose subject exists in the product; record the rest N/A with the reason.

The core profile still governs: authorization follows its section 3.2, testing and evidence follow sections 6–8, and every threshold, count, role, and format comes from the target's approved domain.

Produce or amend an operator-oriented content runbook without leaking implementation detail into ordinary product screens.

## 1. Constitution principle: scoped staff/operator administration

Add this principle when staff/operator and exceptional technical authority exist. Identify the official interface and approved workflows.

- Scope reads, choice lists, related-object selectors, direct URLs, forms, bulk actions, and writes consistently at the trusted boundary.
- Reject revoked, inactive, forged, stale, and cross-scope authority, including the next write from an already active session after revocation.
- Ordinary staff cannot create/promote staff or grant themselves authority unless expressly specified. Exceptional correction powers and audit expectations must be explicit.
- Do not introduce a separate staff app until observed workflows show the existing interface cannot serve them safely, clearly, or efficiently.
- Test actual staff requests/forms/actions. Service tests supplement rather than certify the interface.

## 2. Identity, staff provisioning, and scope

Distinguish end-user authentication/provisioning from staff authentication. An end-user creation form may not provision an operator account; document the actual supported route, password/credential prompts, and idempotent update behavior where provided.

Prefer least-privileged scoped operators to technical superusers. Define who may create/promote staff and grant exact scopes; test no-assignment behavior, permitted reads/writes, refusal outside scope, revocation during an existing session, and stale authority.

If authority is tied to time/context/entity combinations, document exact assignment, active-versus-historical edit rules, separate historical moderation permissions, and whether assignments carry forward. Do not assume rollover.

## 3. Moderation, removal, and restoration

Resolve report thresholds from approved policy. If distinct reporters are required, enforce uniqueness. Determine whether even exceptional roles must meet eligibility. Test reversible visibility/removal, eligible staff inspection, restoration, retained history, and protection against duplicate reports or bypasses.

## 4. Membership, enrollment, progression, and correction

For stateful enrollment/progression or analogous workflows, specify authoritative invariants: membership creates required related records exactly once; all prerequisite outcomes exist before advancement; repeats/retries create only required follow-up records; terminal stages do not create phantom next-stage containers; final success records completion automatically when promised.

Define final versus provisional outcomes, failure boundary cases, idempotence, transactions, retries, exceptional correction with reason/history, and reconciliation of only records caused by the corrected outcome.

## 5. Hierarchy and supported operator surfaces

Document actual creation dependencies from parent to child and how to obtain stable identifiers. Identify supported operator pages for users, structure, material, links, reports, deactivation/reassignment, and moderation. Identify which file types can be uploaded in the official form and which require preprocessing; reject unsupported input clearly rather than allowing a delayed runtime failure.

## 6. Material ingestion and storage contracts

- Resolve supported formats, storage-key semantics, URL assembly, manifests, segments, MIME types, permissions, duration/page metadata, and rendering/playback clients. Use the protocol the project actually supports; streaming formats such as HLS are one option, not a requirement.
- Where HLS is used, distinguish a playlist/segment directory contract from a raw media-file key. Validate preprocessing and manifests before attachment. See [RFC 8216, HTTP Live Streaming](https://www.rfc-editor.org/rfc/rfc8216.html) for the playlist and media-segment relationship.
- Prefer an existing ingestion helper that validates, transforms/transcodes, uploads, and attaches coherently. Document inferred kind and explicit override, metadata extraction and optional tooling, replacement/update semantics, and where preprocessing tools run.
- Keep tools in the correct environment according to the target architecture.
- Verify the API record and fetched content, referenced playlists/segments, actual playback/opening, and representative clients. HTTP success plus expected MIME type is a reachability precheck, not proof that a client can decode, play, download, or open it.
- Seed real representative media/assets where these behaviors are promised. Mock-only payloads cannot certify actual playback or offline storage.

## 7. Refresh, offline behavior, and testing authentication

Only expose active-context content according to approved rules. Exercise refresh, download, offline use, and recovery through the acceptance walkthrough in [live-e2e.md](live-e2e.md#2-acceptance-walkthrough), steps 4–6, and preserve the approved localized feedback.

Use disposable local accounts and supported development authentication. If an existing debug OTP/login bypass is intentionally present, verify its production rejection and prevent capture in evidence. This module does not authorize adding a bypass or harvesting production login codes. Keep credentials/tokens/cookies out of commands and retained outputs.
