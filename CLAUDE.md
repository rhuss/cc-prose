# cc-prose Plugin

Claude Code plugin for proactive content generation with human voice and AI slop prevention.

## When to Use Prose Skills

Prose skills target **human-readable content meant for people to read**.
Invoke them proactively when the output is prose, don't wait for the user to ask.

**Do NOT activate prose skills for machine-targeted content:**
- Code (source files, scripts, configs)
- Structured data (JSON, YAML, TOML, CSV)
- CLI output, log messages, error strings
- Commit messages, PR descriptions, git metadata
- API docs generated from code (OpenAPI specs, JSDoc)
- Makefiles, Dockerfiles, CI pipeline definitions
- SQL, queries, migration files
- Template literals, interpolation strings
- Comments inside source code

**Do activate for human prose:**
- Blog posts, articles, essays
- Documentation written for humans (guides, tutorials, READMEs)
- Emails, announcements, social media posts
- Slide content, talk abstracts, bios
- Any free-form writing where voice and tone matter

**Before generating prose content**, strongly consider invoking the content-generator skill.
Prevention during generation beats fixing AI patterns after the fact.

**Before editing existing prose**, consider the humanizer if AI patterns are present.

**Voice mention rule:** Any explicit mention of "voice" in a writing context (e.g., "using our X voice",
"rephrase with Y voice", "write in Z voice") activates a prose skill:
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

For human-readable prose, invoke skills proactively rather than waiting for explicit requests.
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
make validate        # Validate plugin structure
make install         # Install plugin
make uninstall       # Remove plugin
make reinstall       # Full reinstall
make check-upstream  # Check for upstream humanizer changes
```

## Humanizer Source

The humanizer skill tracks the upstream [blader/humanizer](https://github.com/blader/humanizer) repository,
based on Wikipedia's "Signs of AI writing" guide. The canonical local copy lives at `~/.claude/skills/humanizer/SKILL.md`.

Sync state is tracked in `prose/.humanizer-sync`, which records the last synced upstream commit
and lists local cc-prose additions that must be preserved during merges.

To check for upstream changes:
```bash
make check-upstream
```

To merge upstream changes (AI-assisted, preserves local additions):
```
/update-humanizer
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

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at `specs/003-inline-voice-matching/plan.md`
<!-- SPECKIT END -->
