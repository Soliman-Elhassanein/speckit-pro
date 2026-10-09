# Installing and adopting speckit-pro in four project scenarios

Research date: 2026-10-09. Tool: speckit-pro.

The installation decision depends on whether Spec Kit already exists. The adoption
decision depends on whether application implementation already exists. Installing
files, adopting governance, and verifying application behavior are separate results.

This guide targets the **post-audit profile/preset 3.0.0**, baseline extension
0.6.0, workflow 1.2.0, and tested Spec Kit CLI **1.1.2**. At the start of research,
public main reported profile **2.3.0**. The v3 updates are published alongside this
guide; older checkouts do not contain the evidence/gate behavior described below.
Confirm the profile's Version line and use a checkout containing these updates.
[Public profile](https://raw.githubusercontent.com/Soliman-Elhassanein/speckit-pro/main/speckit-universal-profile.md),
[local installer](../install.sh), [local adoption prompt](../adoption-prompt.md).

## Decision table

| Scenario | Installation | Configuration/adoption | First use |
|---|---|---|---|
| 1. No implementation, no Spec Kit | Initialize the chosen agent integration and add speckit-pro; Codex can also use the ready-made no-CLI route | Establish constitution and an approved product/architecture/decision baseline | Start the first approved feature |
| 2. Implementation, no Spec Kit | Add the tool structure around the existing repository | Recover the baseline from code/tests/docs; review inferred intent; reconcile in advisory mode | Continue an existing change or select the next approved one |
| 3. No implementation, existing Spec Kit | Add preset, extension and workflow through the CLI; keep the existing integration | Amend existing governance in place; create only missing approved baseline material | Continue the current spec/plan/tasks phase or start the first feature |
| 4. Implementation, existing Spec Kit | Add through the CLI; retain integration, other extensions and project settings | Recover/reconcile baseline and migrate active feature evidence without regenerating historical artifacts | Resume the actual active phase; analyze/converge unsupported completion claims |

An unrelated development tool is not detected or adapted automatically. See the
compatibility section before applying scenarios 3 or 4 to something other than Spec Kit.

## Shared prerequisites and installation behavior

Use Linux/macOS with Bash, or WSL on Windows. The shipped installer/hooks use shell
scripts and the checker uses POSIX file locking. Have Git, Python 3.11+, and PyYAML
available to the `python3` used during installation. Spec Kit's pinned package also
requires Python 3.11+, but its isolated installation does not make PyYAML importable
by every other Python interpreter. [Pinned package requirements](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/pyproject.toml),
[uv tool environments](https://docs.astral.sh/uv/concepts/tools/).

Check the actual environment:

```sh
git --version
bash --version
python3 --version
python3 -c 'import yaml; print(yaml.__version__)'
specify --version
```

The last check is optional for the ready-made route. Otherwise use the tested CLI
version. If no CLI is installed, the project's supported persistent install is:

```sh
uv tool install specify-cli --from 'git+https://github.com/github/spec-kit.git@v1.1.2'
```

Follow uv's PATH instructions and verify `specify --version`. Do not silently replace
another project's newer CLI. An isolated environment can hold the pinned CLI instead.
[Spec Kit installation](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/README.md),
[uv tool installation](https://docs.astral.sh/uv/guides/tools/).

If the installer Python lacks PyYAML, install it into an appropriate existing Python
environment or use a separate installation environment, rather than blindly modifying
an OS-managed Python. For example, after choosing a new directory:

```sh
SPECKIT_PRO_RUNTIME="$HOME/.local/share/speckit-pro/install-runtime"
uv venv --python 3.11 "$SPECKIT_PRO_RUNTIME"
uv pip install --python "$SPECKIT_PRO_RUNTIME/bin/python" pyyaml
# For the install command only:
# PATH="$SPECKIT_PRO_RUNTIME/bin:$PATH" "$SPECKIT_PRO_SOURCE/install.sh" ...
```

This command-scoped PATH avoids replacing the application's Python environment in
subsequent test commands. Keep the project's quality gates tied to its actual runtime.
The installed baseline checker itself uses the standard library; Spec Kit template
helpers may still need a PyYAML-capable interpreter. Their supported override is
`SPECKIT_PYTHON_EXECUTABLE`. [uv environment guide](https://docs.astral.sh/uv/pip/environments/),
[shipped helper implementation](../template/.specify/scripts/bash/common.sh).

In the scenario examples, replace these paths once:

```sh
SPECKIT_PRO_SOURCE="/absolute/path/to/the/reviewed/speckit-pro-checkout"
PROJECT_DIR="/absolute/path/to/target-project"
```

The target directory must already exist, and it must differ from the package's own
root. The installer selects its path as follows:

- No `.specify`, no `specify` executable, and no agent selection or `--agent codex`:
  copy the generated `.specify` and `.agents/skills` installation. This installs
  project files, not a CLI executable.
- No `.specify`, with a CLI available: initialize the selected integration, then add
  the preset, extension and workflow. Codex initialization explicitly uses skills mode.
- Existing `.specify`: use the CLI to add components without reinitializing the
  project. Keep its current agent; an `--agent` argument is ignored with a note.
- Existing speckit-pro: use `--force` for a reviewed update. Here `--force` means
  updating speckit-pro; it is not a recommendation to reinitialize existing Spec Kit.

`--with-cli` installs the pinned CLI using uv and `--force` at tool-manager level.
That is optional and affects the machine's persistent CLI. It does not install the
coding agent, authenticate it, or provision the application's runtime/services.
CLI-backed workflow execution also requires the selected agent's runtime.
[Installer](../install.sh).

## 1. New project: no implementation and no existing development tool

Create the target directory, then install for the intended agent:

```sh
mkdir -p "$PROJECT_DIR"
"$SPECKIT_PRO_SOURCE/install.sh" --agent codex "$PROJECT_DIR"
```

For Claude, use `--agent claude` with the CLI available. With no CLI, the Codex/default
route can copy the prepared installation; run individual agent skills until a CLI is
installed if you want `specify workflow run` later.

Open the coding agent in the project root and paste the installed
`.specify/speckit-pro/adoption-prompt.md` block. Its first steps inspect the repository,
establish Git if missing, create a sensible ignore policy and an initial commit, and
install hooks. Git initialization is not guaranteed by stock `specify init`: the pinned
CLI delegates Git workflows to an optional Git extension. A commit must exist before
using `--base HEAD`. [Pinned core behavior](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/docs/reference/core.md),
[adoption prompt](../adoption-prompt.md).

Configuration then proceeds from approved project intent:

1. Establish the constitution and applicable modules; leave unknown stack/platform
   choices unresolved rather than choosing them during adoption.
2. Run the agent's baseline amend command to propose product, architecture and
   decision entries for approval. Remove template sample rows/placeholders. Keep
   planned code parts even when their files do not exist yet.
3. Record the initial accepted comparison point from the project root:

   ```sh
   python3 .specify/extensions/baseline/scripts/baseline_check.py --write --stamp --base HEAD
   python3 .specify/extensions/baseline/scripts/baseline_check.py --gate --strict
   ```

4. Record adoption evidence in `docs/spec-kit-adoption.md`; report ADOPTED only when
   the profile's adoption checklist is satisfied. A passing baseline gate alone
   does not certify every adoption obligation.

The next action is specification of the first approved capability. Adoption does not
itself authorize inventing a feature or writing application implementation.
[Baseline amendment](../extension/commands/speckit.baseline.amend.md).

## 2. Existing implementation: no existing development tool

Inspect existing Git state, instructions, dependencies, source, tests, public contracts
and documents first. Record existing test results and failures. If there is no Git
history, establish a reviewed starting commit as the adoption prompt requires.

Install using the same chosen-agent command as scenario 1:

```sh
"$SPECKIT_PRO_SOURCE/install.sh" --agent codex "$PROJECT_DIR"
```

The difference is adoption. Run the baseline recover command rather than drafting
an ideal architecture from scratch. Its deterministic discovery steps are:

```sh
cd "$PROJECT_DIR"
python3 .specify/extensions/baseline/scripts/baseline_check.py --mode advisory
python3 .specify/extensions/baseline/scripts/baseline_check.py --scan
```

Inspect the scan's folders, root files and hidden folders. Derive proposed capabilities,
stack choices, parts and contracts from evidence. Distinguish implemented behavior
from approved intent. Record only decisions that existing material explains; ask
about significant unknowns or park them as open questions. Code existence does not
make a capability approved or verified.

After the user approves the proposed baseline, record the starting synchronization:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py --write --stamp --base HEAD --reason 'approved initial recovery'
```

Map tests, locks/build configuration, and any hidden deployment/CI code deliberately.
Use `**Verification inputs**: Tooling` or the applicable shared parts to invalidate
feature evidence when shared configuration changes. The initial stamp records
reconciliation; it does not establish successful application tests or feature DONE.

Once reconciliation is clean, switch modes and validate:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py --mode blocking
python3 .specify/extensions/baseline/scripts/baseline_check.py --gate --strict
```

Advisory mode is a recovery aid. Required gates still block, and invalid DONE evidence
is never accepted. If baseline adoption is declined, the shipped required workflow/CI
is not ready to run; document partial adoption. Continue feature work from its actual
phase, or use the fix/small-change path for approved behavior-preserving work.
[Recovery contract](../extension/commands/speckit.baseline.recover.md),
[phase-entry rules](../speckit-universal-profile.md#12-start-from-the-phase-that-exists).

## 3. New project: no implementation, already using Spec Kit

Inspect the existing integration, constitution, templates, custom commands, other
presets/extensions, workflow and any feature already being specified or planned.
Use the CLI to add speckit-pro without selecting another agent:

```sh
cd "$PROJECT_DIR"
specify integration status
"$SPECKIT_PRO_SOURCE/install.sh" "$PROJECT_DIR"
```

Do not manually copy the entire ready-made `.specify` or agent folder over this project.
Do not run `specify init --here --force` merely to add speckit-pro. The installer already
uses supported preset/extension/workflow operations and retains the integration.
The new preset intentionally changes the governed Spec Kit command/template behavior;
review that composition alongside existing presets and customizations.
[Preset system](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/docs/reference/presets.md),
[integration management](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/docs/reference/integrations.md).

Paste the adoption prompt. Amend the existing constitution in place, preserving
ratification/history and settled decisions. Create or amend the approved baseline,
then use the initial `--write --stamp --base HEAD` from scenario 1 only if establishing
its first accepted comparison point. Keep an existing accepted base and synchronization
records; review and reconcile changes rather than resetting them during installation.
Run the required gate. Preserve any existing requirement/task IDs and planning artifacts.

If a feature is already specified, planned or tasked, enter there after repairing its
missing prerequisites. Do not start the full workflow from specify again simply
because speckit-pro was installed. If no feature exists, start the first approved one.

## 4. Existing implementation: already using Spec Kit

Inspect both tool configuration and current feature evidence. Install as an additive
Spec Kit integration:

```sh
cd "$PROJECT_DIR"
specify integration status
"$SPECKIT_PRO_SOURCE/install.sh" "$PROJECT_DIR"
```

Use `--force` only when speckit-pro itself is already installed and needs updating.
Then adopt/reconcile as in scenario 2, retaining existing approved baseline entries
when present. Recovery augments missing facts; it does not replace valid governance
with whatever the current code happens to do.

For active features, preserve folders, FR/AS/TR/task IDs, checked history, accepted
choices and historical logs. Review and add missing baseline citation lines and
verification mappings. After actually reviewing each feature's spec and plan:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py --write --feature specs/007-cart --repin specs/007-cart/spec.md
python3 .specify/extensions/baseline/scripts/baseline_check.py --write --feature specs/007-cart --repin specs/007-cart/plan.md
```

Replace the example folder. Changed existing pins require `--reason`; changed specs
also require downstream plan/tasks review and explicit acknowledgment. The checker
can save valid targeted pins while other features still report migration gaps.

Historical Markdown DONE is preserved as history, not automatically accepted as v3
current verification. Renew evidence with the final-input run below before claiming
current DONE. For claimed-complete features, analyze and converge first; append
remediation rather than blindly restarting specify. Migrate accepted predecessors
on their original promise before amending a capability and creating a Changes spec.
[Evidence/migration contract](../extension/commands/speckit.baseline.check.md),
[audit migration notes](followup-audit-response.md#migration-and-practical-limits).

The next step follows the real phase: planning, tasks, implementation, missing
verification, or convergence. Superseded features remain historical.

## Integrating and using the configured installation

Confirm both registrations and operative contents:

```sh
specify integration status
specify preset list
specify extension list
specify workflow list
specify workflow info speckit-pro
```

Look for preset `universal-profile`, extension `baseline`, workflow `speckit-pro`,
seven governed core commands, convergence, and six baseline commands. Agent invocation
names differ: the generated Codex skill is named `speckit-baseline-recover`, while
its logical command ID is `speckit.baseline.recover`. Use the installed SKILL.md or
command file; do not invent one universal slash syntax. For no-CLI installations,
inspect the corresponding registries/files directly. [Integration reference](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/docs/reference/integrations.md).

Keep project-specific instructions in the project's existing AGENTS.md, CLAUDE.md
or equivalent. Reference `.specify/speckit-pro/speckit-universal-profile.md`, applicable
modules, exact quality-gate commands, their working directories and the evidence policy.
Edit project guidance rather than generated command files that upgrades replace.

With the native Git extension, baseline before_specify is configured at priority 1
and Git feature creation at default priority 10. The pinned HookExecutor sorts enabled
hooks by priority. Its registration file retains insertion order, and generated agent
prompts tell agents to iterate hooks without explicitly specifying a priority sort.
For direct agent execution, instruct the agent to sort enabled hooks by ascending
priority before invoking them and verify intake precedes branch creation. Configuration
priority alone is not evidence that every agent session honored it. This remains a
manual integration consideration, not an agent-runtime behavior tested by the probes.
[Registered hooks](../extension/extension.yml),
[pinned hook executor](https://github.com/github/spec-kit/blob/v1.1.2/src/specify_cli/extensions/__init__.py),
[generated agent instructions](../template/.agents/skills/speckit-specify/SKILL.md).

For a new approved feature, the CLI workflow invocation is:

```sh
specify workflow run speckit-pro --input 'spec=Implement the approved CAP-001 feature'
```

It runs specify, clarify, review gates, plan, tasks, analyze, implementation and
convergence, with independent baseline gates before implementation and after completion.
It is linear: handle tasks_appended/gaps_remaining by returning to implementation,
verification and convergence; do not assume the shipped workflow automatically loops.
Use `specify workflow status` / `resume <run_id>` for run management, not to pretend
an earlier-phase feature has completed. [Workflow CLI](https://raw.githubusercontent.com/github/spec-kit/v1.1.2/docs/reference/workflows.md),
[shipped workflow](../workflow/workflow.yml).

On final feature inputs, use the installed verifier:

```sh
python3 .specify/extensions/baseline/scripts/baseline_check.py --record-run --feature specs/001-feature
# Complete verification.md from verification-run.json and its actual logs;
# complete convergence and only then claim supported Completion: DONE.
python3 .specify/extensions/baseline/scripts/baseline_check.py --write --feature specs/001-feature --stamp specs/001-feature
python3 .specify/extensions/baseline/scripts/baseline_check.py --gate --require-done --feature specs/001-feature
python3 .specify/extensions/baseline/scripts/baseline_check.py --status --json
```

Every planned required gate must succeed. Changed tested inputs need a new run;
cosmetic report edits, skip explanations and stamps cannot renew evidence. Explicit
feature folders avoid ambiguity; `--feature current` reads `.specify/feature.json`.
The baseline extension expects features inside this project's specs tree, even though
stock Spec Kit offers external feature-directory overrides.

For CI, merge `.specify/extensions/baseline/ci/baseline.yml` into the project's existing
workflow setup. Provision its locked runtime/dependencies/services before executable
rules. Keep full Git history, supply the PR base and run the global `--gate --strict`.
Configure repository settings to require that job. Installing YAML or local hooks does
not configure branch protection. The job validates recorded input freshness and rules;
run the application's quality gates in CI as well. [CI scaffold](../extension/ci/baseline.yml).

## When the existing development tool is not Spec Kit

There is no generic automatic adapter in install.sh. An unrelated tool's presence
must not be mistaken for a supported Spec Kit installation.

Choose an explicit integration approach:

- Coexist with Spec Kit: treat installation as scenario 1 or 2, retain the other tool,
  and agree which system owns requirements, plans, tasks and verification. Add explicit
  handoffs to the existing workflow rather than generating two competing task histories.
- Port the profile manually: map constitution/governance, requirements, design, tasks,
  analysis, verification and convergence onto the tool's actual artifacts. This can adopt
  the governance rules, but does not automatically provide the Spec Kit extension's
  mechanical guarantees.

To retain the baseline checker, provide its actual schema: `.specify/memory/` baseline
files, feature spec.md/plan.md/tasks.md/verification.md under specs/, citations, pins,
run records and an explicit gate invocation. If the other tool already stores those
facts elsewhere, a deliberate adapter is needed. Merely renaming files or using the
Spec Kit generic agent integration does not supply that adapter. The preset itself
also does not automatically reach the generic integration.
[Installer](../install.sh), [checker](../extension/scripts/baseline_check.py),
[integration limits](../speckit-universal-profile.md#59-speckit-converge).

## Research validation

Four fresh disposable repositories were tested with the real pinned CLI. The two
existing-tool cases used Claude plus the real bundled Git extension; the no-tool cases
selected Codex. All four installations and configured global required baseline gates
passed. Existing implementation files/tests, constitution, custom skill and feature
IDs/checked tasks were preserved where present; existing integration metadata remained
unchanged. Git priority 10 and baseline priority 1 both remained registered.

The two implementation fixtures each passed one small unittest of their synthetic
cart behavior. These are fixture checks, not verification of a user's application.
The probes supplied synthetic approved baseline data to exercise configuration;
they do not establish completed semantic governance adoption. Interactive agent
execution, authentication, branch-hook execution order and unrelated development-tool
adapters were not tested. Earlier installer regression tests separately cover the
no-CLI ready-made route and failed updates.

Local probe details are in `tmp/speckit-pro-four-scenarios-results.json`; tmp is ignored
and not a distributable source. Operative contracts live in the linked repository files.
The research adds this guide only; it does not adopt speckit-pro into a user application.
