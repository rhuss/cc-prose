---
name: init
description: Initialize style configuration for project or global use
user-invocable: true
argument: optional_flags
---

# /prose:init - Initialize Style Configuration

Create unified style configuration directories for prose and copyedit plugins.

## Usage

```
/prose:init              # Initialize .style/ in current project
/prose:init --global     # Initialize ~/.claude/style/ for all projects
```

## What This Creates

### Project Configuration (.style/)

Running `/prose:init` creates:

```
.style/
├── config.yaml      # Style thresholds and settings
├── styleguide.md    # Project-specific style rules
├── wordlist.txt     # Preferred terminology
├── stoplist.txt     # Forbidden words
└── voice.yaml       # Project voice profile (optional)
```

### Global Configuration (~/.claude/style/)

Running `/prose:init --global` creates:

```
~/.claude/style/
├── config.yaml      # Global thresholds
├── styleguide.md    # Personal style rules
├── wordlist.txt     # Your preferred terms
├── stoplist.txt     # Words you never use
└── voices/          # Voice profile library
    ├── technical.yaml
    └── conversational.yaml
```

## Configuration Hierarchy

```
Plugin defaults (built-in)
    ↓ overridden by
Global config (~/.claude/style/)
    ↓ overridden by
Project config (.style/)
```

**Merge behavior:**
- **Thresholds**: Project overrides global
- **Wordlists**: Both combined (all terms active)
- **Stoplists**: Both combined (all words blocked)
- **Styleguides**: Both enforced (rules appended)
- **Voice**: Project voice takes precedence

## Backward Compatibility

Both cc-prose and cc-copyedit plugins support legacy paths:

| New Path | Legacy Fallback |
|----------|-----------------|
| `.style/` | `.copyedit/`, `.prose/` |
| `~/.claude/style/` | `~/.claude/copyedit/config/`, `~/.claude/prose/` |

Existing configurations continue to work. New configurations should use the unified paths.

## Examples

**Initialize project configuration:**
```
/prose:init
```

Output:
```
Created .style/ directory with:
  - config.yaml
  - styleguide.md
  - wordlist.txt
  - stoplist.txt
  - voice.yaml

Next steps:
  1. Edit .style/stoplist.txt to add blocked words
  2. Edit .style/wordlist.txt to add preferred terms
  3. Edit .style/styleguide.md for project-specific rules
```

**Initialize global configuration:**
```
/prose:init --global
```

Output:
```
Created ~/.claude/style/ directory with:
  - config.yaml
  - styleguide.md
  - wordlist.txt
  - stoplist.txt
  - voices/technical.yaml
  - voices/conversational.yaml

These settings apply to ALL projects by default.
```

## Implementation

When this command is invoked:

1. Parse the argument to detect `--global` flag
2. Run the initialization script:

```bash
# For project initialization
python3 "$PLUGIN_ROOT/scripts/init_style_config.py" --init

# For global initialization
python3 "$PLUGIN_ROOT/scripts/init_style_config.py" --init-global
```

3. Report created files to the user
4. Provide next steps guidance

## Notes

- Existing files are NOT overwritten (skipped with message)
- Global initialization copies voice templates from the plugin
- Both prose and copyedit plugins read from the same unified paths
