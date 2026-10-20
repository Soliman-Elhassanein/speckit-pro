"""Offline regressions for retained memory and completion structure."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'extension/scripts/baseline_check.py'
PRODUCT = '''# Product
## Spirit

Purpose: Login for members.
Users: Members.
### Non-goals

- Public access.

## Capabilities

| ID | Promise | Serves | Decision | Depends on |
|----|---------|--------|----------|------------|
| CAP-001 | Login | PR-001 | approved | - |

| ID | Rule |
|----|------|
| PR-001 | Private by default |
'''
ARCHITECTURE = '''# Architecture
| Part | Owns | Paths | May depend on |
|------|------|-------|---------------|
| Worker | Jobs | future/worker | - |

| ID | Rule | Check |
|----|------|-------|
| AR-001 | No logging | `false \| cat` |
'''
AREAS = ('git & branching', 'PRs & review', 'environments', 'CI/CD', 'code quality',
         'testing', 'documentation', 'issues & tasks', 'release & versioning', 'security',
         'database changes', 'observability', 'dependencies', 'repository governance')
ARCHITECTURE += '\n## Delivery standards\n\n| Area | Status | Rule | Check | Blocking |\n|---|---|---|---|---|\n'
ARCHITECTURE += ''.join(f'| {area} | undecided | - | - | no |\n' for area in AREAS)
DECISIONS = '''# Decisions
**Version**: 0.1.0
| ID | Decision | Rejected options | Status |
|----|----------|------------------|--------|
| D-001 | Python | Ruby: unavailable | accepted |
| D-002 | Guest access | - | rejected |
'''
SPEC = '**Implements**: CAP-001\n**Product rules**: PR-001\nFR-001 Login.\n\n## Focus\n\nVerdict: fits\nUser: Members\n**Promises**: PR-001\n**Override**: none\n'
PLAN = '''**Architecture rules**: AR-001
**Decisions**: D-001
## Quality gates

| Gate | Command |
|------|---------|
| tests | `python3 -m unittest` |
'''
VERIFICATION = '''Completion: DONE

## Execution

| Gate | Command | Exit code | Log path |
|------|---------|-----------|----------|
| tests | `python3 -m unittest` | 0 | evidence/tests.log |

## Remaining gaps

None

## Convergence

Outcome: converged
'''


class BaselineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name, text in [('product.md', PRODUCT), ('architecture.md', ARCHITECTURE),
                           ('decisions.md', DECISIONS)]:
            self.write('.specify/memory/' + name, text)
        self.feature = 'specs/nested/001 login'
        for name, text in [('spec.md', SPEC), ('plan.md', PLAN),
                           ('tasks.md', '- [x] T001 Build login\n'),
                           ('verification.md', VERIFICATION)]:
            self.write(self.feature + '/' + name, text)
        self.write('evidence/tests.log', 'test output\n')

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def check(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root), *args],
                              text=True, capture_output=True)

    def assert_check(self, status, *args):
        result = self.check(*args)
        self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        return result.stdout

    def test_valid_memory_and_done_are_read_only(self):
        before = {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assert_check(0)
        self.assert_check(0, '--done', '--feature', self.feature)
        self.assertEqual(before, {p: p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_privacy_shapes_block_in_every_memory_file_and_advisory(self):
        samples = (
            '/home/example/project', '/Users/example/project', '/root/project',
            r'C:\example\project', '~/project', '/etc/service/config',
            '/data/private', '/private/file', '192.0.2.7', '127.0.0.1',
            '192.0.2.7.', '2001:db8::7', '2001:db8::7.', '[2001:db8::7]', '::1', '::',
            '::ffff:192.0.2.7', 'fe80::7%eth0',
            'fake@example.invalid', 'https://fake:example@example.invalid/repo',
            'https://fake@example.invalid/repo',
            '-----BEGIN PRIVATE KEY-----', '-----BEGIN RSA PRIVATE KEY-----',
            '-----BEGIN OPENSSH PRIVATE KEY-----',
            'AKIA' + 'A' * 16, 'ghp_' + 'a' * 36,
            'github_pat_' + 'a' * 60, 'sk-' + 'a' * 32,
            'xoxb-' + '1234567890-' * 3,
            'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmYWtlIn0.ZmFrZQ',
            'password=fake-value', 'secret="fake-value"', "token='fake-value'",
            'PASSWORD = fake-value',
        )
        for name, base in (('product.md', PRODUCT), ('architecture.md', ARCHITECTURE),
                           ('decisions.md', DECISIONS), ('constitution.md', '# Rules\n')):
            for sample in samples:
                with self.subTest(file=name, shape=sample[:16]):
                    self.write('.specify/memory/' + name, base + '\n' + sample + '\n')
                    for args in ((), ('--mode', 'advisory')):
                        output = self.assert_check(1, *args)
                        self.assertIn('privacy: ' + name, output)
                        self.assertNotIn(sample, output)
            self.write('.specify/memory/' + name, base)

    def test_public_generic_memory_and_repo_relative_paths_pass(self):
        self.write('.specify/memory/constitution.md', '# Rules\nUse the database host and the config file.\n')
        self.write('.specify/memory/product.md', PRODUCT +
                   '\nSource feature: specs/007-login; src/main.py; .config/example; '
                   'src/home/example; https://example.invalid/docs; version 1.2.2; password=""; token=\n')
        self.assert_check(0)
        self.assert_check(0, '--mode', 'advisory')
        self.assert_check(0, '--done')

    def test_missing_each_memory_file_is_visible_even_in_advisory(self):
        for name in ('product.md', 'architecture.md', 'decisions.md'):
            with self.subTest(name=name):
                path = self.root / '.specify/memory' / name
                content = path.read_text()
                path.unlink()
                self.assertIn(name, self.assert_check(1))
                self.assertIn(name, self.assert_check(0, '--mode', 'advisory'))
                self.assert_check(1, '--done', '--mode', 'advisory', '--feature', self.feature)
                path.write_text(content)

    def test_duplicate_and_invalid_ids(self):
        for row in ('| CAP-001 | Duplicate | PR-001 | approved | - |', '| CAP-01 | Bad ID | PR-001 | approved | - |'):
            with self.subTest(row=row):
                self.write('.specify/memory/product.md', PRODUCT.replace('| CAP-001 | Login | PR-001 | approved | - |', row + '\n| CAP-001 | Login | approved | - |'))
                self.assert_check(1)

    def test_explicit_citations_only(self):
        self.write(self.feature + '/plan.md', PLAN + '\nPR-123 is a pull request; rejected in D-002.\n')
        self.assert_check(0)
        self.write(self.feature + '/spec.md', SPEC.replace('CAP-001', 'CAP-999'))
        self.assertIn('CAP-999', self.assert_check(1))

    def test_rejected_and_superseded_decisions_cannot_govern(self):
        for status in ('rejected', 'superseded by D-002'):
            with self.subTest(status=status):
                self.write('.specify/memory/decisions.md', DECISIONS.replace('| accepted |', '| ' + status + ' |'))
                self.assertIn('not accepted', self.assert_check(1))

    def test_missing_dependency_and_local_link(self):
        self.write('.specify/memory/product.md', PRODUCT.replace('| approved | - |', '| approved | CAP-999 |'))
        self.assertIn('CAP-999', self.assert_check(1))
        self.write('.specify/memory/product.md', PRODUCT + '\n[Contract](missing.md)\n')
        self.assertIn('link does not resolve', self.assert_check(1))

    def test_markdown_pipe_shape_is_validated_without_running_rule(self):
        self.assert_check(0)
        self.write('.specify/memory/architecture.md', ARCHITECTURE.replace(r'\|', '|'))
        self.assertIn('malformed table row', self.assert_check(1))

    def test_nested_contract_is_not_feature_and_explicit_scope_is_respected(self):
        self.write(self.feature + '/contracts/openapi/spec.md', '**Implements**: CAP-999\n')
        self.assert_check(0)
        self.write('specs/another/002/spec.md', '**Implements**: CAP-999\n')
        self.assert_check(1)
        self.assert_check(0, '--feature', str(self.root / self.feature) + '/')

    def test_empty_table_header_is_diagnosed(self):
        self.write('.specify/memory/product.md', PRODUCT + '\n|\n|\n')
        self.assertIn('malformed table row', self.assert_check(1))

    def test_answered_question_cites_accepted_decision(self):
        question = '\n| ID | Question | Blocks | Status |\n|---|---|---|---|\n| Q-001 | Why? | CAP-001 | answered by D-001 |\n'
        self.write('.specify/memory/product.md', PRODUCT + question)
        self.assert_check(0)
        for old, new in (('D-001', 'D-002'), ('CAP-001', 'CAP-999')):
            self.write('.specify/memory/product.md', PRODUCT + question.replace(old, new))
            self.assert_check(1)

    def test_missing_feature_is_error(self):
        self.assertIn('spec.md is missing', self.assert_check(1, '--feature', 'specs/missing'))

    def test_done_requires_complete_artifacts(self):
        for name in ('spec.md', 'plan.md', 'tasks.md', 'verification.md'):
            path = self.root / self.feature / name
            content = path.read_text()
            for missing in (True, False):
                with self.subTest(name=name, missing=missing):
                    if missing:
                        path.unlink()
                    else:
                        path.write_text('')
                    self.assert_check(1, '--done', '--feature', self.feature)
                    path.write_text(content)

    def test_two_line_done_unchecked_tasks_and_remaining_gaps_fail(self):
        self.write(self.feature + '/verification.md', 'Completion: DONE\nOutcome: converged\n')
        self.assert_check(1, '--done')
        self.write(self.feature + '/verification.md', VERIFICATION)
        self.write(self.feature + '/tasks.md', '- [ ] T001 Build login\n')
        self.assert_check(1, '--done')
        self.write(self.feature + '/tasks.md', '- [x] T001 Build login\n')
        self.write(self.feature + '/verification.md', VERIFICATION.replace('\nNone\n', '\nLogin broken\n'))
        self.assert_check(1, '--done')

    def test_done_rejects_failed_empty_or_mismatched_gate_records(self):
        for old, new in [('| 0 |', '| 1 |'), ('| 0 |', '| NOT RUN |'),
                         ('`python3 -m unittest`', ''), ('evidence/tests.log', ''),
                         ('evidence/tests.log', 'missing.log'), ('tests |', 'other |'),
                         ('converged', 'gaps_remaining')]:
            with self.subTest(new=new):
                self.write(self.feature + '/verification.md', VERIFICATION.replace(old, new))
                self.assert_check(1, '--done', '--feature', self.feature)

    def test_done_requires_all_planned_gates_and_preserves_escaped_pipes(self):
        self.write(self.feature + '/plan.md', PLAN + '| lint | `lint` |\n')
        self.assert_check(1, '--done')
        self.write(self.feature + '/plan.md', PLAN.replace('python3 -m unittest', r'false \| cat'))
        self.write(self.feature + '/verification.md', VERIFICATION.replace('python3 -m unittest', r'false \| cat'))
        self.assert_check(0, '--done')
        self.write(self.feature + '/plan.md', PLAN.replace('python3 -m unittest', 'cat < input.txt'))
        self.write(self.feature + '/verification.md', VERIFICATION.replace('python3 -m unittest', 'cat < input.txt'))
        self.assert_check(0, '--done')

    def test_done_rejects_each_nonconverged_outcome_even_in_advisory(self):
        for outcome in ('tasks_appended', 'gaps_remaining', 'NOT RUN', ''):
            with self.subTest(outcome=outcome):
                self.write(self.feature + '/verification.md', VERIFICATION.replace('Outcome: converged', 'Outcome: ' + outcome))
                self.assert_check(1, '--done', '--mode', 'advisory')

    def test_done_rejects_duplicate_malformed_and_placeholder_gates(self):
        for addition in ('| tests | `python3 -m unittest` | 0 | evidence/tests.log |\n',
                         '| extra | `true | cat` | 0 | evidence/tests.log |\n'):
            self.write(self.feature + '/verification.md', VERIFICATION.replace('\n\n## Remaining gaps', '\n' + addition + '\n## Remaining gaps'))
            self.assert_check(1, '--done')
        for marker in ('[Command]', '<command>', '-'):
            self.write(self.feature + '/plan.md', PLAN.replace('python3 -m unittest', marker))
            self.write(self.feature + '/verification.md', VERIFICATION.replace('python3 -m unittest', marker))
            self.assert_check(1, '--done')

    def test_spirit_and_non_goals_are_required(self):
        for text in (PRODUCT.replace('## Spirit', '## Purpose'),
                     PRODUCT.replace('### Non-goals', '### Other'),
                     PRODUCT.replace('- Public access.', '')):
            with self.subTest(text=text):
                self.write('.specify/memory/product.md', text)
                self.assertIn('Spirit', self.assert_check(1))
                self.assertIn('Spirit', self.assert_check(0, '--mode', 'advisory'))

    def test_focus_requires_its_own_typed_promise_or_override(self):
        for focus in ('', '## Focus\nPR-001 in ordinary prose.\n',
                      '## Focus\n**Promises**: CAP-001\n',
                      '## Focus\n**Promises**: PR-999\n',
                      '## Focus\n**Promises**: PR-01\n',
                      '## Focus\n**Override**: D-999\n',
                      '## Focus\n**Override**: D-002\n'):
            with self.subTest(focus=focus):
                self.write(self.feature + '/spec.md', SPEC.split('## Focus')[0] + focus)
                self.assert_check(1)
        self.write(self.feature + '/spec.md', '## Focus\n**Override**: D-001\n')
        self.assert_check(0)
        self.write('.specify/memory/decisions.md', DECISIONS.replace('| accepted |', '| superseded by D-002 |'))
        self.assertIn('not accepted', self.assert_check(1))

    def test_capability_serves_must_resolve_to_a_promise(self):
        for value in ('-', '', 'PR-999', 'CAP-001', 'PR-01'):
            with self.subTest(value=value):
                self.write('.specify/memory/product.md', PRODUCT.replace('| PR-001 | approved', '| ' + value + ' | approved'))
                self.assert_check(1)

    def test_delivery_status_blocking_and_all_areas(self):
        for status in ('decided', 'undecided', 'n/a: no database'):
            self.write('.specify/memory/architecture.md', ARCHITECTURE.replace('| undecided |', '| ' + status + ' |'))
            self.assert_check(0)
        for status in ('', 'unknown', 'n/a', 'n/a: '):
            with self.subTest(status=status):
                self.write('.specify/memory/architecture.md', ARCHITECTURE.replace('| undecided |', '| ' + status + ' |'))
                self.assertIn('invalid status', self.assert_check(1))
        for blocking in ('', 'true', 'YES'):
            self.write('.specify/memory/architecture.md', ARCHITECTURE.replace('| no |', '| ' + blocking + ' |'))
            self.assertIn('Blocking', self.assert_check(1))
        for area in AREAS:
            with self.subTest(area=area):
                row = f'| {area} | undecided | - | - | no |\n'
                for text in (ARCHITECTURE.replace(row, ''), ARCHITECTURE + row):
                    self.write('.specify/memory/architecture.md', text)
                    self.assertIn('14 required areas', self.assert_check(1))

    def test_delivery_escaped_pipes_and_malformed_rows(self):
        self.write('.specify/memory/architecture.md', ARCHITECTURE.replace('| - | - | no |', r'| Rule | `false \| cat` | no |'))
        self.assert_check(0)
        self.write('.specify/memory/architecture.md', ARCHITECTURE.replace('| - | - | no |', '| Rule | `false | cat` | no |'))
        self.assertIn('malformed table row', self.assert_check(1))

    def test_typed_memory_decisions_and_wrong_home_ids(self):
        stack = '\n| Area | Choice | Decision |\n|---|---|---|\n| runtime | Python | D-002 |\n'
        self.write('.specify/memory/architecture.md', ARCHITECTURE + stack)
        self.assertIn('not accepted', self.assert_check(1))
        self.write('.specify/memory/architecture.md', ARCHITECTURE)
        self.write('.specify/memory/decisions.md', DECISIONS.replace('Python |', 'PR-999 rejected in D-002 |'))
        self.assert_check(0)
        self.write('.specify/memory/product.md', PRODUCT.replace('| PR-001 | Private', '| AR-002 | Private'))
        self.assertIn('invalid ID AR-002', self.assert_check(1))

    def test_invalid_citation_and_supersession_target(self):
        self.write(self.feature + '/plan.md', PLAN.replace('AR-001', 'AR-01'))
        self.assertIn('invalid citation', self.assert_check(1))
        self.write(self.feature + '/plan.md', PLAN)
        for target in ('D-999', 'D-001'):
            self.write('.specify/memory/decisions.md', DECISIONS.replace('| accepted |', '| superseded by ' + target + ' |'))
            self.assertIn('invalid decision status', self.assert_check(1))


if __name__ == '__main__':
    unittest.main()
