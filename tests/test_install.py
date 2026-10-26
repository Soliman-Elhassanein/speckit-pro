"""Offline checks of the retained CLI delegation, not upstream installation."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.target = self.root / 'project with spaces'
        self.target.mkdir()
        (self.target / '.specify/memory').mkdir(parents=True)
        self.memory = self.target / '.specify/memory/product.md'
        self.memory.write_text('approved product')
        self.custom = self.target / '.specify/extensions.yml'
        self.custom.write_text('foreign hook configuration')
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.cli = self.bin / 'specify'
        self.cli.write_text('''#!/usr/bin/python3
import json
import os
from pathlib import Path
import sys
args = sys.argv[1:]
with open(os.environ['INSTALL_CALLS'], 'a') as out:
    out.write(' '.join(args) + '\\n')
if args[0] == os.environ['FAIL_STEP'] and args[1] != 'list':
    sys.exit(1)
statefile = Path('.specify/mock-state.json')
state = json.loads(statefile.read_text()) if statefile.exists() else {
    'default_integration': 'codex', 'installed_integrations': ['codex']}
if args[:3] == ['integration', 'status', '--json']:
    print(json.dumps(state))
elif args[:2] == ['integration', 'switch']:
    old = state['default_integration']
    state = {'default_integration': args[2],
             'installed_integrations': [k for k in state['installed_integrations'] if k != old] + [args[2]]}
elif args[:2] == ['integration', 'use']:
    state['default_integration'] = args[2]
elif args[:2] == ['integration', 'uninstall']:
    state['installed_integrations'].remove(args[2])
statefile.write_text(json.dumps(state))
extensions_file = Path('.specify/mock-extensions.json')
extensions = json.loads(extensions_file.read_text()) if extensions_file.exists() else []
if args == ['extension', 'list', '--json']:
    print(json.dumps([{'id': name} for name in extensions]))
if args[:2] == ['extension', 'add']:
    name = 'baseline' if '--dev' in args else args[2]
    if name in extensions and '--force' not in args:
        sys.exit('Extension already installed')
    if name not in extensions:
        extensions.append(name)
    extensions_file.write_text(json.dumps(extensions))
if args == ['extension', 'add', 'git']:
    config = Path('.specify/extensions/git/git-config.yml')
    config.parent.mkdir(parents=True, exist_ok=True)
    if not config.exists():
        config.write_text('branch_template: ""\\nbranch_prefix: "custom"\\ncommit_style: fixed\\nforeign: kept\\n')
    script = Path('.specify/extensions/git/scripts/python/initialize_repo.py')
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text("import subprocess\\nfrom pathlib import Path\\n"
                      "subprocess.run(['git', 'init', '-q'], check=True)\\n"
                      "Path('.specify/init-called').write_text('1')\\n")
presets_file = Path('.specify/mock-presets.json')
presets = json.loads(presets_file.read_text()) if presets_file.exists() else []
if args == ['preset', 'list', '--json']:
    print(json.dumps([{'id': name} for name in presets]))
if args[:2] == ['preset', 'add']:
    if presets:
        sys.exit('Preset already installed')
    presets_file.write_text(json.dumps(['universal-profile']))
if args[:2] in (['preset', 'add'], ['preset', 'update']):
    for name in ('plan', 'converge', 'baseline-context', 'git-commit'):
        skill = Path('.agents/skills/speckit-' + name)
        skill.mkdir(parents=True, exist_ok=True)
        (skill / 'SKILL.md').write_text('rendered skill')
''')
        self.cli.chmod(0o755)
        self.calls = self.root / 'calls'

    def install(self, *args, fail=''):
        env = dict(os.environ, PATH=str(self.bin) + ':/usr/bin:/bin',
                   INSTALL_CALLS=str(self.calls), FAIL_STEP=fail)
        return subprocess.run(['sh', str(ROOT / 'install.sh'), *args, str(self.target)],
                              text=True, capture_output=True, env=env)

    def mutation_calls(self):
        return [line for line in self.calls.read_text().splitlines()
                if line not in ('integration status --json', 'extension list --json', 'preset list --json')]

    def test_delegates_without_touching_memory_or_hooks(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.mutation_calls(), [
            'extension add git',
            'extension add --dev ' + str(ROOT / 'extension'),
            'preset add --dev ' + str(ROOT / 'preset')])
        self.assertEqual(self.memory.read_text(), 'approved product')
        self.assertEqual(self.custom.read_text(), 'foreign hook configuration')

    def test_git_settings_preserve_unrelated_values_and_repeat_cleanly(self):
        self.assertEqual(self.install().returncode, 0)
        config = self.target / '.specify/extensions/git/git-config.yml'
        text = config.read_text()
        self.assertIn('branch_template: "feature/{number}-{slug}"', text)
        self.assertIn('branch_prefix: ""', text)
        self.assertIn('commit_style: conventional', text)
        self.assertIn('foreign: kept', text)
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual(config.read_text(), text)
        self.assertEqual(self.mutation_calls().count('extension add git'), 1)

    def test_new_folder_becomes_a_repository_through_upstream_script(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.target / '.git').exists())
        self.assertEqual((self.target / '.specify/init-called').read_text(), '1')

    def test_existing_repository_is_left_alone(self):
        subprocess.run(['git', 'init', '-q', str(self.target)], check=True)
        self.assertEqual(self.install().returncode, 0)
        self.assertFalse((self.target / '.specify/init-called').exists())

    def test_extension_failure_stops_before_preset(self):
        result = self.install(fail='extension')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(len(self.mutation_calls()), 1)

    def test_preset_failure_is_reported(self):
        self.assertEqual(self.install(fail='preset').returncode, 1)

    def test_force_delegates_extension_update(self):
        self.assertEqual(self.install('--force').returncode, 0)
        self.assertIn('--force', self.mutation_calls()[1])

    def test_force_updates_existing_components_through_cli(self):
        self.assertEqual(self.install('--agents', 'claude').returncode, 0)
        result = self.install('--force', '--agents', 'claude')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('preset update universal-profile --dev ' + str(ROOT / 'preset'),
                      self.mutation_calls())
        self.assertEqual(self.mutation_calls().count('extension add git'), 1)

    def test_cli_missing_gives_exact_fix_without_mutation(self):
        self.cli.unlink()
        result = self.install()
        self.assertEqual(result.returncode, 1)
        self.assertIn('uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.2', result.stderr)
        self.assertFalse(self.calls.exists())
        self.assertEqual(self.memory.read_text(), 'approved product')

    def test_project_must_be_initialized(self):
        (self.target / '.specify').rename(self.target / 'saved')
        result = self.install()
        self.assertEqual(result.returncode, 1)
        self.assertIn('specify init', result.stderr)
        self.assertFalse(self.calls.exists())

    def test_migrates_another_default_and_removes_secondary_integrations(self):
        import json
        state = self.target / '.specify/mock-state.json'
        state.write_text(json.dumps({'default_integration': 'claude',
                                    'installed_integrations': ['claude', 'gemini']}))
        result = self.install('--agents', 'claude')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Current default integration: claude', result.stdout)
        self.assertEqual(self.mutation_calls()[:2],
                         ['integration switch codex', 'integration uninstall gemini'])
        self.assertEqual(json.loads(state.read_text())['installed_integrations'], ['codex'])

    def test_selects_existing_codex_without_reinstalling_it(self):
        import json
        (self.target / '.specify/mock-state.json').write_text(json.dumps({
            'default_integration': 'claude', 'installed_integrations': ['claude', 'codex']}))
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual(self.mutation_calls()[:2],
                         ['integration use codex', 'integration uninstall claude'])

    def test_claude_gets_one_folder_link_to_shared_skills(self):
        folder = self.target / '.claude/skills'
        for _ in range(2):
            result = self.install('--agents', 'claude,codex,gemini,cursor,antigravity')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(folder.is_symlink())
            self.assertEqual(str(folder.readlink()), '../.agents/skills')
            self.assertEqual(folder.resolve(), (self.target / '.agents/skills').resolve())

    def test_earlier_per_skill_links_become_one_folder_link(self):
        folder = self.target / '.claude/skills'
        folder.mkdir(parents=True)
        (folder / 'speckit-plan').symlink_to('../../.agents/skills/speckit-plan')
        result = self.install('--agents', 'claude')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(str(folder.readlink()), '../.agents/skills')

    def test_other_skills_file_or_link_stops_without_replacing(self):
        folder = self.target / '.claude/skills'
        for kind in ('skills', 'file', 'link'):
            with self.subTest(kind=kind):
                folder.parent.mkdir(exist_ok=True)
                if kind == 'skills':
                    (folder / 'personal').mkdir(parents=True)
                    (folder / 'speckit-plan').symlink_to('../../.agents/skills/speckit-plan')
                elif kind == 'file':
                    folder.write_text('keep')
                else:
                    folder.symlink_to('missing')
                result = self.install('--agents', 'claude')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('nothing was overwritten', result.stderr)
                if kind == 'skills':
                    self.assertTrue((folder / 'personal').is_dir())
                    self.assertTrue((folder / 'speckit-plan').is_symlink())
                    (folder / 'speckit-plan').unlink()
                    (folder / 'personal').rmdir()
                    folder.rmdir()
                else:
                    folder.unlink()

    def test_integration_failure_stops_before_components(self):
        self.assertNotEqual(self.install(fail='integration').returncode, 0)
        self.assertEqual(self.mutation_calls(), [])

    def test_invalid_agents_stop_before_cli(self):
        for args in (('--agents', 'unknown'), ('--agents', 'claude,,codex')):
            result = self.install(*args)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(self.calls.exists())


if __name__ == '__main__':
    unittest.main()
