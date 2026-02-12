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

## Skills (Proactive Triggering)

**IMPORTANT FOR CLAUDE:** These skills should be triggered PROACTIVELY without user explicitly asking.
Check the trigger conditions below and invoke the skill BEFORE generating content.

### content-generator
**MANDATORY - ALWAYS INVOKE** when creating ANY prose content:

**Trigger conditions (invoke skill if ANY match):**
- User says "write", "draft", "create", "compose", "generate" + content/text/section/paragraph
- User says "with human voice", "publication-ready", "natural writing"
- User mentions a voice by name when requesting new content (e.g., "using our X voice", "with X voice")
- User says "using voice" or references any named voice profile alongside a content-creation action
- User requests documentation, explanations, blog posts, articles
- You are about to generate more than 2 paragraphs of prose text
- User explicitly requests "following our styleguide"

**What it does:**
- Loads copyedit configuration (global + project)
- Applies voice profile
- Enforces humanizer patterns during generation
- Self-validates before output

### humanizer
**MANDATORY - ALWAYS INVOKE** when editing EXISTING text:

**Trigger conditions (invoke skill if ANY match):**
- User says "humanize", "make natural", "remove AI", "fix AI writing"
- User says "rewrite", "rephrase", "revise", "rework", "polish", "improve the writing", "tighten"
- User says "sounds robotic", "less AI-like", "more authentic"
- User mentions a voice by name when editing text (e.g., "using our X voice", "with X voice", "in X voice")
- User says "using voice" or references any named voice profile alongside a text-editing action
- You notice AI patterns in text you're editing (em dashes, "delve", "crucial", etc.)
- Text contains chatbot artifacts, significance inflation, promotional language

**What it does:**
- Detects 24 categories of AI writing patterns
- Rewrites problematic sections
- Injects personality and voice
- Preserves core meaning

### voice-architect
**INVOKE** when managing writing voice/personality (not when writing/editing with a voice):

**Trigger conditions:**
- User says "create voice profile", "define writing style", "set up voice"
- User says "list voices", "show voice profiles"
- User says "apply voice", "use this voice", "switch voice", "change voice"

**Note:** When a user mentions a voice name alongside a writing/editing action (e.g., "rephrase using X voice"), the humanizer or content-generator should activate instead. This skill is for voice profile management only.

### voice-extractor
**INVOKE** when deriving voice profiles from existing content:

**Trigger conditions (invoke skill if ANY match):**
- User says "extract voice", "derive voice profile", "analyze writing style"
- User says "create voice from this document", "learn my voice from..."
- User says "capture voice from", "derive style from", "extract profile from"
- User provides sample content and wants to capture its voice for reuse
- User wants to replicate an author's writing style from samples

**What it does:**
- Reads files (Markdown, AsciiDoc, PDF) or directories
- Analyzes writing patterns to extract all voice parameters
- Presents findings with confidence scores
- Prompts for profile name
- Saves to `~/.claude/style/voices/{name}.yaml` or `.style/voice.yaml`

### pre-validator
**MANDATORY - ALWAYS INVOKE** before finalizing content:

**Trigger conditions (invoke skill if ANY match):**
- User says "check", "validate", "review for AI", "is this ready"
- User is about to submit, publish, or finalize content
- User asks "does this sound AI-generated?", "any AI patterns?"
- Before committing documentation to version control
- After generating content to verify quality

**What it does:**
- Comprehensive validation report
- Scores for AI patterns, style, flow, voice
- PASS/FAIL recommendation

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
