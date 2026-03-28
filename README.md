# cc-prose

A Claude Code plugin for **proactive content generation** with human voice and AI slop prevention.

## Overview

This plugin helps you write content that sounds authentically human while following all style rules.
It complements the [copyedit plugin](https://github.com/rhuss/cc-copyedit), sharing its configuration but with a clear separation of concerns:

- **copyedit** = Review and fix existing content (editing)
- **prose** = Generate new content with human voice (creation)

**Key features:**

- **Automatic activation**: Activates when you request content creation
- **Voice profiles**: 8 built-in templates plus custom profile creation
- **Voice extraction**: Derive voice profiles from existing writing samples
- **Humanizer depth**: Wikipedia's 24-pattern methodology for authentic writing
- **Proactive guidance**: Pattern prevention during writing (not just post-editing)
- **Easy humanizer updates**: Sync from upstream source with `make sync-humanizer`

> **Note:** If you previously used copyedit's `content-writer` skill, this plugin's `content-generator` supersedes it.
> The copyedit plugin should focus on editing, not content creation.

## Installation

**Via Marketplace (recommended):**

```bash
# Add the marketplace (once)
/plugin marketplace add rhuss/cc-rhuss-marketplace

# Install the plugin
/plugin install prose@cc-rhuss-marketplace
```

**From source:**

```bash
git clone https://github.com/rhuss/cc-prose.git
cd cc-prose
make install

# Verify installation
claude plugin list
```

## Commands

| Command | Description |
|---------|-------------|
| `/prose:write <topic>` | Generate content on a topic |
| `/prose:rewrite <file>` | Humanize existing text |
| `/prose:voice [create\|apply\|list]` | Manage voice profiles |
| `/prose:check <file>` | Pre-submission validation |
| `/prose:init [--global]` | Initialize style configuration |

## Quick Start

### Generate Content

The content-generator skill activates **automatically** when you request content creation:

```bash
# Just ask naturally - the skill activates automatically
Write a section about Kubernetes Services with human voice

# Or use the explicit command
/prose:write a section explaining how Kubernetes Services work

# Write using a specific voice
/prose:write an intro to container networking using the tutorial voice
```

The content-generator will:
1. Load your copyedit configuration
2. Apply your active voice profile
3. Generate content following all style rules
4. Validate against humanizer patterns
5. Present publication-ready text

### Humanize Existing Text

The humanizer detects and removes AI writing patterns from existing text. It works across 24 categories of AI-specific patterns, from vocabulary choices ("delve", "leverage") to structural habits (significance inflation, promotional language, excessive hedging).

```bash
# Rewrite a file to remove AI patterns
/prose:rewrite docs/chapter03.md

# Rewrite with a specific voice applied
/prose:rewrite docs/intro.md using the conversational voice

# Or just describe what you need
Tighten up the writing in docs/overview.md, it sounds too robotic
```

The humanizer operates in two modes:

- **Reactive**: Cleans up existing AI-sounding text on demand
- **Proactive**: The content-generator invokes the humanizer's rules during generation, so AI patterns never appear in the first place

### Create a Voice Profile

```bash
# Create a new voice profile interactively
/prose:voice create technical-friendly

# List available voice profiles
/prose:voice list

# Apply a voice to the current project
/prose:voice apply narrative
```

You'll be prompted for:
- Formality level (casual to formal)
- Personality level (neutral to opinionated)
- Pronoun preferences (you vs we)
- Contractions usage

### Extract a Voice from Existing Writing

The voice-extractor analyzes writing samples and derives a reusable voice profile from them:

```bash
# Extract voice from a single document
Extract a voice profile from docs/best-practices.md

# Extract from a directory of samples
Derive a voice from all the posts in content/blog/

# Create a named profile from an author's writing
Learn my voice from ~/writing-samples/ and save it as "my-style"
```

The extractor reads Markdown, AsciiDoc, and PDF files, analyzing sentence structure, vocabulary choices, formality level, and personality markers. For multi-file corpora, it performs incremental analysis and presents aggregate confidence scores before saving.

### Validate Before Submission

```bash
# Run comprehensive validation
/prose:check docs/chapter03.md
```

The pre-validator checks:
- AI pattern scan (24 categories)
- Stoplist word check
- Style compliance
- Flow quality
- Consistency
- Voice consistency
- Readability metrics

### Initialize Configuration

```bash
# Set up project-level style configuration
/prose:init

# Set up global configuration (applies to all projects)
/prose:init --global
```

This creates a `.style/` directory with `config.yaml`, `styleguide.md`, `wordlist.txt`, `stoplist.txt`, and `voice.yaml`. Both cc-prose and cc-copyedit read from the same unified paths.

## Voice Profiles

Voice profiles define consistent personality characteristics for your writing.

### Built-in Templates

| Profile | Formality | Personality | Best For |
|---------|-----------|-------------|----------|
| `technical` | 0.6 (balanced) | 0.6 (engaged) | API docs, architecture guides |
| `conversational` | 0.4 (casual) | 0.8 (opinionated) | Tutorials, blog posts, READMEs |
| `analytical` | 0.7 (formal-leaning) | 0.4 (measured) | Benchmarks, research findings, performance reports |
| `narrative` | 0.4 (casual) | 0.8 (personal) | Post-mortems, case studies, conference talks |
| `pov` | 0.5 (moderate) | 0.9 (strongly opinionated) | Op-eds, ADRs, position papers |
| `reasoning` | 0.6 (balanced) | 0.7 (thoughtful) | RFCs, design proposals, comparison articles |
| `reference` | 0.8 (formal) | 0.2 (neutral) | API reference, man pages, specifications |
| `tutorial` | 0.3 (casual) | 0.7 (encouraging) | Getting started guides, how-to articles, workshops |

**Scale**: 0.0 (casual/neutral) to 1.0 (formal/opinionated)

### Profile Locations

- **Global**: `~/.claude/style/voices/` (available across all projects)
- **Project**: `.style/voice.yaml` (project-specific, overrides global)

### Profile Structure

```yaml
name: "technical-friendly"
characteristics:
  formality: 0.6
  personality: 0.7
  first_person: true
  contractions: true
sentence_patterns:
  mix_short: true
  max_consecutive_similar: 3
personality_traits:
  opinions: true
  acknowledge_complexity: true
  humor: "subtle"
```

## AI Pattern Prevention (Humanizer)

The humanizer enforces Wikipedia's 24 AI writing pattern categories. It works as both a standalone rewriting tool and as an integrated layer inside the content-generator.

### How It Works

Every pattern belongs to a severity tier that determines enforcement:

### CRITICAL (never appear)
- Chatbot artifacts ("I hope this helps")
- Knowledge cutoff disclaimers

### HIGH (strongly avoid)
- AI vocabulary (delve, leverage, robust)
- Significance inflation ("is a testament")
- Promotional language ("groundbreaking")
- Superficial -ing analyses

### MEDIUM (should avoid)
- Filler phrases ("in order to")
- Excessive hedging
- Copula avoidance ("serves as")

### LOW (optional)
- Rule of three overuse
- Boldface overuse

### Stoplist

The stoplist is a constitutional rule: words on it never appear in output, regardless of context or voice. Stoplists cascade (global + project are combined). Edit your stoplist at `.style/stoplist.txt` or `~/.claude/style/stoplist.txt`.

## Configuration

This plugin shares configuration with the copyedit plugin:

- `~/.claude/style/` - Global settings (unified path)
- `.style/` - Project overrides (unified path)

Legacy paths (`~/.claude/copyedit/config/`, `.copyedit/`, `.prose/`) are still supported as fallbacks.

### Key Configuration Files

| File | Purpose |
|------|---------|
| `stoplist.txt` | Forbidden words (constitutional rule) |
| `wordlist.txt` | Preferred terminology |
| `styleguide.md` | Prose style rules |
| `config.yaml` | Thresholds and settings |

## Humanizer Updates

The humanizer skill is sourced from `~/.claude/skills/humanizer/SKILL.md`.
To update:

```bash
# Edit the source at ~/.claude/skills/humanizer/SKILL.md
# Then sync to plugin
make sync-humanizer

# Test with reinstall
make reinstall
```

## Development

```bash
# Validate plugin structure
make validate

# Full reinstall
make reinstall

# Uninstall
make uninstall

# Show available targets
make help
```

## Directory Structure

```
cc-prose/
+-- .claude-plugin/
|   +-- marketplace.json           # Root marketplace
+-- prose/                         # Plugin directory
|   +-- .claude-plugin/
|   |   +-- plugin.json            # Plugin manifest
|   +-- .claude/
|   |   +-- settings.local.json    # Permissions
|   +-- commands/                  # Thin command wrappers
|   |   +-- write.md
|   |   +-- rewrite.md
|   |   +-- voice.md
|   |   +-- check.md
|   |   +-- init.md
|   +-- skills/                    # Detailed workflows
|   |   +-- content-generator/
|   |   +-- humanizer/
|   |   +-- voice-architect/
|   |   +-- voice-extractor/
|   |   +-- pre-validator/
|   +-- knowledge-base/
|   |   +-- voice-autodetect.md
|   |   +-- voice-templates/
|   |       +-- analytical.yaml
|   |       +-- conversational.yaml
|   |       +-- narrative.yaml
|   |       +-- pov.yaml
|   |       +-- reasoning.yaml
|   |       +-- reference.yaml
|   |       +-- technical.yaml
|   |       +-- tutorial.yaml
|   +-- docs/
+-- Makefile
+-- README.md
+-- CLAUDE.md
+-- LICENSE
```

## Related Projects

- [cc-copyedit](https://github.com/rhuss/cc-copyedit) - Comprehensive copy-editing for technical documentation
- [cc-superpowers-sdd](https://github.com/rhuss/cc-superpowers-sdd) - Specification-driven development plugin

## License

MIT
