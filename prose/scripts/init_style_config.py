#!/usr/bin/env python3
"""
Style Configuration Initializer

Creates unified style configuration directories for cc-prose and cc-copyedit plugins.

Usage:
  init_style_config.py --init          # Initialize project configuration (.style/)
  init_style_config.py --init-global   # Initialize global configuration (~/.claude/style/)
"""

import sys
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def get_plugin_root() -> Path:
    """Get the plugin root directory from script location."""
    # scripts/init_style_config.py -> scripts -> prose plugin root
    return Path(__file__).parent.parent


def create_config_yaml(is_global: bool = False) -> str:
    """Generate default config.yaml content."""
    location = "~/.claude/style/" if is_global else ".style/"
    scope = "global (all projects)" if is_global else "project-specific"

    return f"""# Style Configuration
# Location: {location}
# Scope: {scope}
# Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}
#
# Configuration hierarchy:
#   1. Plugin defaults
#   2. Global config (~/.claude/style/)
#   3. Project config (.style/) - highest priority
#
# Thresholds: Project overrides global
# Wordlists/Stoplists: Both active (combined)
# Styleguides: Both enforced (appended)

# Severity threshold for displaying issues
# Options: critical, high, medium, low
severity_threshold: medium

# Style checking thresholds
style:
  # Target sentence length (words)
  target_sentence_length: 15

  # Maximum sentence length before flagging
  max_sentence_length: 40

  # Target active voice percentage
  target_active_voice_pct: 80

  # Maximum passive voice percentage allowed
  passive_voice_threshold: 20

# Consistency settings
consistency:
  # Similarity threshold for duplication detection (0-1)
  duplication_similarity: 0.65

  # Maximum filler word density (percentage)
  filler_word_density_max: 3.0

# Voice profile settings (cc-prose)
voice:
  # Default voice profile to use
  # Set to profile name from ~/.claude/style/voices/ or leave empty
  default_profile: ""
"""


def create_styleguide_md(is_global: bool = False) -> str:
    """Generate default styleguide.md content."""
    scope = "Global" if is_global else "Project-Specific"

    return f"""# {scope} Style Guide

Style rules that apply to {"all projects" if is_global else "this project"}.

## Voice & Tone

- Use active voice (>80% target)
- Address reader as "you" for instructions
- Use "we" for collaborative exploration
- Use contractions naturally (don't, can't, won't)

## Formatting

- One sentence per line (semantic line breaks for AsciiDoc)
- Use straight quotes, not curly quotes
- No em-dash or en-dash characters (rephrase instead)
- Serial comma in lists (a, b, and c)

## Numbers

- Spell out 0-9: "three servers"
- Numerals for 10+: "15 nodes"
- Always numerals for technical values: "5GB", "3.14"
- Numerals for versions: "Python 3.9"

## Technical Conventions

- Capitalize Kubernetes resources: Pod, Service, ConfigMap
- Close up common prefixes: microservices, multicloud, nonblocking
- Define technical terms on first use

## Avoid

- AI vocabulary: delve, leverage, robust, utilize
- Filler phrases: "in order to", "basically", "simply"
- Hedging: "might possibly", "could potentially"
- Promotional language: groundbreaking, revolutionary
"""


def create_wordlist_txt(is_global: bool = False) -> str:
    """Generate default wordlist.txt content."""
    scope = "Global" if is_global else "Project"

    return f"""# {scope} Wordlist
#
# Preferred terminology and spelling for {"all projects" if is_global else "this project"}.
# One term per line. Lines starting with # are comments.
#
# Format examples:
#   Kubernetes (proper capitalization)
#   container image (preferred over "Docker image")
#   Pod (always capitalized - Kubernetes resource)

# Common technical terms
Kubernetes
Docker
ConfigMap
Pod
Service
Deployment
"""


def create_stoplist_txt(is_global: bool = False) -> str:
    """Generate default stoplist.txt content."""
    scope = "Global" if is_global else "Project"

    return f"""# {scope} Stoplist
#
# Words to BLOCK in {"all projects" if is_global else "this project"}.
# Format: word_to_block -> replacement1, replacement2
# Or just: word_to_block (plugin finds replacement)
#
# Comments starting with # are ignored.

# === AI-GENERATED LANGUAGE (Hard Stop) ===
delve -> explore, examine, investigate
foster -> encourage, support, promote
leverage -> use, apply
robust -> reliable, strong, stable
paramount -> critical, essential, key
utilize -> use
meticulous -> careful, thorough
pivotal -> critical, key, important
harness -> use, apply, employ
facilitate -> enable, help, support

# === HEDGING WORDS ===
basically -> (remove entirely)
simply -> (remove or rephrase)
obviously -> (remove - show, don't tell)
actually -> (remove in most cases)

# === FILLER PHRASES ===
# (These are handled by style checks, but can be added here for emphasis)
"""


def init_project_config(project_dir: Path, plugin_root: Path) -> bool:
    """Initialize project configuration in .style/ directory."""
    style_dir = project_dir / ".style"

    # Check for existing directory
    if style_dir.exists():
        print(f"Directory already exists: {style_dir}")
        response = input("Overwrite existing files? [y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            print("Aborted. No files were modified.")
            return False
    else:
        style_dir.mkdir(parents=True, exist_ok=True)

    # Create configuration files
    files_created = []

    # config.yaml
    config_file = style_dir / "config.yaml"
    if not config_file.exists():
        config_file.write_text(create_config_yaml(is_global=False))
        files_created.append("config.yaml")
    else:
        print(f"  Skipped: config.yaml (already exists)")

    # styleguide.md
    styleguide_file = style_dir / "styleguide.md"
    if not styleguide_file.exists():
        styleguide_file.write_text(create_styleguide_md(is_global=False))
        files_created.append("styleguide.md")
    else:
        print(f"  Skipped: styleguide.md (already exists)")

    # wordlist.txt
    wordlist_file = style_dir / "wordlist.txt"
    if not wordlist_file.exists():
        wordlist_file.write_text(create_wordlist_txt(is_global=False))
        files_created.append("wordlist.txt")
    else:
        print(f"  Skipped: wordlist.txt (already exists)")

    # stoplist.txt
    stoplist_file = style_dir / "stoplist.txt"
    if not stoplist_file.exists():
        stoplist_file.write_text(create_stoplist_txt(is_global=False))
        files_created.append("stoplist.txt")
    else:
        print(f"  Skipped: stoplist.txt (already exists)")

    # voice.yaml placeholder
    voice_file = style_dir / "voice.yaml"
    if not voice_file.exists():
        voice_file.write_text("""# Project Voice Profile
#
# Copy a voice template from ~/.claude/style/voices/ and customize here,
# or create a custom profile.
#
# See /prose:voice create for interactive voice profile creation.
#
# Leave this file empty or remove it to use the global default voice.
""")
        files_created.append("voice.yaml")
    else:
        print(f"  Skipped: voice.yaml (already exists)")

    # Report results
    if files_created:
        print(f"\nCreated .style/ directory with:")
        for f in files_created:
            print(f"  - {f}")

    print(f"\nNext steps:")
    print(f"  1. Edit .style/stoplist.txt to add blocked words")
    print(f"  2. Edit .style/wordlist.txt to add preferred terms")
    print(f"  3. Edit .style/styleguide.md for project-specific rules")
    print(f"  4. Optionally configure .style/voice.yaml for voice profile")

    return True


def init_global_config(plugin_root: Path) -> bool:
    """Initialize global configuration in ~/.claude/style/ directory."""
    global_dir = Path.home() / ".claude" / "style"
    voices_dir = global_dir / "voices"

    # Check for existing directory
    if global_dir.exists():
        print(f"Directory already exists: {global_dir}")
        response = input("Overwrite existing files? [y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            print("Aborted. No files were modified.")
            return False
    else:
        global_dir.mkdir(parents=True, exist_ok=True)

    # Create voices subdirectory
    voices_dir.mkdir(parents=True, exist_ok=True)

    files_created = []

    # config.yaml
    config_file = global_dir / "config.yaml"
    if not config_file.exists():
        config_file.write_text(create_config_yaml(is_global=True))
        files_created.append("config.yaml")
    else:
        print(f"  Skipped: config.yaml (already exists)")

    # styleguide.md
    styleguide_file = global_dir / "styleguide.md"
    if not styleguide_file.exists():
        styleguide_file.write_text(create_styleguide_md(is_global=True))
        files_created.append("styleguide.md")
    else:
        print(f"  Skipped: styleguide.md (already exists)")

    # wordlist.txt
    wordlist_file = global_dir / "wordlist.txt"
    if not wordlist_file.exists():
        wordlist_file.write_text(create_wordlist_txt(is_global=True))
        files_created.append("wordlist.txt")
    else:
        print(f"  Skipped: wordlist.txt (already exists)")

    # stoplist.txt
    stoplist_file = global_dir / "stoplist.txt"
    if not stoplist_file.exists():
        stoplist_file.write_text(create_stoplist_txt(is_global=True))
        files_created.append("stoplist.txt")
    else:
        print(f"  Skipped: stoplist.txt (already exists)")

    # Copy voice templates
    templates_dir = plugin_root / "knowledge-base" / "voice-templates"
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.yaml"):
            dest_file = voices_dir / template_file.name
            if not dest_file.exists():
                shutil.copy(template_file, dest_file)
                files_created.append(f"voices/{template_file.name}")
            else:
                print(f"  Skipped: voices/{template_file.name} (already exists)")

    # Report results
    if files_created:
        print(f"\nCreated ~/.claude/style/ directory with:")
        for f in files_created:
            print(f"  - {f}")

    print(f"\nGlobal configuration initialized at: {global_dir}")
    print(f"\nNext steps:")
    print(f"  1. Edit ~/.claude/style/stoplist.txt for your personal blocked words")
    print(f"  2. Edit ~/.claude/style/wordlist.txt for your preferred terms")
    print(f"  3. Edit ~/.claude/style/styleguide.md for your personal style rules")
    print(f"  4. Customize voice profiles in ~/.claude/style/voices/")
    print(f"\nThese settings apply to ALL projects by default.")
    print(f"Create project-specific .style/ directories to override per-project.")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: init_style_config.py --init | --init-global")
        print("")
        print("Options:")
        print("  --init         Create .style/ in current directory")
        print("  --init-global  Create ~/.claude/style/ for all projects")
        sys.exit(1)

    mode = sys.argv[1]
    plugin_root = get_plugin_root()

    if mode == "--init":
        project_dir = Path.cwd()
        success = init_project_config(project_dir, plugin_root)
        sys.exit(0 if success else 1)

    elif mode == "--init-global":
        success = init_global_config(plugin_root)
        sys.exit(0 if success else 1)

    else:
        print(f"Unknown option: {mode}")
        print("Usage: init_style_config.py --init | --init-global")
        sys.exit(1)


if __name__ == "__main__":
    main()
