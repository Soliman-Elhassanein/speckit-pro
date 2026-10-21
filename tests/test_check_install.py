"""Exercise the real checker's embedded Python against offline install layouts."""
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CHECK = (ROOT / 'scripts/check-install.sh').read_text().split("<<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]


class UpgradeCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / 'project with spaces'
        self.project.mkdir()
        self.bin = Path(self.tmp.name) / 'bin'
        self.bin.mkdir()
        cli = self.bin / 'specify'
        cli.write_text('#!/bin/sh\nprintf \'%s\\n\' \'{"default_integration":"codex","installed_integrations":["codex"]}\'\n')
        cli.chmod(0o755)
        for path in (ROOT / 'extension/templates').glob('*.md'):
            self.write('.specify/extensions/baseline/templates/' + path.name, path.read_text())
        self.write('.specify/extensions/baseline/scripts/baseline_check.py',
                   (ROOT / 'extension/scripts/baseline_check.py').read_text())
        self.write('.specify/extensions/git/git-config.yml',
                   'branch_template: "feature/{number}-{slug}"\nbranch_prefix: ""\ncommit_style: conventional\n')
        self.write('.specify/extensions/git/scripts/python/create_new_feature_branch.py',
                   'print(\'{"BRANCH_NAME": "feature/001-install-check"}\')\n')
        self.write('.specify/extensions.yml', 'after_specify: speckit.baseline.branch\n')
        for path in (ROOT / 'preset/templates').glob('*.md'):
            self.write('.specify/resolved/' + path.name, path.read_text() + '\n' + 'upstream content\n' * 20)
            # Installed files need not contain the append; resolution owns composition.
            self.write('.specify/templates/' + path.name, 'uncomposed upstream\n')
        self.write('.specify/scripts/bash/resolve-template.sh', 'cat ".specify/resolved/$1.md"\n')

    def write(self, name, text):
        path = self.project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def commands(self, layout):
        for path in (ROOT / 'preset/commands').glob('*.md'):
            text = path.read_text().split('---', 2)[2].replace('{CORE_TEMPLATE}', 'upstream content\n' * 20)
            self.command(path.stem, text, layout)
        for name in ('checklist', 'taskstoissues'):
            self.command('speckit.' + name, 'upstream command', layout)
        for path in (ROOT / 'extension/commands').glob('*.md'):
            self.command(path.stem, path.read_text(), layout)
        for name in ('feature', 'validate', 'commit', 'initialize', 'remote'):
            self.command('speckit.git.' + name, 'upstream git command', layout)

    def command(self, name, text, layout):
        if layout == 'skills':
            target = '.agents/skills/' + name.replace('.', '-') + '/SKILL.md'
        elif layout == 'commands':
            target = '.claude/commands/nested/' + name + '.md'
        else:
            target = '.specify/presets/universal-profile/.composed/' + name + '.md'
        if layout == 'skills':
            text = ('---\nname: ' + name.replace('.', '-') + '\ndescription: command\n'
                    'compatibility: Spec Kit\nmetadata:\n  source: upstream\n---\n' + text)
        path = self.write(target, text)
        if layout == 'skills':
            link = self.project / '.claude/skills'
            link.parent.mkdir(parents=True, exist_ok=True)
            if not link.is_symlink():
                link.symlink_to('../.agents/skills', target_is_directory=True)
        return path

    def run_check(self):
        return subprocess.run([sys.executable, '-c', CHECK, str(ROOT), str(self.project)],
                              capture_output=True, text=True,
                              env=dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH']))

    def test_shared_skills_and_links_with_resolved_templates(self):
        self.commands('skills')
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('PASS type/ticket override command', result.stdout)
        self.assertIn('PASS commit convention composed', result.stdout)
        self.assertIn('PASS shared rule speckit.plan', result.stdout)
        self.assertIn('PASS shared rule speckit.converge', result.stdout)

    def test_copied_claude_skills_are_rejected(self):
        self.commands('skills')
        link = self.project / '.claude/skills'
        text = (link / 'speckit-plan/SKILL.md').read_text()
        link.unlink()
        (link / 'speckit-plan').mkdir(parents=True)
        (link / 'speckit-plan/SKILL.md').write_text(text)
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FAIL Claude skills folder link', result.stdout)

    def test_old_command_and_composed_layouts_are_not_shared_skills(self):
        for layout in ('commands', 'composed'):
            self.commands(layout)
            result = self.run_check()
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('FAIL wrap speckit.plan', result.stdout)

    def test_missing_standard_metadata_is_rejected(self):
        self.commands('skills')
        skill = self.project / '.agents/skills/speckit-plan/SKILL.md'
        skill.write_text(skill.read_text().replace('compatibility: Spec Kit\n', ''))
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FAIL standard skill metadata plan', result.stdout)

    def test_missing_extension_skill_is_rejected(self):
        self.commands('skills')
        (self.project / '.agents/skills/speckit-git-commit/SKILL.md').unlink()
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FAIL git command commit', result.stdout)

    def test_component_sources_alone_do_not_prove_composition(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL wrap speckit.plan', result.stdout)
        self.assertIn('FAIL type/ticket override command', result.stdout)
        self.assertIn('FAIL commit convention composed', result.stdout)

    def test_missing_resolved_append_fails_even_if_static_template_has_it(self):
        self.commands('skills')
        template = ROOT / 'preset/templates/plan-template.md'
        self.write('.specify/templates/plan-template.md', template.read_text())
        self.write('.specify/resolved/plan-template.md', 'upstream content only\n' * 20)
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL template plan-template', result.stdout)

    def test_resolver_failure_is_not_a_passing_template(self):
        self.commands('skills')
        self.write('.specify/scripts/bash/resolve-template.sh', 'exit 1\n')
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertIn('FAIL template plan-template', result.stdout)


if __name__ == '__main__':
    unittest.main()
