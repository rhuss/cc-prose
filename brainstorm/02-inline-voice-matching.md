# Brainstorm: Inline voice-matching in the humanizer

**Date:** 2026-06-12
**Status:** active

## Problem Framing

When a user says "rewrite this to sound like my blog post at X," our current architecture requires a multi-step workflow: run voice-extractor to analyze the sample, save a YAML profile via voice-architect, then invoke the humanizer with that profile. The upstream humanizer (v2.8.0) handles this in a single pass with an inline "Voice Calibration" section.

Our full voice pipeline (extractor → architect → profile YAML) is more powerful for repeat use, but the lightweight inline path fills a gap: ad-hoc, one-shot voice matching without ceremony.

## Context

### Current cc-prose voice architecture
- **voice-extractor**: Deep multi-file corpus analysis, confidence scoring, produces reusable YAML profiles. Supports single-pass and multi-pass modes, weighting by file quality. Minimum 500-word corpus.
- **voice-architect**: Interactive CRUD for voice profiles. Creates profiles from questionnaire or parameters.
- **content-generator**: Loads voice profile from `.style/voice.yaml` or `.prose/voice.yaml`, applies during generation.
- **humanizer**: Announces voice before rewriting, but only uses pre-configured profiles. No inline sample matching.

### Upstream approach (v2.8.0 Voice Calibration)
```
If the user provides a writing sample, analyze it before rewriting:
1. Read the sample. Note: sentence length, word choice level, paragraph starts,
   punctuation habits, recurring phrases, transition handling.
2. Match their voice in the rewrite. Replace AI patterns with patterns from the sample.
3. When no sample is provided, fall back to default behavior.
```

Upstream's approach is intentionally lightweight: no YAML, no persistence, no confidence scores. Just "read the sample, match it."

### Gap analysis
| Scenario | Our plugin | Upstream | Gap |
|----------|-----------|----------|-----|
| "Rewrite this matching my blog" | 3 steps (extract → save → rewrite) | 1 step (inline) | We're slower |
| "Always write like our docs" | Extract once, reuse profile | Re-analyze every time | Upstream is slower |
| "Match this 200-word snippet" | voice-extractor warns: <500 words | Handles it fine inline | We block valid use |

## Approaches Considered

### A: Add inline voice-matching to humanizer (Recommended)
- Add a "Voice Calibration" section to the humanizer SKILL.md, similar to upstream
- When user provides a sample alongside a rewrite request, match it inline
- When no sample is provided but a voice profile exists, use the profile
- When neither is provided, fall back to default behavior

- Pros: Fills the gap, simple to implement, one SKILL.md edit
- Cons: Duplicates some voice-extractor logic (but much simpler version)

### B: Make voice-extractor support lightweight mode
- Add a `--quick` or `--inline` flag to voice-extractor that skips YAML generation
- Have humanizer call voice-extractor internally for sample matching
- Pros: Single source of voice analysis logic
- Cons: Over-engineering for what's essentially "read sample, note patterns, match them"

### C: Do nothing, keep current workflow
- Users who want voice matching use the full pipeline
- Pros: No new code
- Cons: Friction remains, users can't do ad-hoc matching

## Decision

Approach A: Add inline voice-matching directly to the humanizer skill. It's a small addition to the SKILL.md that covers the common case. The full voice pipeline remains for persistent, multi-file, high-fidelity extraction.

## Key Requirements

1. Add "Voice Calibration (Optional)" section to humanizer SKILL.md
2. The inline analysis should note:
   - Sentence length patterns
   - Word choice level (casual vs. academic)
   - Paragraph opening patterns
   - Punctuation habits
   - Recurring phrases or verbal tics
   - Transition handling
3. Priority order: explicit voice profile > inline sample > default behavior
4. No minimum word count for inline matching (unlike voice-extractor's 500-word minimum)
5. No YAML output, no persistence. Inline matching is ephemeral.
6. Two ways to provide a sample:
   - Inline: "Humanize this text. Here's a sample of my writing: [sample]"
   - File: "Humanize this. Use my writing style from [file path]."

## Open Questions

- Should the humanizer mention that voice-extractor exists for persistent profiles? ("For reusable profiles, use /prose:voice extract")
- Should content-generator also get inline voice-matching, or is the voice profile workflow sufficient there?
- If both an inline sample AND a voice profile are present, which wins? (Proposed: inline sample, since it's more explicit)
