"""Schema, execution and historical transition failure-path regressions."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_baseline_check import Repo, SPEC, PLAN, VERIFICATION, SCRIPT


class EvidenceContractTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Repo(self.tmp.name)
        self.repo.feature()
        self.assertEqual(self.repo.check('--write', '--repin', '001-login')[0], 0)

    def finish(self, key='001-login'):
        r = self.repo
        self.assertEqual(r.check('--record-run', '--feature', key)[0], 0)
        r.write(f'specs/{key}/verification.md', VERIFICATION)
        self.assertEqual(r.check('--write', '--feature', key)[0], 0)

    def test_mandatory_gate_cannot_be_mutated_or_redirected(self):
        r = self.repo
        old = r.read('.specify/memory/baseline-state.json')
        for option in ('--mode advisory', '--scan', '--structural', '--acknowledge', '--context', '--write'):
            with self.subTest(option=option):
                self.assertEqual(r.check('--gate', *option.split())[0], 1)
                self.assertEqual(r.read('.specify/memory/baseline-state.json'), old)

    def test_record_run_dry_run_never_executes(self):
        r = self.repo
        r.edit('specs/001-login/plan.md', 'python3 src/app.py |', 'touch sentinel |')
        code, output = r.check('--record-run', '--feature', '001-login', '--dry-run')
        self.assertEqual(code, 0, output)
        self.assertIn('would execute', output)
        self.assertFalse((r.root / 'sentinel').exists())
        self.assertFalse((r.root / 'specs/001-login/verification-run.json').exists())

    def test_new_file_during_run_aborts_acceptance(self):
        r = self.repo
        r.edit('specs/001-login/plan.md', 'python3 src/app.py |', 'touch sentinel |')
        code, output = r.check('--record-run', '--feature', '001-login')
        self.assertEqual(code, 1, output)
        self.assertIn('inventory changed', output)
        self.assertFalse((r.root / 'specs/001-login/verification-run.json').exists())

    def test_run_record_wrong_shapes_never_crash(self):
        r = self.repo
        self.finish()
        path = 'specs/001-login/verification-run.json'
        original = json.loads(r.read(path))
        for field, value in (('inputs', []), ('checks', []), ('checks', [7]), ('checks', [{'evidence': 7}]), ('observations', {}), ('observations', [7])):
            record = dict(original); record[field] = value
            r.write(path, json.dumps(record))
            code, output = r.check('--gate')
            self.assertEqual(code, 1, output)
            self.assertNotIn('Traceback', output)

    def test_commands_counts_and_skips_are_bound_to_run(self):
        r = self.repo
        self.finish()
        original = r.read('specs/001-login/verification.md')
        for old, new in (('python3 src/app.py', 'true'), ('1 / 0 / 0 / 0', ''), ('1 / 0 / 0 / 0', '1 / 0 / 1 / 0'), ('1 / 0 / 0 / 0', '1 / 0 / 0 / 1'), ('| . |', '| |')):
            r.write('specs/001-login/verification.md', original.replace(old, new) + '\nSkip reason: unavailable platform.\n')
            self.assertEqual(r.check('--write')[0], 1)

    def test_log_change_and_constitution_change_invalidate(self):
        r = self.repo
        r.write('.specify/memory/constitution.md', 'approved working rules')
        self.finish()
        record = json.loads(r.read('specs/001-login/verification-run.json'))
        log = record['checks'][0]['evidence']
        old = r.read(log)
        r.write(log, 'fabricated output')
        self.assertIn('run evidence is missing or changed', r.check('--gate')[1])
        r.write(log, old)
        r.write('.specify/memory/constitution.md', 'changed working rules')
        self.assertIn('baseline changed', r.check('--gate')[1])

    def test_manual_observations_need_hashed_evidence_and_complete_fields(self):
        r = self.repo
        self.finish()
        path = 'specs/001-login/verification-run.json'
        record = json.loads(r.read(path))
        evidence = 'specs/001-login/evidence/manual.txt'
        r.write(evidence, 'observed login success')
        obs = dict(method='walkthrough', platform='browser', expected='shop', observed='shop', status='PASS',
                   evidence=evidence, digest=hashlib.sha256(b'observed login success').hexdigest()[:16])
        record['observations'] = [obs]
        r.write(path, json.dumps(record))
        report = r.read('specs/001-login/verification.md')
        extra = '\n## Additional acceptance evidence\n\n| AS / SC | Method and platform | Expected | Observed | Status / evidence |\n|---|---|---|---|---|\n| AS-001 | walkthrough browser | shop | shop | PASS / [observation](' + evidence + ') |\n'
        r.write('specs/001-login/verification.md', report.replace('## Convergence', extra + '\n## Convergence'))
        self.assertEqual(r.check('--write')[0], 0)
        r.write(evidence, 'different observation')
        self.assertIn('manual observation evidence changed', r.check('--gate')[1])
        obs.pop('method'); r.write(path, json.dumps(record))
        self.assertEqual(r.check('--gate')[0], 1)

    def test_contract_code_inputs_and_bad_working_directory(self):
        r = self.repo
        r.write('api.md', '# API v1')
        r.edit('.specify/memory/architecture.md', '- The HTTP API is described in the plan of each feature.', '- [API](../../api.md)')
        self.finish()
        r.write('api.md', '# API v2')
        self.assertIn('contracts changed', r.check('--gate')[1])
        r.edit('specs/001-login/plan.md', '| smoke | . |', '| smoke | ../ |')
        self.assertEqual(r.check('--record-run', '--feature', '001-login')[0], 1)

    def test_multiple_historical_changes_keep_original_records(self):
        r = self.repo
        self.finish()
        for key, promise, pred in (('002-mfa', 'MFA', ''), ('003-otp', 'OTP', '**Previous change**: specs/002-mfa\n')):
            r.edit('.specify/memory/product.md', 'Customers can log in.' if key == '002-mfa' else 'MFA', promise)
            r.feature(key, spec=SPEC.replace('**Implements**', '**Changes**') + pred)
            self.assertEqual(r.check('--write', '--feature', key, '--repin', key)[0], 0)
            self.finish(key)
        self.assertEqual(r.check('--gate')[0], 0)
        r.edit('specs/001-login/verification-run.json', '"date":', '"tampered":')
        # Harmless metadata is allowed; input bindings and run ID remain authoritative.
        record = json.loads(r.read('specs/001-login/verification-run.json'))
        record['id'] = 'f' * 32
        r.write('specs/001-login/verification-run.json', json.dumps(record))
        self.assertIn('historical run differs', r.check('--gate')[1])

    def test_context_and_touched_failure_paths(self):
        r = self.repo
        for args in (('--context', '--ids', 'CAP-999'), ('--touched', 'missing'), ('--touched', '001-login'), ('--gate', '--base', 'no-such-commit')):
            self.assertEqual(r.check(*args)[0], 1)
        r.edit('specs/001-login/spec.md', '**Baseline**: abc1234', '**Baseline**: deadbee')
        self.assertIn('git cannot compare', r.check('--touched', '001-login')[1])
        r.edit('.specify/memory/architecture.md', '- The HTTP API is described in the plan of each feature.', '- [external](https://example.test/api)')
        self.assertIn('omitted (external', r.check('--context', '--paths', 'src')[1])
        r.write('huge.md', 'x' * 65537)
        r.edit('.specify/memory/architecture.md', 'https://example.test/api', '../../huge.md')
        self.assertIn('64 KiB', r.check('--context', '--paths', 'src')[1])

    def test_shared_tooling_affects_every_feature_binding(self):
        r = self.repo
        r.write('pyproject.toml', '[project]\nname="shop"\n')
        r.edit('.specify/memory/architecture.md', '| App | Requests | src, main.py | - | built |', '| App | Requests | src, main.py | - | built |\n| Tooling | Build inputs | pyproject.toml | - | built |')
        r.write('.specify/memory/architecture.md', r.read('.specify/memory/architecture.md') + '\n**Verification inputs**: Tooling\n')
        self.finish()
        r.write('pyproject.toml', '[project]\nname="different"\n')
        self.assertIn('code changed', r.check('--gate')[1])

    def test_parallel_scoped_writers_and_interrupted_journal(self):
        import base64
        r = self.repo
        r.feature('002-pay', spec=SPEC.replace('CAP-001', 'CAP-002'))
        calls = [subprocess.Popen([sys.executable, str(SCRIPT), '--root', str(r.root), '--write', '--feature', key, '--repin', key], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for key in ('001-login', '002-pay')]
        for process in calls:
            output, error = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 0, output + error)
        for key in ('001-login', '002-pay'):
            self.assertTrue(json.loads(r.read(f'specs/{key}/baseline-pins.json'))['pins'])
        name = 'specs/001-login/baseline-pins.json'
        old = r.read(name)
        r.write('.specify/.baseline-local/journal.json', json.dumps({name: base64.b64encode(old.encode()).decode(), 'newly-created.txt': None}))
        r.write(name, 'interrupted corrupt write')
        r.write('newly-created.txt', 'partial write')
        self.assertIn('interrupted transaction', r.check('--gate')[1])
        self.assertEqual(r.check()[0], 0)
        self.assertEqual(r.read(name), old)
        self.assertFalse((r.root / 'newly-created.txt').exists())

    def test_unicode_code_paths_and_root_discovery(self):
        r = self.repo
        r.write('src/صفحة.py', 'first state')
        self.finish()
        r.write('src/صفحة.py', 'second state')
        self.assertIn('code changed', r.check('--gate')[1])
        result = subprocess.run([sys.executable, str(SCRIPT), '--status'], cwd=r.root / 'src', capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('CAP-001: in progress', result.stdout)

    def test_no_git_and_empty_evidence_paths(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '.specify').mkdir()
            result = subprocess.run([sys.executable, str(SCRIPT), '--root', folder, '--scan'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
        r = self.repo
        self.finish()
        original = r.read('specs/001-login/verification.md')
        for old, new in (('Status |', 'Result |'), ('Exit code |', 'Result |'), ('1/1', '0/1'), ('Outcome: converged', 'Outcome:')):
            r.write('specs/001-login/verification.md', original.replace(old, new))
            self.assertEqual(r.check('--write')[0], 1)
        r.write('specs/001-login/tasks.md', '# no tasks')
        self.assertEqual(r.check('--write')[0], 1)

    def test_exact_shipped_workflow_and_ci_gates(self):
        import shutil
        import yaml
        r = self.repo
        self.finish()
        package = SCRIPT.parents[2]
        installed = r.root / '.specify/extensions/baseline/scripts'
        installed.mkdir(parents=True)
        for path in SCRIPT.parent.glob('*.py'):
            shutil.copy2(path, installed / path.name)
        r.write('.specify/feature.json', json.dumps({'feature_directory': 'specs/001-login'}))
        steps = yaml.safe_load((package / 'workflow/workflow.yml').read_text())['steps']
        commands = [step['run'] for step in steps if step.get('type') == 'shell']
        ci = yaml.safe_load((package / 'extension/ci/baseline.yml').read_text())['jobs']['baseline']['steps'][-1]['run']
        commands.append(ci)
        base = subprocess.check_output(['git', '-C', str(r.root), 'rev-parse', 'HEAD'], text=True).strip()
        for command in commands:
            result = subprocess.run(['bash', '-c', command], cwd=r.root, capture_output=True, text=True,
                                    env={**__import__('os').environ, 'BASELINE_PR_BASE': base})
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        r.write('specs/001-login/verification.md', 'Completion: NOT DONE\n')
        final = subprocess.run(['bash', '-c', commands[1]], cwd=r.root, capture_output=True, text=True)
        self.assertEqual(final.returncode, 1)
        (r.root / '.specify/memory/product.md').unlink()
        for command in (commands[0], ci):
            result = subprocess.run(['bash', '-c', command], cwd=r.root, capture_output=True, text=True,
                                    env={**__import__('os').environ, 'BASELINE_PR_BASE': base})
            self.assertEqual(result.returncode, 1)

    def test_recovery_does_not_overwrite_invalid_state(self):
        r = self.repo
        path = '.specify/memory/baseline-state.json'
        r.write(path, '{"stamp": []}')
        self.assertEqual(r.check('--mode', 'advisory')[0], 1)
        self.assertEqual(r.read(path), '{"stamp": []}')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '.specify').mkdir()
            result = subprocess.run([sys.executable, str(SCRIPT), '--root', folder, '--dry-run', '--mode', 'advisory'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertFalse((root / '.specify/memory/baseline-state.json').exists())
