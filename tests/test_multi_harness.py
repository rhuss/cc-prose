import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'prose/scripts/init_style_config.py'


def load_resolver():
    spec = importlib.util.spec_from_file_location('style_paths', ROOT / 'prose/scripts/resolve_style_config.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.resolve_paths


class StylePathsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.project = Path(self.temp.name) / 'project'
        self.project.mkdir()
        self.home.mkdir()

    def put(self, path, content='fixture'):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return str(path.resolve())

    def test_empty_sources_do_not_create_files(self):
        before = list(Path(self.temp.name).rglob('*'))
        self.assertEqual(load_resolver()(self.project, self.home), {
            'global_config': {}, 'project_config': {}, 'project_voice': None, 'voices': {}})
        self.assertEqual(before, list(Path(self.temp.name).rglob('*')))

    def test_config_layers_and_directory_fallback(self):
        legacy = self.put(self.home / '.claude/copyedit/config/stoplist.txt')
        project = self.put(self.project / '.copyedit/wordlist.txt')
        result = load_resolver()(self.project, self.home)
        self.assertEqual(result['global_config'], {'stoplist.txt': legacy})
        self.assertEqual(result['project_config'], {'wordlist.txt': project})
        preferred = self.put(self.home / '.claude/style/config.yaml')
        local = self.put(self.project / '.style/config.yaml')
        result = load_resolver()(self.project, self.home)
        self.assertEqual(result['global_config'], {'config.yaml': preferred})
        self.assertEqual(result['project_config'], {'config.yaml': local})

    def test_profile_precedence_and_legacy_only_names(self):
        self.put(self.home / '.claude/prose/voices/shared.yaml', 'old')
        old = self.put(self.home / '.claude/prose/voices/legacy.yaml')
        new = self.put(self.home / '.claude/style/voices/shared.yaml', 'new')
        self.put(self.project / '.prose/voice.yaml', 'old')
        project = self.put(self.project / '.style/voice.yaml', 'new')
        result = load_resolver()(self.project, self.home)
        self.assertEqual(result['voices'], {'legacy': old, 'shared': new})
        self.assertEqual(result['project_voice'], project)

    def test_initializer_repeated_stdin_closed_preserves_files(self):
        env = dict(os.environ, HOME=str(self.home))
        for mode, directory in [('--init', self.project / '.style'),
                                ('--init-global', self.home / '.claude/style')]:
            for attempt in range(2):
                run = subprocess.run([sys.executable, str(SCRIPT), mode], cwd=self.project,
                                     env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                if attempt == 0:
                    (directory / 'stoplist.txt').write_bytes(b'preserve exactly\n')
                    (directory / 'wordlist.txt').unlink()
            self.assertEqual((directory / 'stoplist.txt').read_bytes(), b'preserve exactly\n')
            self.assertTrue((directory / 'wordlist.txt').is_file())
        self.assertEqual(len(list((self.home / '.claude/style/voices').glob('*.yaml'))), 8)

    def test_script_symlink_resolves_bundled_templates(self):
        link = self.project / 'init.py'
        link.symlink_to(SCRIPT)
        run = subprocess.run([sys.executable, str(link), '--init-global'], cwd=self.project,
                             env=dict(os.environ, HOME=str(self.home)), capture_output=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertTrue((self.home / '.claude/style/voices/technical.yaml').is_file())

    def test_missing_templates_reports_reinstall_without_writes(self):
        import shutil
        broken = self.project / 'broken/scripts/init_style_config.py'
        broken.parent.mkdir(parents=True)
        shutil.copyfile(SCRIPT, broken)
        run = subprocess.run([sys.executable, str(broken), '--init-global'], cwd=self.project,
                             env=dict(os.environ, HOME=str(self.home)), capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn('Reinstall cc-prose', run.stderr)
        self.assertFalse((self.home / '.claude/style').exists())

    def test_resolver_cli_outside_repository(self):
        expected = self.put(self.home / '.claude/style/stoplist.txt')
        run = subprocess.run([sys.executable, str(ROOT / 'prose/scripts/resolve_style_config.py')],
                             cwd=self.project, env=dict(os.environ, HOME=str(self.home)),
                             capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['global_config']['stoplist.txt'], expected)


class PackagingTests(unittest.TestCase):
    def test_manifest_and_marketplace_sources(self):
        claude = json.loads((ROOT / 'prose/.claude-plugin/plugin.json').read_text())
        codex = json.loads((ROOT / 'prose/.codex-plugin/plugin.json').read_text())
        market = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text())
        self.assertEqual((codex['name'], codex['version']), (claude['name'], claude['version']))
        self.assertEqual(codex['skills'], './skills/')
        self.assertEqual(market['plugins'][0]['source']['path'], './prose')
        self.assertEqual(json.loads((ROOT / 'package.json').read_text())['version'], codex['version'])

    def test_six_thin_wrappers_delegate_to_existing_commands(self):
        for action in ('write', 'rewrite', 'voice', 'check', 'init', 'update-humanizer'):
            skill = ROOT / 'prose/skills' / action / 'SKILL.md'
            text = skill.read_text()
            self.assertIn(f'name: {action}', text)
            self.assertIn(f'../../commands/{action}.md', text)
            self.assertTrue((skill.parent / f'../../commands/{action}.md').resolve().is_file())
            self.assertLess(len(text.splitlines()), 20)

    def test_all_skills_load_common_guide(self):
        for skill in (ROOT / 'prose/skills').glob('*/SKILL.md'):
            text = skill.read_text()
            self.assertIn('../../docs/harnesses.md', text, str(skill))
            self.assertTrue((skill.parent / '../../docs/harnesses.md').resolve().is_file())
        guide = (ROOT / 'prose/docs/harnesses.md').read_text()
        self.assertIn('resolve_style_config.py', guide)
        self.assertIn('~/.claude/style/', guide)

    def test_maintenance_does_not_require_claude_copy_or_env(self):
        tracking = json.loads((ROOT / 'prose/.humanizer-sync').read_text())
        self.assertNotIn('canonical_file', tracking['modified_skills'][0])
        sync = (ROOT / 'prose/commands/update-humanizer.md').read_text()
        self.assertIn('writable cc-prose checkout', sync)
        self.assertNotIn('cp prose/skills/humanizer', sync)
        self.assertIn('--dry-run', sync)
        self.assertIn('including initial-baseline creation', sync)
        self.assertIn('Harness portability', [a['section'] for a in tracking['modified_skills'][0]['local_additions']])
        self.assertIn('local_additions', sync)
        self.assertNotIn('$PLUGIN_ROOT', (ROOT / 'prose/commands/init.md').read_text())


if __name__ == '__main__':
    unittest.main()
