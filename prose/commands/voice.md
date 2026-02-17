---
description: Manage voice profiles for consistent writing personality
argument-hint: "[subcommand]"
---

# /prose:voice - Voice Profile Management

Create and manage voice profiles for consistent writing personality.

## Usage

```
/prose:voice create <name>
/prose:voice extract <source>
/prose:voice apply <name> <file_or_text>
/prose:voice list
/prose:voice show <name>
```

## Subcommands

### create

Create a new voice profile interactively:

```
/prose:voice create technical-friendly
```

This will prompt for voice characteristics (formality, personality, pronouns, etc.).

### extract

Extract a voice profile from existing content:

```
/prose:voice extract docs/my-writing.md
/prose:voice extract "docs/**/*.md"
/prose:voice extract docs/
/prose:voice extract document.pdf
```

Analyzes writing patterns to derive all voice profile parameters (formality, personality, sentence patterns, pronoun balance, etc.) with confidence scores.

### apply

Apply a voice profile to content:

```
/prose:voice apply technical-friendly docs/intro.md
```

### list

Show all available voice profiles:

```
/prose:voice list
```

### show

Display details of a specific voice profile:

```
/prose:voice show technical-friendly
```

## What This Command Does

This command invokes the **voice-architect** or **voice-extractor** skill to:

1. Manage voice profile definitions (YAML format)
2. Extract voice profiles from existing content samples
3. Apply consistent personality characteristics across documents
4. Store profiles in `~/.claude/style/voices/` (global) or `.style/voice.yaml` (project)

## Invoke Skill

- For `create`, `apply`, `list`, `show`: Use the **voice-architect** skill
- For `extract`: Use the **voice-extractor** skill
