# Module: Local live end-to-end operations

- **Part of:** [Spec Kit Universal Adoption and Execution Profile](../speckit-universal-profile.md)
- **Apply when:** the product has running services and at least one client that talks to them. Otherwise record this module N/A with the reason.

The core profile still governs: statuses, evidence, freshness, and completion follow its sections 6–8, and every concrete value comes from the target project.

Produce or amend a runbook equivalent to `docs/live-testing.md`, linked to the native and content guides where present. Separate setup, reachability, compile/runtime, acceptance observations, diagnostics, evidence, and teardown.

## 1. Prerequisites and topology

- Start the actual configured backend/services with safe local configuration. Seed disposable actors and realistic files/objects through the project-supported path; verify required buckets/permissions or equivalent services.
- Record exact locked SDK/toolchain components, revisions, archive checksums where the runner supports them, OS/browser/device identifiers, acceleration, and fixture inputs.
- Resolve API **and asset/media** addresses from the client/device's network perspective. A host precheck does not prove device access. Confirm actual target-side reachability, signed/public access policy, manifests/segments if relevant, and environment-specific transport restrictions.
- Use supported local networking by default. Scope any cleartext development exception narrowly; do not weaken production transport policy.
- Validate prerequisite failures before diagnosing the app. Reachability failure identifies a setup/dependency gap, not automatically a client defect.
- Prefer bounded startup/health helpers with readiness deadlines, actionable diagnostics, and explicit teardown.

## 2. Acceptance walkthrough

1. Run the installed app/client against the local test stack and establish the actual user role/scope.
2. Visit required hierarchy/navigation, content, offline/runtime, and operator surfaces. Check relevant locale/directionality, state/recovery, and no crashes; capture sanitized rendered evidence.
3. Exercise positive and negative authorization through the actual interface. Correlate the response/server record with user-visible feedback and resulting state. A server refusal does not alone prove the user sees an actionable reason.
4. For downloadable content, verify progress/completion and correct control-state changes; disable **all relevant transport** and verify the network is actually unavailable, then open/play each promised type from local storage. Merely disabling cellular data is insufficient if another transport remains usable.
5. Attempt a new download offline. Assert the approved user message, queued behavior, automatic resume/retry on reconnection, and resulting content integrity where promised.
6. Exercise live refresh after operator updates, manual refresh, background/resume, and active-context changes. Assert that context labels, displayed descendants, caches, and navigation reconcile together; stale descendant pages must not expose the previous context if the specification promises their closure.
7. Record measurements and evidence per AS/TR/SC.

## 3. Repeatable E2E coordinator

Where the project has an existing end-to-end command, preserve and document it. If the current requirements justify building one, use isolated test-only actors/data, real permitted operator submissions, client refresh, sanitized diagnostics/screenshots/timings, and teardown. Constrain credentials and destinations; reject accidental production targets. Do not expose tokens/passwords through CLI arguments or retained traces. Keep exact commands project-specific in the resulting runbook.

## 4. Local phones and optional tunnels

Use a reachable private address, supported device forwarding, or another approved local route as appropriate. Treat API and object storage as separate endpoints when the topology requires it. Build-time endpoint configuration binds a build to that configuration; record it without retaining sensitive/transient hostnames.

An external tunnel/preview is optional exploratory infrastructure, subject to explicit authorization for external exposure. If authorized, stop it afterward, restore service URL configuration, and remove transient endpoints from retained artifacts. It is not a default completion dependency.

## 5. Success criteria and teardown

Map separately: each platform's visible behavior; download/offline use on promised platforms; allowed/refused upload/write paths; device-to-service/asset reachability; and reproducibility of the documented process. Stop emulators/VMs and dispose only of identified test-owned data after capture. Preserve persistent development environments; distinguish stop from destructive remove.
