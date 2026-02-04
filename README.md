# cc-prose

A Claude Code plugin for **proactive content generation** with human voice and AI slop prevention.

## Overview

This plugin helps you write content that sounds authentically human while following all style rules.
It complements the [copyedit plugin](https://github.com/rhuss/cc-copyedit), sharing its configuration but with a clear separation of concerns:

- **copyedit** = Review and fix existing content (editing)
- **prose** = Generate new content with human voice (creation)

**Key features:**

- **Automatic activation**: Activates when you request content creation
- **Voice profiles**: Consistent personality across documents
- **Humanizer depth**: Wikipedia's 24-pattern methodology for authentic writing
- **Proactive guidance**: Pattern prevention during writing (not just post-editing)
- **Easy humanizer updates**: Sync from upstream source with `make sync-humanizer`

> **Note:** If you previously used copyedit's `content-writer` skill, this plugin's `content-generator` supersedes it.
> The copyedit plugin should focus on editing, not content creation.

## Installation

```bash
# Clone the repository
git clone https://github.com/rhuss/cc-prose.git
cd cc-prose

# Install the plugin
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

## Quick Start

### Generate Content

The content-generator skill activates **automatically** when you request content creation:

```bash
# Just ask naturally - the skill activates automatically
Write a section about Kubernetes Services with human voice

# Or use the explicit command
/prose:write a section explaining how Kubernetes Services work
```

The content-generator will:
1. Load your copyedit configuration
2. Apply your active voice profile
3. Generate content following all style rules
4. Validate against humanizer patterns
5. Present publication-ready text

### Humanize Existing Text

```bash
# Transform AI-sounding text
/prose:rewrite docs/chapter03.md
```

The humanizer identifies and removes all 24 categories of AI writing patterns while injecting authentic personality.

### Create a Voice Profile

```bash
# Create a new voice profile interactively
/prose:voice create technical-friendly
```

You'll be prompted for:
- Formality level (casual to formal)
- Personality level (neutral to opinionated)
- Pronoun preferences (you vs we)
- Contractions usage

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

## Voice Profiles

Voice profiles define consistent personality characteristics for your writing.

### Built-in Templates

| Profile | Formality | Personality | Best For |
|---------|-----------|-------------|----------|
| `technical` | 0.6 (balanced) | 0.6 (engaged) | API docs, guides |
| `conversational` | 0.4 (casual) | 0.8 (opinionated) | Tutorials, blog posts |

### Profile Locations

- **Global**: `~/.claude/prose/voices/` (available across all projects)
- **Project**: `.prose/voice.yaml` (project-specific, overrides global)

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

## Configuration

This plugin shares configuration with the copyedit plugin:

- `~/.claude/copyedit/config/` - Global settings
- `.copyedit/` - Project overrides

### Key Configuration Files

| File | Purpose |
|------|---------|
| `stoplist.txt` | Forbidden words (constitutional rule) |
| `wordlist.txt` | Preferred terminology |
| `styleguide.md` | Prose style rules |
| `config.yaml` | Thresholds and settings |

## AI Pattern Prevention

The plugin enforces Wikipedia's 24 AI writing pattern categories:

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
|   +-- skills/                    # Detailed workflows
|   |   +-- content-generator/
|   |   +-- humanizer/
|   |   +-- voice-architect/
|   |   +-- pre-validator/
|   +-- knowledge-base/
|   |   +-- voice-templates/
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
