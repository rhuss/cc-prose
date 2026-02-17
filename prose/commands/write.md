---
description: Generate new prose content with human voice
argument-hint: "[topic or requirements]"
---

# /prose:write - Content Generation

Generate new content following all style rules with human voice.

## Usage

```
/prose:write <topic or requirements>
```

## Examples

```
/prose:write a section explaining how Kubernetes Pods work
/prose:write an introduction to machine learning for beginners
/prose:write a technical blog post about API design patterns
```

## Automatic Activation

The content-generator skill also activates **automatically** when you:

1. Request content creation:
   - "Write a section about..."
   - "Create a chapter on..."
   - "Draft a paragraph explaining..."

2. Use writing keywords:
   - "with human voice"
   - "publication-ready"
   - "following our styleguide"

So you can simply ask:
```
Write a section about Kubernetes networking with human voice
```

And the content-generator skill will activate automatically.

## When to Use This Command

Use `/prose:write` explicitly when:
- You want to be certain the content-generator skill is invoked
- Your request doesn't include obvious content creation keywords
- You want to bypass any ambiguity

## What This Command Does

This command invokes the **content-generator** skill to:

1. Load copyedit configuration (global and project)
2. Apply the active voice profile (if configured)
3. Generate content that inherently follows all rules
4. Enforce all humanizer patterns (24 categories)
5. Self-validate before presenting output

## Invoke Skill

Use the **content-generator** skill with the provided topic or requirements.
