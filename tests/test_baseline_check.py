"""Regression tests for extension/scripts/baseline_check.py.

Each test builds a small git repository in a temporary folder and runs the
script against it. Run with: python3 -m unittest discover -s tests
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "extension" / "scripts" / "baseline_check.py"

PRODUCT = """# Product: Shop

**Version**: 1.0.0 | **Last amended**: 2026-10-09

## Purpose and users

A small shop for returning customers.

## Product rules

| ID | Rule |
|----|------|
| PR-001 | Prices include tax. |

## Capabilities

| ID | Promise | Decision | Depends on | Owning spec | Delivery |
|----|---------|----------|------------|-------------|----------|
| CAP-001 | Customers can log in. | approved | - | - | unstarted |
| CAP-002 | Customers can pay. | approved | - | - | unstarted |

## Open questions

| ID | Question | Blocks | Raised | Status |
|----|----------|--------|--------|--------|
"""

ARCHITECTURE = """# Architecture: Shop

**Version**: 1.0.0 | **Last amended**: 2026-10-09

## Stack

| Area | Choice | Decision |
|------|--------|----------|
| Language | Python | D-001 |

## Parts and boundaries

| Part | Owns | Paths | May depend on | State |
|------|------|-------|---------------|-------|
| App | Requests | src, main.py | - | built |

## Architecture rules

| ID | Rule | Blocking | Check |
|----|------|----------|-------|
| AR-001 | No print statements. | yes | - |

## Interfaces and contracts

- The HTTP API is described in the plan of each feature.
"""

DECISIONS = """# Decisions: Shop

| ID | Date | Question | Decision | Rejected options | Affects | Status |
|----|------|----------|----------|------------------|---------|--------|
| D-001 | 2026-10-09 | Which language? | Python, the team knows it. | Go | App | accepted |
| D-002 | 2026-10-09 | Guest checkout? | No guest checkout. | Guest checkout | - | accepted |
| D-003 | 2026-10-09 | Which database? | MongoDB | - | App | rejected |
"""

SPEC = """# Feature Specification: Login

**Implements**: CAP-001
**Product rules**: PR-001
**Baseline**: abc1234

- **FR-001**: Login works.
- AS-001: Given a user, when they log in, then they see the shop.
- TR-001: The login request returns the session.
"""

PLAN = """# Implementation Plan: Login

**Architecture impact**: none
**Architecture rules**: AR-001
**Decisions**: D-001
**Parts**: App
"""

VERIFICATION = """# Verification: Login

Completion: DONE
Tested revision / relevant working-tree fingerprint: abc1234 clean

## Coverage

FRs with meaningful assertions: 1/1
Required TRs passing: 1/1

| FR / AS | TR | Executable selector or observation | Status | Evidence / tested state |
|---------|----|-------------------------------------|--------|-------------------------|
| FR-001 / AS-001 | TR-001 | tests/test_login.py::test_login | PASS | abc1234 |

## Execution

| Working directory | Exact command | Exit code | Passed / failed / skipped / xfailed | Evidence |
|-------------------|---------------|-----------|------------------------------------|----------|
| . | pytest | 0 | 1 / 0 / 0 / 0 | run of 2026-10-09 |

## Convergence

Outcome: converged

## Historical runs

| Run | Status |
|-----|--------|
| first attempt | FAIL |
"""


class Repo:
    def __init__(self, folder: str) -> None:
        self.root = Path(folder).resolve()
        self.memory = self.root / ".specify" / "memory"
        self.write(".specify/memory/product.md", PRODUCT)
        self.write(".specify/memory/architecture.md", ARCHITECTURE)
        self.write(".specify/memory/decisions.md", DECISIONS)
        self.write("src/app.py", "x = 1\n")
        self.write("main.py", "import src\n")
        self.git("init", "-q")
        self.commit("start")

    def write(self, name: str, text: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read(self, name: str) -> str:
        return (self.root / name).read_text(encoding="utf-8")

    def edit(self, name: str, old: str, new: str) -> None:
        text = self.read(name)
        assert old in text, f"{old!r} not in {name}"
        self.write(name, text.replace(old, new))

    def git(self, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(self.root), "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
            check=True, capture_output=True,
        )

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)

    def check(self, *args: str) -> tuple[int, str]:
        done = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args], capture_output=True, text=True, check=False
        )
        return done.returncode, done.stdout + done.stderr

    def feature(self, key: str = "001-login", spec: str = SPEC, plan: str = PLAN, verification: str | None = None,
                tasks: str | None = "- [x] T001 Build login\n") -> None:
        self.write(f"specs/{key}/spec.md", spec)
        if plan is not None:
            self.write(f"specs/{key}/plan.md", plan)
        if tasks is not None:
            self.write(f"specs/{key}/tasks.md", tasks)
        if verification is not None:
            self.write(f"specs/{key}/verification.md", verification)

    def delivery(self, ident: str) -> str:
        row = next(line for line in self.read(".specify/memory/product.md").splitlines() if line.startswith(f"| {ident} "))
        return row.strip("|").split("|")[-1].strip()


class BaselineCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.repo = Repo(self.folder.name)

    def started(self, fresh: bool = False) -> Repo:
        """A feature that went through specify and plan, with its pins recorded."""
        repo = Repo(tempfile.mkdtemp(dir=self.folder.name)) if fresh else self.repo
        repo.feature()
        code, out = repo.check("--write", "--repin", "specs/001-login")
        self.assertEqual(code, 0, out)
        return repo

    def verified(self) -> Repo:
        repo = self.started()
        repo.write("specs/001-login/verification.md", VERIFICATION)
        code, out = repo.check("--write", "--stamp", "specs/001-login")
        self.assertEqual(code, 0, out)
        self.assertEqual(repo.delivery("CAP-001"), "verified")
        return repo

    # The normal path

    def test_no_baseline_is_not_an_error(self):
        (self.repo.memory / "product.md").unlink()
        code, out = self.repo.check("--run-rule-checks")
        self.assertEqual(code, 0, out)
        self.assertIn("no baseline to check", out)

    def test_new_feature_passes_in_one_run_and_records_its_owner(self):
        repo = self.started()
        self.assertIn("| specs/001-login | in progress |", repo.read(".specify/memory/product.md"))
        self.assertEqual(repo.check("--strict")[0], 0)

    def test_supported_done_becomes_verified(self):
        self.verified()

    # Completion needs evidence

    def test_two_line_done_is_rejected(self):
        repo = self.repo
        repo.feature(plan=None, tasks=None, verification="Completion: DONE\nOutcome: converged\n")
        code, out = repo.check("--strict", "--write")
        self.assertEqual(code, 1, out)
        self.assertIn("plan.md is missing", out)
        self.assertIn("the Coverage section has no rows", out)
        self.assertEqual(repo.delivery("CAP-001"), "unstarted")

    def test_failing_exit_code_is_rejected(self):
        repo = self.started()
        repo.write("specs/001-login/verification.md", VERIFICATION.replace("| pytest | 0 | 1 / 0 / 0 / 0 |", "| pytest | 1 | 0 passed, 1 failed |"))
        code, out = repo.check("--write")
        self.assertEqual(code, 1, out)
        self.assertIn("exit code '1'", out)
        self.assertIn("reports failures", out)

    def test_unknown_and_skipped_statuses_are_rejected(self):
        for status in ("FAILED", "SKIPPED", "OK"):
            with self.subTest(status=status):
                repo = self.started(fresh=True)
                repo.write("specs/001-login/verification.md", VERIFICATION.replace("| PASS |", f"| {status} |"))
                code, out = repo.check()
                self.assertEqual(code, 1, out)
                self.assertIn(f"unknown status '{status}'", out)

    def test_every_spec_id_needs_a_passing_row(self):
        repo = self.started()
        repo.edit("specs/001-login/spec.md", "- TR-001", "- **FR-002**: Logout works.\n- TR-001")
        repo.write("specs/001-login/verification.md", VERIFICATION)
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("FR-002", out)

    def test_unchecked_task_missing_link_and_placeholder_are_rejected(self):
        repo = self.started()
        repo.write("specs/001-login/tasks.md", "- [x] T001 a\n- [ ] T002 b\n")
        repo.write("specs/001-login/verification.md", VERIFICATION.replace("run of 2026-10-09", "[log](evidence/missing.log) <path>"))
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("1 unchecked task(s)", out)
        self.assertIn("evidence link does not resolve", out)
        self.assertIn("unfilled <placeholders>", out)

    def test_spec_changed_after_verification_needs_a_new_run(self):
        repo = self.verified()
        repo.edit("specs/001-login/spec.md", "Login works.", "Login works with a passkey.")
        code, out = repo.check("--strict")
        self.assertEqual(code, 1, out)
        self.assertIn("changed after the feature was verified", out)

    def test_capability_changed_after_verification_is_reported(self):
        repo = self.verified()
        repo.edit(".specify/memory/product.md", "Customers can log in.", "Customers can log in with MFA.")
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("CAP-001 changed after this feature was verified", out)

    # Writes are transactional in blocking mode

    def test_failed_check_writes_nothing(self):
        repo = self.repo
        repo.edit(".specify/memory/product.md", "| CAP-001 | Customers can log in. | approved", "| CAP-001 | Customers can log in. | proposed")
        repo.feature(verification=VERIFICATION)
        before = repo.read(".specify/memory/product.md")
        code, out = repo.check("--write", "--repin", "--stamp")
        self.assertEqual(code, 1, out)
        self.assertIn("nothing was written", out)
        self.assertEqual(repo.read(".specify/memory/product.md"), before)
        self.assertFalse((repo.memory / "baseline-state.json").exists())
        self.assertFalse((repo.root / "specs/001-login/baseline-pins.json").exists())

    def test_advisory_mode_reports_and_exits_zero(self):
        repo = self.repo
        repo.feature(spec=SPEC.replace("CAP-001", "CAP-999"))
        code, out = repo.check("--mode", "advisory")
        self.assertEqual(code, 0, out)
        self.assertIn("error: specs/001-login/spec.md: cites CAP-999", out)
        self.assertEqual(repo.check()[0], 0)
        self.assertEqual(repo.check("--mode", "blocking")[0], 1)

    def test_corrupt_state_is_an_error(self):
        repo = self.started()
        repo.write("specs/001-login/baseline-pins.json", "{not json")
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("not valid JSON", out)

    # Citations and pins

    def test_ids_in_prose_are_not_citations(self):
        repo = self.repo
        repo.feature(spec=SPEC + "\nSee PR-123 on the forge. Not MongoDB (rejected in D-003).\n")
        code, out = repo.check("--write", "--repin", "specs/001-login")
        self.assertEqual(code, 0, out)

    def test_repin_accepts_every_form_of_path(self):
        for form in ("001-login", "specs/001-login", "specs/001-login/", "ABSOLUTE", "specs/001-login/spec.md"):
            with self.subTest(form=form):
                repo = Repo(tempfile.mkdtemp(dir=self.folder.name))
                repo.feature()
                target = str(repo.root / "specs" / "001-login") if form == "ABSOLUTE" else form
                code, out = repo.check("--write", "--repin", target)
                self.assertEqual(code, 0, out)
                pins = json.loads(repo.read("specs/001-login/baseline-pins.json"))["pins"]
                self.assertIn("CAP-001", pins["spec.md"])

    def test_repin_of_an_unknown_spec_is_an_error(self):
        code, out = self.repo.check("--repin", "specs/404-missing")
        self.assertEqual(code, 1, out)

    def test_unpinned_citation_fails_strict(self):
        self.repo.feature()
        code, out = self.repo.check("--strict")
        self.assertEqual(code, 1, out)
        self.assertIn("is not pinned", out)

    def test_repinning_the_plan_does_not_clear_a_stale_spec(self):
        repo = self.started()
        repo.edit(".specify/memory/product.md", "Customers can log in.", "Customers can log in with MFA.")
        self.assertEqual(repo.check()[0], 1)
        code, out = repo.check("--repin", "specs/001-login/plan.md")
        self.assertEqual(code, 1, out)
        self.assertIn("CAP-001 changed in the baseline", out)

    def test_stack_and_part_changes_make_the_plan_stale(self):
        for old, new in (("| Language | Python |", "| Language | Go |"), ("| App | Requests |", "| App | Everything |")):
            with self.subTest(change=new):
                repo = Repo(tempfile.mkdtemp(dir=self.folder.name))
                repo.feature()
                self.assertEqual(repo.check("--write", "--repin", "specs/001-login")[0], 0)
                repo.edit(".specify/memory/architecture.md", old, new)
                code, out = repo.check()
                self.assertEqual(code, 1, out)
                self.assertIn("changed in the baseline", out)

    # Capabilities

    def test_open_question_blocks_its_capability(self):
        repo = self.repo
        repo.edit(".specify/memory/product.md", "|----|----------|--------|--------|--------|\n",
                  "|----|----------|--------|--------|--------|\n| Q-001 | Guest login? | CAP-001 | 2026-10-09 | open |\n")
        repo.feature()
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("blocked by open question Q-001", out)

    def test_a_later_spec_changes_a_capability(self):
        repo = self.verified()
        repo.feature("002-login-mfa", spec=SPEC.replace("**Implements**", "**Changes**"))
        code, out = repo.check("--write", "--repin", "specs/002-login-mfa")
        self.assertEqual(code, 0, out)
        self.assertEqual(repo.delivery("CAP-001"), "in progress")
        self.assertIn("| specs/001-login |", repo.read(".specify/memory/product.md"))

    def test_two_specs_cannot_implement_one_capability(self):
        repo = self.started()
        repo.feature("002-again")
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("later spec lists it under `**Changes**:`", out)

    def test_retired_capability_keeps_its_finished_spec_valid(self):
        repo = self.verified()
        repo.edit(".specify/memory/product.md", "| CAP-001 | Customers can log in. | approved", "| CAP-001 | Customers can log in. | retired")
        code, out = repo.check()
        self.assertEqual(code, 0, out)

    def test_dependency_cycle_is_an_error(self):
        repo = self.repo
        repo.edit(".specify/memory/product.md", "| CAP-001 | Customers can log in. | approved | - |", "| CAP-001 | Customers can log in. | approved | CAP-002 |")
        repo.edit(".specify/memory/product.md", "| CAP-002 | Customers can pay. | approved | - |", "| CAP-002 | Customers can pay. | approved | CAP-001 |")
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("through a cycle", out)

    def test_deleted_row_is_an_error_and_rewritten_decision_a_warning(self):
        repo = self.repo
        text = repo.read(".specify/memory/decisions.md")
        repo.write(".specify/memory/decisions.md", "\n".join(
            line.replace("No guest checkout.", "Guest checkout allowed.") for line in text.splitlines() if "D-003" not in line
        ) + "\n")
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("D-003 was deleted", out)
        self.assertIn("D-002 was rewritten", out)

    def test_nested_spec_folders_are_checked(self):
        self.repo.feature("payments/002-pay", spec=SPEC.replace("CAP-001", "CAP-999"))
        code, out = self.repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("specs/payments/002-pay/spec.md: cites CAP-999", out)

    # Code against the map

    def test_planned_part_does_not_block_and_becomes_built(self):
        repo = self.repo
        repo.edit(".specify/memory/architecture.md", "| App | Requests | src, main.py | - | built |",
                  "| App | Requests | src, main.py | - | built |\n| Worker | Jobs | worker | App | planned |")
        code, out = repo.check("--run-rule-checks")
        self.assertEqual(code, 0, out)
        repo.write("worker/jobs.py", "y = 1\n")
        code, out = repo.check("--write")
        self.assertEqual(code, 0, out)
        self.assertIn("| Worker | Jobs | worker | App | built |", repo.read(".specify/memory/architecture.md"))
        (repo.root / "worker/jobs.py").unlink()
        code, out = repo.check()
        self.assertEqual(code, 1, out)
        self.assertIn("match no file any more", out)

    def test_escaped_pipe_runs_the_whole_command(self):
        repo = self.repo
        repo.edit(".specify/memory/architecture.md", "| AR-001 | No print statements. | yes | - |",
                  "| AR-001 | No print statements. | yes | `printf pass \\| grep absent` |")
        code, out = repo.check("--run-rule-checks")
        self.assertEqual(code, 1, out)
        self.assertIn("AR-001 check failed (`printf pass | grep absent`)", out)

    def test_drift_is_reported_per_part_and_includes_root_files(self):
        repo = self.verified()
        repo.commit("verified")
        self.assertEqual(repo.check("--strict")[0], 0)
        repo.write("main.py", "import src\nprint('changed')\n")
        code, out = repo.check()
        self.assertIn("part 'App' changed since its synced point", out)
        repo.write("tool.py", "z = 1\n")
        self.assertIn("`tool.py` is tracked code that no part maps", repo.check()[1])

    def test_unfinished_feature_only_covers_the_parts_it_lists(self):
        repo = self.verified()
        repo.edit(".specify/memory/architecture.md", "| App | Requests | src, main.py | - | built |",
                  "| App | Requests | src, main.py | - | built |\n| Worker | Jobs | worker | App | planned |")
        repo.write("worker/jobs.py", "y = 1\n")
        self.assertEqual(repo.check("--write", "--stamp")[0], 0)
        repo.feature("002-pay", spec=SPEC.replace("CAP-001", "CAP-002"), plan=PLAN.replace("**Parts**: App", "**Parts**: Worker"))
        self.assertEqual(repo.check("--write", "--repin", "specs/002-pay")[0], 0)
        repo.write("worker/jobs.py", "y = 2\n")
        self.assertNotIn("changed since its synced point", repo.check()[1])
        repo.write("src/app.py", "x = 2\n")
        self.assertIn("part 'App' changed since its synced point", repo.check()[1])

    def test_synced_point_survives_a_rewritten_commit(self):
        repo = self.verified()
        repo.commit("verified")
        repo.git("commit", "-q", "--amend", "-m", "squashed")
        code, out = repo.check("--strict")
        self.assertEqual(code, 0, out)

    # No agent as a contributor

    def hook(self, message: str, **env: str) -> tuple[int, str]:
        import os
        path = self.repo.write("COMMIT_MSG", message)
        done = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.repo.root), "--commit-msg", str(path)],
            capture_output=True, text=True, check=False, cwd=self.repo.root,
            env={**os.environ, "GIT_AUTHOR_NAME": "Jane Roe", "GIT_AUTHOR_EMAIL": "jane@example.com",
                 "GIT_COMMITTER_NAME": "Jane Roe", "GIT_COMMITTER_EMAIL": "jane@example.com", **env},
        )
        return done.returncode, done.stdout + done.stderr

    def test_commit_message_naming_an_agent_is_rejected(self):
        for line in (
            "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>",
            "Co-authored-by: Copilot <175728472+Copilot@users.noreply.github.com>",
            "Co-authored-by: aider (gpt-4o) <aider@aider.chat>",
            "\U0001F916 Generated with [Claude Code](https://claude.com/claude-code)",
            "Generated by Codex",
        ):
            with self.subTest(line=line):
                code, out = self.hook(f"feat: add login\n\n{line}\n")
                self.assertEqual(code, 1, out)
                self.assertIn("names a coding agent as a contributor", out)

    def test_human_contributors_and_ordinary_wording_pass(self):
        for line in (
            "Co-Authored-By: Claude Dupont <claude.dupont@example.fr>",
            "Co-authored-by: Jane Roe <jane@anthropic.com>",
            "The table is generated by the build script.",
            "# Co-Authored-By: Claude <noreply@anthropic.com>",
        ):
            with self.subTest(line=line):
                self.assertEqual(self.hook(f"fix: cursor position\n\n{line}\n")[0], 0)

    def test_agent_as_author_is_rejected(self):
        code, out = self.hook("feat: add login\n", GIT_AUTHOR_NAME="Claude", GIT_AUTHOR_EMAIL="noreply@anthropic.com")
        self.assertEqual(code, 1, out)
        self.assertIn("the author is", out)

    def test_installed_hook_blocks_the_commit_and_the_check_reports_one_that_got_past(self):
        repo = self.repo
        ext = repo.root / ".specify/extensions/baseline/scripts"
        ext.mkdir(parents=True)
        (ext / "baseline_check.py").write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
        installer = SCRIPT.parent / "install-git-hooks.sh"
        subprocess.run(["sh", str(installer)], cwd=repo.root, check=True, capture_output=True)
        subprocess.run(["sh", str(installer)], cwd=repo.root, check=True, capture_output=True)  # safe to repeat
        repo.write("src/app.py", "x = 3\n")
        repo.git("add", "-A")
        with self.assertRaises(subprocess.CalledProcessError):
            repo.git("commit", "-q", "-m", "feat: x\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
        repo.git("commit", "-q", "-m", "feat: x")
        self.assertNotIn("names a coding agent", repo.check()[1])
        repo.git("commit", "-q", "--allow-empty", "--no-verify", "-m", "feat: y\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
        self.assertIn("names a coding agent as a contributor", repo.check()[1])

    # Context

    def test_context_carries_what_specify_and_plan_need(self):
        repo = self.repo
        repo.edit(".specify/memory/product.md", "|----|----------|--------|--------|--------|\n",
                  "|----|----------|--------|--------|--------|\n| Q-001 | Guest login? | CAP-001 | 2026-10-09 | open |\n")
        code, out = repo.check("--context", "--ids", "CAP-001")
        self.assertEqual(code, 0, out)
        for expected in ("A small shop", "PR-001", "D-002", "Q-001", "product 1.0.0"):
            self.assertIn(expected, out)
        code, out = repo.check("--context", "--paths", "src")
        for expected in ("| Language | Python |", "**Parts**: App", "AR-001", "D-001", "D-003", "The HTTP API"):
            self.assertIn(expected, out)


if __name__ == "__main__":
    unittest.main()
