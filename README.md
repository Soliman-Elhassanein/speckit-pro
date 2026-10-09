# speckit-pro

A complete [Spec Kit](https://github.com/github/spec-kit) setup with a stricter standard on top: every project keeps its rules, its product, its architecture and its decisions in files, and a script rejects a "done" that the project's own records do not support.

## Install into a project

One command, from any machine with Git:

```sh
git clone https://github.com/Soliman-Elhassanein/speckit-pro ~/.speckit-pro && ~/.speckit-pro/install.sh /path/to/project
```

Then open your coding agent in the project and paste the block from `.specify/speckit-pro/adoption-prompt.md`.

What the installer does depends on the project:

| Project | What happens | Needs the Spec Kit CLI |
|---|---|---|
| No Spec Kit yet, agent reads `.agents/skills` (Codex and others) | Copies a ready-made installation | No |
| No Spec Kit yet, another agent (`--agent claude`, `copilot`, `cursor`, `gemini`, ...) | Initializes Spec Kit for that agent, then adds speckit-pro | Yes |
| Already has Spec Kit | Adds speckit-pro through the CLI. The project keeps its agent, hooks, other extensions and settings | Yes |

Options:

| Option | Effect |
|---|---|
| `--agent NAME` | The coding agent the project uses, as Spec Kit names it. |
| `--force` | Update a project where speckit-pro is already installed. |
| `--with-cli` | Install the pinned Spec Kit CLI with `uv` first. |

Specs, code, `constitution.md` and the baseline files are never overwritten. The installed commands need `git`, `bash`, `python3` and the Python package PyYAML; on Windows that means WSL.

To update a machine later: `git -C ~/.speckit-pro pull`, then `install.sh --force` in each project.

## What a project gets

| Path in the project | What it is |
|---|---|
| The agent's command folder (`.agents/skills`, `.claude/skills`, ...) | The ten Spec Kit commands, seven of them carrying the standard's rules, plus six baseline commands |
| `.specify/` | Spec Kit's scripts, templates and hooks, the standard's template sections, and the `speckit-pro` workflow |
| `.specify/extensions/baseline/` | Templates and the check script for the project baseline, and a sample CI workflow |
| `.specify/speckit-pro/` | The standard, its optional modules and the adoption prompt |

## How it works

Project memory, one home per kind of fact:

```
.specify/memory/
  constitution.md   rules   how we work
  product.md        what    one row per capability, with its state
  architecture.md   how     stack, parts, boundaries, rules
  decisions.md      why     one row per decision, never deleted
specs/NNN/          one change, with its proof
```

Four laws:

1. **One home per fact.** Everything else links to it.
2. **Calculate, do not maintain.** A script derives each capability's owner and delivery status and each part's state, and checks IDs, pins and code drift.
3. **The agent proposes; you approve.** Only one command edits what the baseline means, and only after you approve the exact rows.
4. **Process weight follows change size.** A new feature, a change to an existing one, a bug fix and a small change take different paths.

The full rules are in [speckit-universal-profile.md](speckit-universal-profile.md).

### What is checked by a script, and what is not

The check script is deterministic: plain Python and git, no AI. It rejects `Completion: DONE` unless the feature's records hold together: every requirement ID in the spec has a passing coverage row, every recorded command exited with 0, every task is checked, the evidence links resolve, and convergence was reached. It also catches stale citations, code that changed outside a feature, and deleted history.

It judges structure, not meaning. It cannot tell whether a test asserts the right thing, or whether a recorded run really happened. That judgment stays with the analyze and converge commands, which are instructions an agent follows, and with your review. Treat `verified` as "the record is complete and consistent", not as proof.

A project that adopts the baseline with code already written starts in advisory mode: the check reports and does not stop work. To run it in CI, copy `.specify/extensions/baseline/ci/baseline.yml` into `.github/workflows/`.

## What is in this repository

| Path | What it is |
|---|---|
| [speckit-universal-profile.md](speckit-universal-profile.md) | The standard |
| [modules/](modules/) | Optional rule sets for specific kinds of product |
| [preset/](preset/) | The standard's command rules and template sections, as a Spec Kit preset |
| [extension/](extension/) | The project baseline, as a Spec Kit extension |
| [workflow/](workflow/) | The full cycle with review gates and a check step, as a Spec Kit workflow |
| [tests/](tests/) | Regression tests of the check script |
| [template/](template/) | The ready-made installation that `install.sh` copies. Generated; do not edit by hand. |
| [install.sh](install.sh) | The installer |
| [scripts/build-template.sh](scripts/build-template.sh) | Rebuilds `template/` from the pinned Spec Kit release |
| [adoption-prompt.md](adoption-prompt.md) | The prompt that makes an agent adopt the standard |

## Maintaining it

Run the tests after changing the check script:

```sh
python3 -m unittest discover -s tests
```

After changing `preset/`, `extension/` or `workflow/`, or to move to a newer Spec Kit release (edit the [SPECKIT_VERSION](SPECKIT_VERSION) file first, and add a row to the table below):

```sh
sh scripts/build-template.sh
```

CI runs the tests and fails when `template/` no longer matches its sources.

[SPECKIT_VERSION](SPECKIT_VERSION) holds the Spec Kit release this project was last built and tested with. The build script refuses to run with any other version, and `install.sh` copies the number into each project.

| Spec Kit release | Used from | Notes |
|---|---|---|
| 1.1.2 | 2026-10-09 | Current. Preset, extension, workflow and installer verified with the Codex (skills) and Claude layouts. |
| 0.13.3.dev0 | 2026-10-08 | First version of the standard and the converge preset. |

## Known limits

- The commands are instructions to an agent. Only the check script, the workflow's check step and CI enforce anything on their own.
- Verification evidence is tied to the spec and plan it was recorded for, not to a fingerprint of the code.
- There is no release, rollback or production-feedback stage: completion is local by design.
- Feature folders must live under `specs/`.

## Credits

`template/` contains files generated by GitHub Spec Kit, which is MIT licensed. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
