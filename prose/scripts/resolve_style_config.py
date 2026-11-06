#!/usr/bin/env python3
"""Report existing shared style sources; never read YAML values or write files."""
import argparse
import json
from pathlib import Path

CONFIG_FILES = ('config.yaml', 'styleguide.md', 'wordlist.txt', 'stoplist.txt')


def resolve_paths(project_dir: Path, home: Path) -> dict:
    project_dir, home = project_dir.resolve(), home.resolve()
    global_dir = home / '.claude/style'
    legacy_global = home / '.claude/copyedit/config'
    project_config = project_dir / '.style'
    legacy_project = project_dir / '.copyedit'

    def config_sources(preferred, legacy):
        selected = preferred if preferred.is_dir() else legacy
        result = {name: str((selected / name).resolve())
                  for name in CONFIG_FILES if (selected / name).is_file()}
        if selected == legacy and (legacy / 'defaults.yaml').is_file():
            result['config.yaml'] = str((legacy / 'defaults.yaml').resolve())
        return result

    voices = {}
    for directory in (home / '.claude/prose/voices', global_dir / 'voices'):
        for voice in directory.glob('*.yaml'):
            if voice.is_file():
                voices[voice.stem] = str(voice.resolve())
    project_voice = next((str(path.resolve()) for path in (
        project_dir / '.style/voice.yaml', project_dir / '.prose/voice.yaml') if path.is_file()), None)
    return {'global_config': config_sources(global_dir, legacy_global),
            'project_config': config_sources(project_config, legacy_project),
            'project_voice': project_voice, 'voices': dict(sorted(voices.items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-dir', type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(resolve_paths(args.project_dir, Path.home()), indent=2))


if __name__ == '__main__':
    main()
