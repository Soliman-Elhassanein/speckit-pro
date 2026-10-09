"""Installer rollback probes plus opt-in smoke tests against the pinned real CLI."""
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def tree(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*')
            if p.is_file() and '.git' not in p.relative_to(root).parts}


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / 'package [x]&odd'
        self.package.mkdir()
        for name in ('install.sh', 'scripts', 'preset', 'extension', 'workflow', 'modules', 'template',
                     'speckit-universal-profile.md', 'adoption-prompt.md'):
            source, target = ROOT / name, self.package / name
            if source.is_dir(): shutil.copytree(source, target)
            else: shutil.copy2(source, target)
        self.target = self.root / 'project with spaces'
        self.target.mkdir()
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        cli = self.bin / 'specify'
        cli.write_text('''#!/usr/bin/env python3
import json, os, pathlib, shutil, sys
if '--version' in sys.argv:
    print('specify 1.1.2'); raise SystemExit(0)
a = sys.argv[1:]
kind, action = a[:2]
p = pathlib.Path('.specify')
ids = {'preset': 'universal-profile', 'extension': 'baseline', 'workflow': 'speckit-pro'}
path = p / (kind + 's') / ids[kind]
if action == 'remove':
    shutil.rmtree(path)
else:
    path.mkdir(parents=True, exist_ok=True)
    (path / 'changed').write_text('new')
    if kind == 'workflow':
        (p / 'workflows/workflow-registry.json').write_text(json.dumps({'workflows': {'speckit-pro': {}}}))
if kind == os.environ.get('FAIL_STEP') and action == 'add':
    print('injected ' + kind + ' installation failure', file=sys.stderr)
    raise SystemExit(1)
''')
        cli.chmod(0o755)

    def install(self, *args, real=False, env=None):
        environment = dict(os.environ)
        if not real: environment['PATH'] = str(self.bin) + os.pathsep + environment['PATH']
        environment.update(env or {})
        return subprocess.run([str(self.package / 'install.sh'), *args, str(self.target)],
                              capture_output=True, text=True, env=environment)

    def existing(self):
        for path in ('.specify/presets/universal-profile/old', '.specify/extensions/baseline/old',
                     '.specify/memory/product.md', '.claude/commands/custom.md', '.config/settings',
                     'CLAUDE.md', 'specs/001-real/spec.md', 'src/app.py'):
            p = self.target / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('keep ' + path)

    def test_invalid_package_is_rejected_before_removal(self):
        self.existing()
        before = tree(self.target)
        (self.package / 'preset/preset.yml').write_text('invalid: [')
        result = self.install('--force')
        self.assertEqual(result.returncode, 1)
        self.assertIn('validation failed', result.stderr)
        self.assertEqual(tree(self.target), before)

    def test_failed_preset_extension_and_workflow_restore_previous_install(self):
        self.existing()
        before = tree(self.target)
        for step in ('preset', 'extension', 'workflow'):
            with self.subTest(step=step):
                result = self.install('--force', env={'FAIL_STEP': step})
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('injected ' + step, result.stderr)
                self.assertIn('restored', result.stderr)
                self.assertEqual(tree(self.target), before)

    def test_ready_made_install_without_cli(self):
        (self.bin / 'specify').unlink()
        python = self.bin / 'python3'
        python.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) + ' "$@"\n')
        python.chmod(0o755)
        result = self.install(env={'PATH': str(self.bin) + os.pathsep + '/usr/bin:/bin'})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('ready-made setup', result.stdout)
        self.assertTrue((self.target / '.agents/skills/speckit-implement/SKILL.md').exists())
        self.assertTrue((self.target / '.specify/extensions/baseline/scripts/baseline_store.py').exists())

    @unittest.skipUnless(os.environ.get('SPECKIT_REAL_CLI') == '1', 'set SPECKIT_REAL_CLI=1 for pinned CLI smoke')
    def test_real_cli_codex_claude_and_update_preserve_project(self):
        self.assertIn('1.1.2', subprocess.check_output(['specify', '--version'], text=True))
        for agent in ('codex', 'claude'):
            with self.subTest(agent=agent):
                self.target = self.root / ('real ' + agent)
                self.target.mkdir()
                result = self.install('--agent', agent, real=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((self.target / '.specify/extensions/baseline/scripts/baseline_store.py').is_file())
                self.assertTrue((self.target / '.specify/workflows/speckit-pro/workflow.yml').is_file())
                memory = self.target / '.specify/memory/product.md'
                memory.write_text('existing approved product')
                custom = self.target / '.specify/keep-custom.txt'
                custom.write_text('preserve me')
                result = self.install('--force', real=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(memory.read_text(), 'existing approved product')
                self.assertEqual(custom.read_text(), 'preserve me')
                hooks = (self.target / '.specify/extensions.yml').read_text()
                self.assertIn('priority: 1', hooks)
                self.assertEqual((self.target / '.specify/.gitignore').read_text().count('.baseline-local/'), 1)
