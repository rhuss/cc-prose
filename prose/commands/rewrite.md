---
description: Rewrite existing text to remove AI patterns
argument-hint: "[file-path or text]"
---

# /prose:rewrite - Humanize Text

Transform AI-sounding text into natural, human-written content.

## Usage

```
/prose:rewrite <file_path>
/prose:rewrite <inline_text>
```

## Examples

```
/prose:rewrite docs/chapter03.md
/prose:rewrite "The groundbreaking solution leverages robust capabilities..."
```

## What This Command Does

This command invokes the **humanizer** skill to:

1. Identify all 24 categories of AI writing patterns
2. Rewrite problematic sections with natural alternatives
3. Inject personality and voice (opinions, varied rhythm, acknowledgment of complexity)
4. Preserve the core meaning while removing AI markers
5. Present the humanized version with a summary of changes

## Invoke Skill

Use the **humanizer** skill with the provided file path or text.
