# cc-prose Plugin

Claude Code plugin for proactive content generation with human voice and AI slop prevention.

## PROACTIVE SKILL INVOCATION (READ THIS FIRST)

**CRITICAL:** This plugin's skills are designed to be invoked PROACTIVELY.
You should NOT wait for the user to explicitly ask for them.

**Before generating prose content:**
1. Check if the content-generator skill should be invoked (see trigger conditions below)
2. If yes, invoke `/prose:write` or the content-generator skill BEFORE generating
3. This ensures AI patterns are prevented during generation, not fixed after

**Before editing existing text:**
1. Check if the humanizer skill should be invoked
2. If user's text contains AI patterns, invoke the skill proactively

**The goal:** Invoke skills BEFORE the action, not after the user complains about AI-sounding output.

**Voice mention rule:** Any explicit mention of "voice" in a writing context (e.g., "using our X voice",
"rephrase with Y voice", "write in Z voice") MUST activate a prose skill:
- Editing/rephrasing existing text + voice → **humanizer**
- Creating new content + voice → **content-generator**
- Managing voice profiles (create, list, show) → **voice-architect**

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

## Skill Routing

Skills are invoked PROACTIVELY. Don't wait for explicit requests.
Each skill's SKILL.md contains full trigger conditions in its "When to Activate" section.

| User intent | Skill | Examples |
|-------------|-------|---------|
| Create new content | content-generator | "write a section", "draft a blog post" |
| Edit/rewrite existing text | humanizer | "rewrite this", "polish", "tighten" |
| Check before publishing | pre-validator | "validate", "check for AI patterns" |
| Manage voice profiles | voice-architect | "create voice", "list voices" |
| Extract voice from samples | voice-extractor | "extract voice from docs/" |

**Voice disambiguation:** When a user mentions a voice name alongside an action, route to content-generator (new content) or humanizer (editing), not voice-architect. The voice-architect is only for CRUD operations on profiles themselves.

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
