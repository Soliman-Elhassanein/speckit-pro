# Module: Native and platform-specific verification

- **Part of:** [Spec Kit Universal Adoption and Execution Profile](../speckit-universal-profile.md)
- **Apply when:** the product ships native code or makes promises about OS-level behavior on a specific platform. Otherwise record this module N/A with the reason.

The core profile still governs: its section 6.3 defines which kind of evidence can support which claim, and a required capability that is unavailable is BLOCKED, never N/A.

## 1. Capability matrix

Record the target's actual environment:

| Platform/environment | Build/compile | Unit/package | Native integration | Rendered UI | Physical OS behavior | Prerequisites / evidence |
|----------------------|---------------|--------------|--------------------|-------------|----------------------|--------------------------|
| <actual target> | <check status> | <check status> | <check status> | <check status> | <check status> | <versions, resources, method> |

Compilation, local unit/widget tests, native runtime, visual rendering, and physical-device acceptance are different claims. Do not remove a supported platform without an explicit product decision.

## 2. Android or equivalent local emulator

- Pin the SDK/system image/tool inputs required by the target. Verify acceleration, device discovery, bounded boot readiness, and the intended build variant.
- Run app/package static checks, non-device plugin tests, and device integration selectors from their correct directories. Root tests must not silently omit separately configured packages.
- Resolve host networking correctly. For the Android Emulator's documented virtual router, `10.0.2.2` aliases the host loopback; it is not a universal physical-phone or arbitrary-emulator address. See [Android Developers, Network address space](https://developer.android.com/studio/run/emulator-networking-address).
- Capture screenshots and native logs where relevant.
- Document start/wait/headless/stop operations supported by the actual helpers. Boot times, device names, API levels, and build results observed on another machine are not evidence for this one.

## 3. Apple/iOS or equivalent proprietary platform

- Use an available, authorized, supported local build environment and current compatible toolchain. Verify platform licensing/support and the user's actual hardware before choosing any virtualized environment.
- For iOS build/simulator work, install/select full compatible Xcode, required SDKs and runtimes, dependencies, and accepted license prerequisites. The standalone macOS Command Line Tools package is not a substitute for Xcode-only `xcodebuild`/`simctl` tooling. See Apple's [Xcode command-line tool reference](https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference) and [Installing the command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools).
- Transfer the project locally through an authorized route, excluding generated build/cache output and keeping secrets confined. Use exact committed dependency inputs. Do not require a remote clone as the only route.
- Resolve backend connectivity from that environment. Run configured analysis/unit checks, platform builds, and simulator integration separately. An unsigned build demonstrates only the relevant build claim; it does not certify install/signing, rendering, or physical behavior.
- If a VM can compile but cannot provide required graphics/simulator functionality, retain compile evidence and mark rendered/device checks BLOCKED. Do not equate a booted VM with a working simulator.
- Use a locally installed signed development build where physical behavior requires it. Verify the actual account/signing prerequisites rather than assuming every development test needs a paid account. Some hardware-specific features are unavailable in simulation. See Apple's [Running your app on simulated or physical devices](https://developer.apple.com/documentation/xcode/running-your-app-on-simulated-or-physical-devices).
- Define explicit physical observations for each promised OS integration, such as background execution, notifications, lock-screen controls, file visibility, or backup behavior. Verify current platform capability for each.

## 4. Resource, lifecycle, and setup discipline

Budget actual RAM, CPU, storage, acceleration, backend load, and rendering capabilities before starting environments. Serialize heavy sessions if concurrent execution is infeasible.

Use a supported diagnostic/readiness check before creation. Document first-boot manual steps when applicable, persistent environment identity, start/stop, local access, and destructive removal separately. Never copy default VM passwords into a target runbook or retained evidence. Optional cloud previews cannot replace locally authoritative required evidence.
