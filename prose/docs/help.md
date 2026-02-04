# cc-prose Command Reference

Complete reference for all writing skill commands.

## Commands Overview

| Command | Description |
|---------|-------------|
| `/prose:write` | Generate new content |
| `/prose:rewrite` | Humanize existing text |
| `/prose:voice` | Manage voice profiles |
| `/prose:check` | Pre-submission validation |

---

## /prose:write

Generate new content with human voice and zero AI patterns.

### Syntax

```
/prose:write <topic or requirements>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| topic | Yes | What to write about |

### Examples

```bash
# Simple topic
/prose:write a section explaining Kubernetes Pods

# With context
/prose:write an introduction to machine learning for developers who know Python

# Specific format
/prose:write a technical blog post about API design patterns, 800 words
```

### What It Does

1. Loads copyedit configuration (global + project)
2. Loads active voice profile (if configured)
3. Generates content following all style rules
4. Enforces all 24 humanizer pattern categories
5. Self-validates before output
6. Presents publication-ready text

### Configuration Used

- `~/.claude/copyedit/config/styleguide.md`
- `~/.claude/copyedit/config/stoplist.txt`
- `.copyedit/styleguide.md` (overrides)
- `.prose/voice.yaml` (voice profile)

---

## /prose:rewrite

Humanize existing text by removing AI patterns and adding personality.

### Syntax

```
/prose:rewrite <file_path>
/prose:rewrite <inline_text>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| file_path | Yes* | Path to file to humanize |
| inline_text | Yes* | Text to humanize directly |

*One of file_path or inline_text required

### Examples

```bash
# Humanize a file
/prose:rewrite docs/chapter03.md

# Humanize inline text
/prose:rewrite "This groundbreaking solution leverages robust capabilities..."
```

### What It Does

1. Identifies all 24 categories of AI writing patterns
2. Rewrites problematic sections with natural alternatives
3. Injects personality (opinions, varied rhythm, acknowledgments)
4. Preserves core meaning
5. Presents humanized version with summary of changes

### Pattern Categories

| Category | Severity | Examples |
|----------|----------|----------|
| Chatbot artifacts | CRITICAL | "I hope this helps" |
| Knowledge cutoffs | CRITICAL | "as of my training" |
| AI vocabulary | HIGH | delve, leverage, robust |
| Significance inflation | HIGH | "is a testament" |
| Promotional language | HIGH | groundbreaking, stunning |
| Superficial -ing | HIGH | highlighting, showcasing |
| Style issues | HIGH | curly quotes, em dashes |
| Filler phrases | MEDIUM | "in order to" |
| Hedging | MEDIUM | "could potentially" |
| Copula avoidance | MEDIUM | "serves as" |

---

## /prose:voice

Manage voice profiles for consistent writing personality.

### Subcommands

| Subcommand | Description |
|------------|-------------|
| create | Create new voice profile |
| apply | Apply profile to content |
| list | List available profiles |
| show | Show profile details |

### /prose:voice create

Create a new voice profile interactively.

#### Syntax

```
/prose:voice create <name>
```

#### Example

```bash
/prose:voice create technical-friendly
```

#### Interactive Prompts

1. **Formality**: Casual / Balanced / Formal
2. **Personality**: Neutral / Engaged / Strong
3. **Pronouns**: You-focused / We-inclusive / Mixed
4. **Contractions**: Yes / No
5. **Location**: Global / Project

### /prose:voice apply

Apply a voice profile to content.

#### Syntax

```
/prose:voice apply <name> <file_or_text>
```

#### Example

```bash
/prose:voice apply technical-friendly docs/intro.md
```

### /prose:voice list

Show all available voice profiles.

#### Syntax

```
/prose:voice list
```

#### Output

```markdown
## Available Voice Profiles

### Global Profiles (~/.claude/prose/voices/)
| Name | Formality | Personality |
|------|-----------|-------------|
| technical | 0.6 | 0.6 |
| conversational | 0.4 | 0.8 |

### Project Profile (.prose/voice.yaml)
| Name | Formality | Personality |
|------|-----------|-------------|
| docs-voice | 0.5 | 0.6 |
```

### /prose:voice show

Display details of a specific voice profile.

#### Syntax

```
/prose:voice show <name>
```

#### Example

```bash
/prose:voice show technical
```

---

## /prose:check

Validate content before submission.

### Syntax

```
/prose:check <file_path>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| file_path | Yes | File to validate |

### Examples

```bash
/prose:check docs/chapter03.md
/prose:check README.md
```

### What It Checks

| Category | Points | Checks |
|----------|--------|--------|
| AI Patterns | 25 | All 24 humanizer categories |
| Style | 25 | Sentence structure, voice, formatting |
| Flow | 20 | Transitions, structure, guidance |
| Consistency | 15 | Terminology, duplications |
| Voice | 15 | Profile matching |

### Score Interpretation

| Score | Status | Meaning |
|-------|--------|---------|
| 85-100 | PASS | Ready for publication |
| 70-84 | WARNINGS | Minor issues |
| <70 | FAIL | Significant issues |

### Report Sections

1. **Overall Score**: Total out of 100
2. **Recommendation**: PASS / PASS WITH WARNINGS / FAIL
3. **CRITICAL Issues**: Must fix before publication
4. **HIGH Priority**: Strongly recommend fixing
5. **MEDIUM Priority**: Should fix for polish
6. **LOW Priority**: Optional improvements
7. **Readability Metrics**: Stats about the writing
8. **Voice Consistency**: Profile matching analysis

---

## Configuration Reference

### Copyedit Configuration

| File | Location | Purpose |
|------|----------|---------|
| stoplist.txt | ~/.claude/copyedit/config/ | Forbidden words |
| wordlist.txt | ~/.claude/copyedit/config/ | Preferred terms |
| styleguide.md | ~/.claude/copyedit/config/ | Style rules |
| config.yaml | ~/.claude/copyedit/config/ | Thresholds |

Project overrides in `.copyedit/`.

### Voice Configuration

| File | Location | Purpose |
|------|----------|---------|
| *.yaml | ~/.claude/prose/voices/ | Global profiles |
| voice.yaml | .prose/ | Project profile |

---

## Troubleshooting

### Command Not Found

```bash
# Reinstall plugin
make reinstall

# Verify installation
claude plugin list
```

### Configuration Not Loading

```bash
# Check global config
ls ~/.claude/copyedit/config/

# Check project config
ls .copyedit/

# Check voice profiles
ls ~/.claude/prose/voices/
ls .prose/
```

### Humanizer Not Working

```bash
# Sync humanizer from source
make sync-humanizer
make reinstall
```

---

## See Also

- [Tutorial](tutorial.md) - Quick start guide
- [README](../../README.md) - Full documentation
- [Skills](../skills/) - Detailed skill documentation
