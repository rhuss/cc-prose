# cc-prose Tutorial

A quick start guide to using the writing skill plugin for content generation with human voice.

## Prerequisites

Before using this plugin, you should have:

1. Claude Code installed and configured
2. Optionally: style configuration at `~/.claude/style/` (global) or `.style/` (project)
   - Legacy paths (`~/.claude/copyedit/config/`, `.copyedit/`) are also supported

## Installation

```bash
cd ~/Development/context-engineering/cc-prose
make install
```

Verify installation:
```bash
claude plugin list
# Should show: prose@prose-plugin-development
```

## Your First Content Generation

### Step 1: Generate Content

```bash
/prose:write a brief introduction to Kubernetes Pods
```

The plugin will:
1. Check for copyedit configuration
2. Check for an active voice profile
3. Generate content following all style rules
4. Validate against AI patterns
5. Present publication-ready text

### Step 2: Review the Output

The generated content will be free of:
- AI vocabulary words (delve, leverage, robust)
- Chatbot artifacts (I hope this helps)
- Promotional language (groundbreaking)
- Filler phrases (in order to)

### Step 3: Make Adjustments

If you want a different tone, create a voice profile:

```bash
/prose:voice create my-style
```

## Creating a Voice Profile

### Interactive Creation

```bash
/prose:voice create technical-blog
```

You'll be asked about:

**Formality:**
- Casual (0.4) - Like talking to a friend
- Balanced (0.6) - Professional but approachable
- Formal (0.8) - Academic, authoritative

**Personality:**
- Neutral (0.3) - Objective, factual
- Engaged (0.6) - Express opinions, reactions
- Strong (0.9) - Highly opinionated

**Pronouns:**
- You-focused - "You can configure..."
- We-inclusive - "We'll explore..."
- Mixed (recommended) - 60% you, 40% we

**Contractions:**
- Yes - Use don't, can't, won't
- No - Spell out for formal tone

### Example Profile

```yaml
name: "technical-blog"
characteristics:
  formality: 0.5
  personality: 0.7
  first_person: true
  contractions: true
sentence_patterns:
  mix_short: true
  max_consecutive_similar: 3
personality_traits:
  opinions: true
  acknowledge_complexity: true
```

### Setting as Project Default

Save the profile to `.style/voice.yaml` for project-wide use (or legacy `.prose/voice.yaml`).

## Humanizing Existing Text

### Basic Usage

```bash
/prose:rewrite docs/chapter03.md
```

### What Gets Fixed

**Before (AI-sounding):**
> This groundbreaking solution leverages robust capabilities to deliver a seamless experience. It serves as a testament to innovation, fostering collaboration and underscoring the vital role of technology in our evolving landscape.

**After (Human):**
> This solution uses reliable features to provide a good user experience. The technology supports team collaboration effectively.

### Pattern Categories

The humanizer addresses 24 pattern categories:

1. **Content patterns**: Significance inflation, promotional language
2. **Language patterns**: AI vocabulary, copula avoidance
3. **Style patterns**: Em dash overuse, curly quotes
4. **Communication patterns**: Chatbot artifacts, sycophantic tone
5. **Filler/hedging**: Unnecessary words, excessive qualification

## Pre-Submission Validation

### Running Validation

```bash
/prose:check docs/chapter03.md
```

### Understanding the Report

The report includes:

| Category | Weight | Description |
|----------|--------|-------------|
| AI Patterns | 25 pts | Humanizer pattern violations |
| Style | 25 pts | Sentence structure, voice, formatting |
| Flow | 20 pts | Transitions, structure, guidance |
| Consistency | 15 pts | Terminology, duplications |
| Voice | 15 pts | Profile matching |

### Score Interpretation

- **85-100**: PASS - Ready for publication
- **70-84**: PASS WITH WARNINGS - Minor issues
- **<70**: FAIL - Significant issues need fixing

## Working with Style Configuration

### Initialize Configuration

The easiest way to set up configuration is using the init command:

```bash
# Initialize project configuration
/prose:init

# Initialize global configuration (applies to all projects)
/prose:init --global
```

### Global Configuration

Global settings that apply to all projects are stored in `~/.claude/style/`:

```
~/.claude/style/
├── config.yaml      # Thresholds and settings
├── styleguide.md    # Style rules
├── wordlist.txt     # Preferred terminology
├── stoplist.txt     # Words to never use
└── voices/          # Voice profile library
    ├── technical.yaml
    └── conversational.yaml
```

### Project Configuration

Project-specific overrides are stored in `.style/`:

```
.style/
├── config.yaml      # Project thresholds
├── styleguide.md    # Project style rules
├── wordlist.txt     # Project terminology
├── stoplist.txt     # Project blocked words
└── voice.yaml       # Project voice profile
```

Project settings override global settings.

### Configuration Hierarchy

```
Plugin defaults (built-in)
    ↓ overridden by
Global config (~/.claude/style/)
    ↓ overridden by
Project config (.style/)
```

**Merge behavior:**
- Thresholds: Project overrides global
- Wordlists: Both combined
- Stoplists: Both combined
- Styleguides: Both enforced

### Stoplist Example

```text
# ~/.claude/style/stoplist.txt
# Forbidden words (never use)

delve -> explore, examine, investigate
leverage -> use, apply
utilize -> use
robust -> reliable, strong
comprehensive -> complete, thorough
crucial -> critical, key
pivotal -> critical, important
```

### Backward Compatibility

Legacy paths are still supported:
- `~/.claude/copyedit/config/` (legacy global)
- `.copyedit/` (legacy project)
- `~/.claude/prose/voices/` (legacy voice profiles)
- `.prose/voice.yaml` (legacy project voice)

## Tips for Best Results

### Content Generation

1. **Be specific** in your request
   - Good: "Write a section explaining Kubernetes Pod networking with examples"
   - Less good: "Write about Pods"

2. **Mention the audience**
   - "Write for beginners who know Docker but not Kubernetes"

3. **Specify format** if needed
   - "Use AsciiDoc format with one sentence per line"

### Voice Profiles

1. **Start with templates**
   - Use `technical` or `conversational` as starting points
   - Customize from there

2. **Match your audience**
   - Technical docs: Higher formality, lower personality
   - Tutorials: Lower formality, higher personality

3. **Be consistent**
   - Use one profile per project for consistency

### Humanizing

1. **Run on complete sections**
   - Context helps the humanizer make better choices

2. **Review the changes**
   - Some "AI patterns" may be intentional

3. **Iterate if needed**
   - Run multiple passes for heavily AI-generated text

## Troubleshooting

### Plugin Not Found

```bash
make reinstall
claude plugin list
```

### Configuration Not Loading

Check paths (new unified paths):
```bash
ls ~/.claude/style/
ls .style/
```

Or legacy paths:
```bash
ls ~/.claude/copyedit/config/
ls .copyedit/
```

### Voice Profile Not Applied

Ensure profile is in correct location:
- Global: `~/.claude/style/voices/<name>.yaml` (or legacy `~/.claude/prose/voices/`)
- Project: `.style/voice.yaml` (or legacy `.prose/voice.yaml`)

## Next Steps

- Explore the [help documentation](help.md) for command reference
- Read the skill files in `writing/skills/` for detailed workflows
- Check the [README](../../README.md) for full documentation
