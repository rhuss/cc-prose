# cc-prose Plugin

Claude Code plugin for proactive content generation with human voice and AI slop prevention.

## Project Overview

This plugin provides writing assistance focused on:
- Content generation with human voice (automatic activation)
- AI pattern prevention (24 humanizer categories)
- Voice profile management for consistent personality
- Pre-submission validation

## Separation from Copyedit

This plugin complements cc-copyedit with clear separation:

| Plugin | Purpose | Focus |
|--------|---------|-------|
| **copyedit** | Review and fix existing content | Editing |
| **prose** | Generate new content with human voice | Creation |

The content-generator skill in this plugin supersedes copyedit's content-writer.
Copyedit should focus on its core mission: editing, not content creation.

## Directory Structure

```
cc-prose/
+-- .claude-plugin/marketplace.json    # Root marketplace pointing to ./prose
+-- prose/                             # Main plugin directory
|   +-- .claude-plugin/plugin.json     # Plugin manifest
|   +-- .claude/settings.local.json    # Permissions
|   +-- commands/                      # Thin command wrappers
|   +-- skills/                        # Detailed skill workflows
|   +-- knowledge-base/                # Voice templates
|   +-- docs/                          # Documentation
+-- Makefile                           # Development automation
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `/prose:write` | Generate content with style rules |
| `/prose:rewrite` | Humanize existing text |
| `/prose:voice` | Manage voice profiles |
| `/prose:check` | Pre-submission validation |

## Skills

### content-generator
**Activates automatically** when user requests content creation or uses keywords like
"with human voice", "publication-ready", "following our styleguide".

Generates new content following all rules:
- Loads copyedit configuration (global + project)
- Applies voice profile
- Enforces humanizer patterns during generation
- Self-validates before output

### humanizer
Removes AI writing patterns using 24 categories:
- Content patterns (significance inflation, promotional)
- Language patterns (AI vocabulary, copula avoidance)
- Style patterns (em dash, curly quotes)
- Communication patterns (chatbot artifacts)
- Filler and hedging

Synced from `~/.claude/skills/humanizer/SKILL.md`.

### voice-architect
Manages voice profiles:
- Create profiles interactively
- Apply profiles to content
- List available profiles
- Profile schema: formality, personality, pronouns, patterns

### pre-validator
Final validation before submission:
- AI pattern scan
- Stoplist word check
- Style compliance
- Flow quality
- Consistency check
- Voice consistency
- Readability metrics

## Configuration Integration

Shares configuration with cc-copyedit plugin (read-only):
- `~/.claude/copyedit/config/` - Global config
- `.copyedit/` - Project config

Prose-specific additions:
- `~/.claude/prose/voices/` - Global voice profiles
- `.prose/voice.yaml` - Project voice profile

## Development

```bash
make validate       # Validate plugin structure
make install        # Install plugin
make uninstall      # Remove plugin
make reinstall      # Full reinstall
make sync-humanizer # Update humanizer from source
```

## Humanizer Source

The humanizer skill is maintained at `~/.claude/skills/humanizer/SKILL.md`.
This is the canonical source based on Wikipedia's "Signs of AI writing" guide.

To update the plugin's humanizer:
```bash
make sync-humanizer
make reinstall
```

## Voice Templates

Built-in templates in `prose/knowledge-base/voice-templates/`:
- `technical.yaml` - Professional, balanced (0.6 formality, 0.6 personality)
- `conversational.yaml` - Casual, engaging (0.4 formality, 0.8 personality)

## Key Principles

1. **Prevention over correction**: Generate clean content, don't fix after
2. **Humanizer patterns authority**: All 24 categories forbidden by default
3. **Stoplist supremacy**: Constitutional rule, overrides everything
4. **Voice consistency**: Personality maintained throughout
5. **Self-validation**: Content checked before output
