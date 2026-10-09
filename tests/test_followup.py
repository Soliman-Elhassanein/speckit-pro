"""Acceptance transitions, not just isolated field checks, from the follow-up audits."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_baseline_check import Repo, SPEC, PLAN, VERIFICATION, SCRIPT


class FollowupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Repo(self.tmp.name)

    def start(self, key='001-login', spec=SPEC):
        r = self.repo
        r.feature(key, spec=spec)
        code, out = r.check('--write', '--repin', 'specs/' + key)
        self.assertEqual(code, 0, out)
        return r

    def finish(self, key='001-login'):
        r = self.repo
        code, out = r.check('--record-run', '--feature', 'specs/' + key)
        self.assertEqual(code, 0, out)
        r.write(f'specs/{key}/evidence/run.log', 'observation\n')
        r.write(f'specs/{key}/verification.md', VERIFICATION)
        code, out = r.check('--write', '--feature', 'specs/' + key)
        self.assertEqual(code, 0, out)
        return r

    def verified(self):
        self.start()
        return self.finish()

    def test_cosmetic_edits_cannot_renew_evidence(self):
        r = self.verified()
        r.edit('specs/001-login/spec.md', 'Login works.', 'Login needs MFA.')
        for edit in ('\n<!-- comment -->', '\nRun date: tomorrow', '\n\n'):
            r.write('specs/001-login/verification.md', VERIFICATION + edit)
            code, out = r.check('--write')
            self.assertEqual(code, 1, out)
            self.assertNotEqual(r.delivery('CAP-001'), 'verified')

    def test_deleted_adopted_baseline_and_required_nonadopter_fail(self):
        r = self.verified()
        (r.memory / 'product.md').unlink()
        self.assertEqual(r.check('--strict')[0], 1)
        self.assertEqual(r.check('--gate')[0], 1)

    def test_advisory_cannot_weaken_gate_or_promote(self):
        r = self.start()
        self.assertEqual(r.check('--mode', 'advisory')[0], 0)
        r.edit('.specify/memory/product.md', '| approved |', '| proposed |')
        r.write('specs/001-login/evidence/run.log', 'observation\n')
        r.write('specs/001-login/verification.md', VERIFICATION)
        pins = r.read('specs/001-login/baseline-pins.json')
        self.assertEqual(r.check('--write')[0], 0)  # diagnostic-only preference
        self.assertEqual(r.read('specs/001-login/baseline-pins.json'), pins)
        self.assertNotEqual(r.delivery('CAP-001'), 'verified')
        self.assertEqual(r.check('--gate')[0], 1)

    def test_code_freshness_independent_of_stamp_and_other_active_feature(self):
        r = self.verified()
        r.write('src/app.py', 'raise RuntimeError("broken")\n')
        for args in (('--write', '--stamp', '--reason', 'reviewed mapping'), ('--strict',)):
            self.assertEqual(r.check(*args)[0], 1)
        r.feature('002-pay', spec=SPEC.replace('CAP-001', 'CAP-002'))
        self.assertEqual(r.check('--gate', '--feature', '001-login')[0], 1)

    def test_completed_pin_deletion_and_governing_changes_fail(self):
        r = self.verified()
        old = r.read('specs/001-login/baseline-pins.json')
        (r.root / 'specs/001-login/baseline-pins.json').unlink()
        self.assertEqual(r.check('--write')[0], 1)
        r.write('specs/001-login/baseline-pins.json', old)
        r.edit('.specify/memory/architecture.md', 'No print statements.', 'MFA required.')
        self.assertEqual(r.check('--strict')[0], 1)

    def test_task_meaning_invalidates_but_checkbox_bookkeeping_does_not(self):
        r = self.start()
        r.write('specs/001-login/tasks.md', '- [ ] T001 Build login\n')
        self.assertEqual(r.check('--record-run', '--feature', '001-login')[0], 0)
        r.write('specs/001-login/tasks.md', '- [x] T001 Build login\n')
        r.write('specs/001-login/evidence/run.log', 'observation\n')
        r.write('specs/001-login/verification.md', VERIFICATION)
        self.assertEqual(r.check('--write')[0], 0)
        r.write('specs/001-login/tasks.md', '- [x] T999 Completely different work\n')
        self.assertEqual(r.check('--strict')[0], 1)

    def test_revision_change_preparation_and_completion_preserve_history(self):
        r = self.verified()
        old = r.read('specs/001-login/baseline-pins.json')
        r.edit('.specify/memory/product.md', 'Customers can log in.', 'Customers can log in with MFA.')
        r.feature('002-mfa', spec=SPEC.replace('**Implements**', '**Changes**'))
        code, out = r.check('--write', '--repin', 'specs/002-mfa')
        self.assertEqual(code, 0, out)
        self.assertEqual(r.delivery('CAP-001'), 'in progress')
        self.finish('002-mfa')
        self.assertEqual(r.delivery('CAP-001'), 'verified')
        self.assertEqual(r.read('specs/001-login/baseline-pins.json'), old)

    def test_first_done_cannot_bypass_question_or_rejected_decision(self):
        r = self.start()
        r.edit('.specify/memory/product.md', '|----|----------|--------|--------|--------|',
               '|----|----------|--------|--------|--------|\n| Q-001 | MFA? | CAP-001 | today | open |')
        r.write('specs/001-login/verification.md', VERIFICATION)
        code, out = r.check('--write')
        self.assertEqual(code, 1, out)
        self.assertIn('blocked by open question', out)
        r.edit('specs/001-login/plan.md', '**Decisions**: D-001', '**Decisions**: D-003')
        self.assertIn("whose status is 'rejected'", r.check()[1])

    def test_gate_runs_blocking_rules_and_final_completion(self):
        r = self.verified()
        r.edit('.specify/memory/architecture.md', '| yes | - |', '| yes | `false` |')
        self.assertEqual(r.check('--gate')[0], 1)
        r.write('specs/001-login/verification.md', 'Completion: NOT DONE\n')
        self.assertEqual(r.check('--gate', '--require-done', '--feature', '001-login')[0], 1)

    def test_committed_deletion_against_accepted_base(self):
        r = self.start()
        r.write('.specify/memory/decisions.md', '\n'.join(l for l in r.read('.specify/memory/decisions.md').splitlines() if 'D-003' not in l))
        r.commit('delete decision')
        self.assertEqual(r.check('--gate')[0], 1)
        self.assertIn('unavailable', r.check('--gate', '--base', 'deadbeef')[1])

    def test_context_missing_file_duplicate_and_contract_content(self):
        r = self.repo
        r.write('api.md', 'Actual contract detail\n')
        r.edit('.specify/memory/architecture.md', '- The HTTP API is described in the plan of each feature.', '- [API](../../api.md)')
        code, out = r.check('--context', '--paths', 'src')
        self.assertEqual(code, 0, out)
        self.assertIn('Actual contract detail', out)
        r.write('.specify/memory/decisions.md', r.read('.specify/memory/decisions.md') + '| D-002 | today | x | y | z | - | rejected |\n')
        self.assertEqual(r.check('--context')[0], 1)
        (r.memory / 'decisions.md').unlink()
        self.assertEqual(r.check('--context')[0], 1)

    def test_invalid_state_shapes_have_controlled_diagnostics(self):
        r = self.start()
        for value in ({'pins': []}, {'pins': {'spec.md': []}}, {'verified': []}, {'accepted': []}, {'version': 999}):
            r.write('specs/001-login/baseline-pins.json', json.dumps(value))
            code, out = r.check('--write')
            self.assertEqual(code, 1, out)
            self.assertNotIn('Traceback', out)
        r.write('.specify/memory/baseline-state.json', '{"stamp": []}')
        self.assertNotIn('Traceback', r.check()[1])

    def test_recovery_mode_initializes_without_product(self):
        root = Path(self.tmp.name) / 'new'
        (root / '.specify').mkdir(parents=True)
        result = subprocess.run([sys.executable, str(SCRIPT), '--root', str(root), '--mode', 'advisory'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads((root / '.specify/memory/baseline-state.json').read_text())['mode'], 'advisory')

    def test_repin_dry_run_reason_and_truthful_no_write(self):
        r = self.start()
        before = r.read('specs/001-login/baseline-pins.json')
        r.edit('.specify/memory/architecture.md', '| Language | Python |', '| Language | Go |')
        self.assertEqual(r.check('--repin', '001-login/plan.md')[0], 1)
        code, out = r.check('--repin', '001-login/plan.md', '--reason', 'reviewed', '--dry-run')
        self.assertEqual(code, 0, out)
        self.assertEqual(before, r.read('specs/001-login/baseline-pins.json'))
        self.assertIn('would write', out)
        self.assertNotIn('pinned ', out)

    def test_scan_and_touched_include_root_hidden_and_untracked(self):
        r = self.start()
        commit = subprocess.check_output(['git', '-C', str(r.root), 'rev-parse', 'HEAD'], text=True).strip()
        r.edit('specs/001-login/spec.md', 'abc1234', commit)
        r.write('main.py', 'changed\n')
        r.write('src/new.py', 'new\n')
        r.write('.github/a.yml', 'test\n')
        r.commit('new files')
        code, out = r.check('--scan')
        self.assertEqual(code, 0, out)
        self.assertIn('(root files)', out)
        self.assertIn('.github', out)
        code, out = r.check('--touched', '001-login')
        self.assertEqual(code, 0, out)
        self.assertIn('main.py -> App', out)
        self.assertIn('src/new.py -> App', out)

    def test_abandoned_feature_stops_excusing_drift_and_stamp_requires_done(self):
        r = self.start()
        self.assertEqual(r.check('--write', '--stamp', '001-login')[0], 1)
        self.assertEqual(r.check('--write', '--stamp')[0], 0)
        r.write('src/app.py', 'changed\n')
        r.write('specs/001-login/verification.md', 'Completion: ABANDONED\n')
        self.assertIn('changed since its synced point', r.check()[1])

    def test_runner_failure_and_modified_logs_cannot_verify(self):
        r = self.start()
        r.write('src/app.py', 'raise RuntimeError("failed")\n')
        code, out = r.check('--record-run', '--feature', '001-login')
        self.assertEqual(code, 1, out)
        record = json.loads(r.read('specs/001-login/verification-run.json'))
        self.assertNotEqual(record['checks'][0]['exit'], 0)
        r.write('specs/001-login/evidence/run.log', 'fake\n')
        r.write('specs/001-login/verification.md', VERIFICATION)
        self.assertEqual(r.check('--write')[0], 1)


class StorageTest(unittest.TestCase):
    def test_rollback_at_each_write_and_snapshot_guard(self):
        sys.path.insert(0, str(SCRIPT.parent))
        import baseline_store as store
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            a, b = root / 'a', root / 'b'
            a.write_text('old a'); b.write_text('old b')
            for fail_at in (2, 3):  # journal is write 1
                original = store.atomic
                calls = 0
                def fail(path, data):
                    nonlocal calls
                    calls += 1
                    if calls == fail_at: raise OSError('injected failure')
                    return original(path, data)
                with store.locked(root) as local:
                    with patch.object(store, 'atomic', side_effect=fail):
                        with self.assertRaises(OSError):
                            store.transact(root, local, {a: 'new a', b: 'new b'}, {a: b'old a', b: b'old b'})
                self.assertEqual(a.read_text(), 'old a'); self.assertEqual(b.read_text(), 'old b')
            with store.locked(root) as local:
                with self.assertRaises(ValueError): store.transact(root, local, {a: 'new'}, {a: b'wrong'})

    def test_bounded_runner_timeout_output_and_pipeline_failure(self):
        sys.path.insert(0, str(SCRIPT.parent))
        from baseline_runtime import run
        with tempfile.TemporaryDirectory() as root:
            self.assertNotEqual(run('false | true', root)[0], 0)
            code, out = run('sleep 3', root, timeout=.05)
            self.assertEqual(code, 124); self.assertIn('timed out', out)
            code, out = run('yes x', root, limit=100)
            self.assertEqual(code, 124); self.assertIn('output exceeded', out)


if __name__ == '__main__': unittest.main()
