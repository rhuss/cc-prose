---
name: check
description: Validate content before submission for AI patterns and style issues
user-invocable: true
argument: file_path
---

# /prose:check - Pre-Submission Validation

Validate content for AI patterns, style compliance, and voice consistency before submission.

## Usage

```
/prose:check <file_path>
```

## Examples

```
/prose:check docs/chapter03.md
/prose:check README.md
```

## What This Command Does

This command invokes the **pre-validator** skill to perform comprehensive validation:

### AI Pattern Scan
- Check all 24 humanizer categories (content, language, style, communication, filler/hedging)
- Flag CRITICAL, HIGH, MEDIUM, and LOW severity patterns

### Stoplist Word Check
- Verify no forbidden words from `~/.claude/copyedit/config/stoplist.txt`
- Verify no forbidden words from `.copyedit/stoplist.txt`

### Style Compliance
- Active voice percentage (target >80%)
- Sentence length (max 40 words, avg 15-20)
- Sentence variety (no 3+ consecutive similar lengths)
- Contractions for conversational tone
- Number style (spell out 0-9, numerals for 10+)
- Serial comma in lists
- No special characters (curly quotes, em dash, en dash)

### Flow Quality
- Smooth transitions between paragraphs
- Front-loaded paragraphs (topic sentence first)
- Concrete follows abstract (examples within 2-3 sentences)
- Minimal parentheticals and dash insertions

### Consistency
- Terminology consistency (same concept = same term)
- Kubernetes resources capitalized (Pod, Service, ConfigMap)
- No semantic duplications

### Voice Consistency
- Matches selected voice profile (if configured)
- Consistent formality and personality

### Report Format

The validation produces a detailed report with:
- Overall score (0-100)
- Issues by severity
- Specific line numbers and suggestions
- Pass/fail recommendation for submission

## Invoke Skill

Use the **pre-validator** skill with the provided file path.
