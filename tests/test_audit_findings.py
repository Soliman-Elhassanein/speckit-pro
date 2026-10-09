"""Failing tests for the audit findings. Each one passes once its finding is fixed.

Put this file next to tests/test_baseline_check.py; it reuses that file's Repo fixture.
Run with: python3 -m unittest discover -s tests
"""

import json
import subprocess
import tempfile
import unittest

from test_baseline_check import SPEC, VERIFICATION, Repo

SPEC_PAY = SPEC.replace("**Implements**: CAP-001", "**Implements**: CAP-002").replace("Login", "Pay")
SPEC_CHANGES_LOGIN = SPEC.replace("**Implements**: CAP-001", "**Changes**: CAP-001").replace("Login", "Passkeys")


class AuditFindings(unittest.TestCase):
    # The same fixtures as BaselineCheckTest, without inheriting its tests.
    def setUp(self) -> None:
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.repo = Repo(self.folder.name)

    def started(self) -> Repo:
        repo = self.repo
        repo.feature()
        code, out = repo.check("--write", "--repin", "specs/001-login")
        self.assertEqual(code, 0, out)
        return repo

    def verified(self) -> Repo:
        repo = self.started()
        self.assertEqual(repo.check("--record-run", "--feature", "specs/001-login")[0], 0)
        repo.write("specs/001-login/evidence/run.log", "fixture observation\n")
        repo.write("specs/001-login/verification.md", VERIFICATION)
        code, out = repo.check("--write", "--stamp", "specs/001-login")
        self.assertEqual(code, 0, out)
        self.assertEqual(repo.delivery("CAP-001"), "verified")
        return repo

    # A1: a targeted repin cannot be saved while another feature has an error.
    def test_a1_targeted_repin_is_saved_while_another_feature_is_stale(self):
        repo = self.started()
        repo.feature("002-pay", spec=SPEC_PAY, tasks="- [ ] T001 Build pay\n")
        code, out = repo.check("--write", "--repin", "specs/002-pay")
        self.assertEqual(code, 0, out)
        repo.commit("two features in flight")
        repo.edit(".specify/memory/architecture.md", "| Language | Python | D-001 |",
                  "| Language | Python | D-001 |\n| Database | Postgres | D-001 |")
        before = repo.read("specs/001-login/baseline-pins.json")
        code, out = repo.check("--repin", "specs/001-login/plan.md", "--reason", "reviewed stack")
        self.assertNotEqual(repo.read("specs/001-login/baseline-pins.json"), before, out)

    # A2: one feature's error blocks the implement gate of every other feature.
    def test_a2_gate_of_the_current_feature_ignores_another_features_error(self):
        repo = self.verified()
        repo.feature("002-pay", spec=SPEC_PAY, tasks="- [ ] T001 Build pay\n")
        code, out = repo.check("--write", "--repin", "specs/002-pay")
        self.assertEqual(code, 0, out)
        repo.edit("specs/001-login/spec.md", "Login works.", "Login works with a passkey.")
        # Spec Kit's own pointer to the feature being worked on.
        repo.write(".specify/feature.json", json.dumps({"feature_directory": "specs/002-pay"}))
        code, out = repo.check("--gate", "--feature", "current")
        self.assertEqual(code, 0, out)
        self.assertIn("001-login", out)  # still reported, as a warning

    # A3: the documented way to change a promise (amend the row, then a Changes spec) deadlocks.
    def test_a3_changing_a_promise_through_a_changes_spec_is_not_blocked(self):
        repo = self.verified()
        repo.commit("001 done")
        repo.edit(".specify/memory/product.md", "Customers can log in.", "Customers can log in with a passkey.")
        repo.feature("002-passkeys", spec=SPEC_CHANGES_LOGIN, tasks="- [ ] T001 Add passkeys\n")
        code, out = repo.check("--write", "--repin", "specs/002-passkeys")
        self.assertEqual(code, 0, out)
        self.assertEqual(repo.delivery("CAP-001"), "in progress")

    # A4: any edit to verification.md re-verifies a changed spec, without a new run.
    def test_a4_touching_verification_md_does_not_reverify_a_changed_spec(self):
        repo = self.verified()
        repo.edit("specs/001-login/spec.md", "Login works.", "Login works within 200 ms.")
        repo.edit("specs/001-login/verification.md", "## Historical runs", "Reviewed again.\n\n## Historical runs")
        code, out = repo.check("--write")
        self.assertEqual(code, 1, out)
        self.assertIn("changed after the feature was verified", out)

    # A5: a deleted row is only an error until the deletion is committed.
    def test_a5_a_committed_deletion_is_still_an_error(self):
        repo = self.repo
        repo.edit(".specify/memory/decisions.md",
                  "| D-003 | 2026-10-09 | Which database? | MongoDB | - | App | rejected |\n", "")
        repo.commit("drop D-003")
        base = subprocess.check_output(["git", "-C", str(repo.root), "rev-list", "--max-parents=0", "HEAD"], text=True).strip()
        code, out = repo.check("--base", base)
        self.assertEqual(code, 1, out)
        self.assertIn("D-003", out)

    # A6: parallel features that touch different capabilities still conflict at merge.
    def test_a6_parallel_features_merge_cleanly(self):
        repo = self.repo
        code, out = repo.check("--write", "--stamp")
        self.assertEqual(code, 0, out)
        repo.commit("stamp")
        base = subprocess.run(["git", "-C", str(repo.root), "branch", "--show-current"],
                              capture_output=True, text=True, check=True).stdout.strip()
        repo.git("checkout", "-q", "-b", "feature-a")
        repo.feature("001-login")
        self.assertEqual(repo.check("--write", "--repin", "specs/001-login")[0], 0)
        repo.commit("A")
        repo.git("checkout", "-q", base)
        repo.git("checkout", "-q", "-b", "feature-b")
        repo.feature("002-pay", spec=SPEC_PAY)
        self.assertEqual(repo.check("--write", "--repin", "specs/002-pay")[0], 0)
        repo.commit("B")
        repo.git("checkout", "-q", base)
        repo.git("merge", "-q", "--no-edit", "feature-a")
        merged = subprocess.run(["git", "-C", str(repo.root), "-c", "user.name=t", "-c", "user.email=t@example.com",
                                 "merge", "--no-edit", "feature-b"], capture_output=True, text=True)
        self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)

    # A7: failure words outside the Coverage table are matched case-sensitively.
    def test_a7_failed_acceptance_evidence_blocks_done(self):
        extra = ("## Additional acceptance evidence\n\n"
                 "| AS / SC | Method and platform | Expected | Observed | Status / evidence |\n"
                 "|---------|---------------------|----------|----------|-------------------|\n"
                 "| AS-001 | manual walkthrough | shop shown | error page | Failed |\n\n## Convergence")
        repo = self.started()
        repo.write("specs/001-login/verification.md", VERIFICATION.replace("## Convergence", extra))
        code, out = repo.check("--write")
        self.assertEqual(code, 1, out)

    # A8: skipped and xfailed counts pass (listed as open by the agent).
    def test_a8_skipped_tests_block_done_without_a_reason(self):
        repo = self.started()
        repo.write("specs/001-login/verification.md", VERIFICATION.replace("| 1 / 0 / 0 / 0 |", "| 1 / 0 / 2 / 0 |"))
        code, out = repo.check("--write")
        self.assertEqual(code, 1, out)

    # A9: evidence written as a plain path is never checked (listed as open by the agent).
    def test_a9_plain_evidence_path_must_exist(self):
        repo = self.started()
        repo.write("specs/001-login/verification.md",
                   VERIFICATION.replace("| evidence/run.log |", "| evidence/pytest-run.log |"))
        code, out = repo.check("--write")
        self.assertEqual(code, 1, out)

    # A10: an unescaped pipe still truncates a rule's command and inverts its result.
    def test_a10_unescaped_pipe_is_a_table_error_not_a_rule_failure(self):
        repo = self.repo
        repo.edit(".specify/memory/architecture.md", "| AR-001 | No print statements. | yes | - |",
                  "| AR-001 | No print statements. | yes | grep -rn print src | wc -l | grep -qx 0 |")
        code, out = repo.check("--run-rule-checks")
        self.assertNotIn("AR-001 check failed", out)  # today the truncated command runs and "fails"
        self.assertIn("AR-001", out)  # the malformed row is reported instead

    # A11: any <Word> in recorded evidence is treated as an unfilled placeholder.
    def test_a11_angle_brackets_in_evidence_are_not_placeholders(self):
        repo = self.verified()
        repo.write("specs/001-login/verification.md",
                   VERIFICATION.replace("| PASS | abc1234 |", "| PASS | screenshot shows the <LoginBanner> component |"))
        code, out = repo.check("--write")
        self.assertEqual(code, 0, out)

    # A12: any file named spec.md below a feature becomes a feature of its own.
    def test_a12_spec_md_inside_a_feature_is_not_a_feature(self):
        repo = self.started()
        repo.write("specs/001-login/contracts/openapi/spec.md", "# OpenAPI notes\n")
        code, out = repo.check()
        self.assertEqual(code, 0, out)

    # A13: "pinned ..." is printed even when the run then writes nothing.
    def test_a13_no_pinned_message_when_nothing_is_written(self):
        repo = self.repo
        repo.edit(".specify/memory/product.md", "| CAP-001 | Customers can log in. | approved",
                  "| CAP-001 | Customers can log in. | proposed")
        repo.feature()
        code, out = repo.check("--write", "--repin")
        self.assertIn("nothing was written", out)
        self.assertNotIn("pinned CAP-001", out)


if __name__ == "__main__":
    unittest.main()
