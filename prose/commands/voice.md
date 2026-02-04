---
name: voice
description: Manage voice profiles for consistent writing personality
user-invocable: true
argument: subcommand
---

# /prose:voice - Voice Profile Management

Create and manage voice profiles for consistent writing personality.

## Usage

```
/prose:voice create <name>
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

This command invokes the **voice-architect** skill to:

1. Manage voice profile definitions (YAML format)
2. Apply consistent personality characteristics across documents
3. Store profiles in `~/.claude/prose/voices/` (global) or `.prose/voice.yaml` (project)

## Invoke Skill

Use the **voice-architect** skill with the provided subcommand and arguments.
