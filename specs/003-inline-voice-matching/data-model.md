# Data Model: Inline Voice-Matching

## Overview

This feature does not introduce persistent data models. Inline voice matching is entirely ephemeral, operating within a single skill invocation. No YAML profiles, configuration files, or state are created.

## Voice Source Resolution (Conceptual)

The voice source resolution follows a priority chain. This is not stored data but runtime behavior encoded in the SKILL.md instructions.

### Priority Chain

```
1. Inline Sample (user provides text or file reference in current request)
   ↓ (not present)
2. Configured Voice Profile (.style/voice.yaml or .prose/voice.yaml)
   ↓ (not present)
3. Auto-Detection (content-generator only: pattern-based voice selection)
   ↓ (no match)
4. Default Behavior (humanizer: PERSONALITY AND SOUL; content-generator: technical voice)
```

### Inline Sample Analysis Dimensions

When an inline sample is provided, the skill extracts these ephemeral characteristics (never persisted):

| Dimension | What to Note | Example |
|-----------|-------------|---------|
| Sentence length | Short/punchy, long/flowing, mixed | "Mostly 8-12 words, occasional 25+ word sentence" |
| Word choice level | Casual, academic, technical, mixed | "Uses 'stuff' and 'things', avoids jargon" |
| Paragraph openings | Jump right in, set context first | "Starts with a question or assertion" |
| Punctuation habits | Dashes, parentheticals, semicolons | "Heavy use of parenthetical asides" |
| Recurring phrases | Verbal tics, favorite expressions | "Frequently uses 'the thing is'" |
| Transition handling | Explicit connectors, implicit flow | "Rarely uses 'however' or 'moreover'" |

### Input Methods

| Method | Format | Validation |
|--------|--------|------------|
| Inline text | User pastes sample in the request | Always accepted, no minimum word count |
| File reference | User provides a path to existing writing | Must exist, must be text (not binary) |

### Style Rule Override

Project-level style rules (from CLAUDE.md or copyedit config) take precedence over inline voice matching for specific prohibited patterns. For example, if the sample uses em dashes but CLAUDE.md forbids them, em dashes are still forbidden in the output.
