# Brainstorm: Voice profile granularity refinement

**Date:** 2026-06-13
**Status:** active

## Problem Framing

Our voice profiles have ~20 parameters across 5 groups (characteristics, sentence_patterns, elaboration, personality_traits, pronoun_balance). Research across commercial humanizers, AI writing assistants, academic stylometry (LIWC, Coh-Metrix, Biber), and open-source tools (harshaneel/humanize, ngpepin/stylometric-transfer) reveals that effective voice control needs 30-50 actionable dimensions.

The current profiles have two problems:

1. **Expressiveness gaps.** Key dimensions that distinguish human from AI writing are missing entirely: hedging/confidence, paragraph structure, opening patterns, vocabulary sophistication, discourse flow, and emotional texture.

2. **Consistency gaps.** Existing parameters like `variation: moderate` are too coarse for the LLM to follow reliably. The generator interprets "moderate" differently across runs because there's no numeric target to validate against.

## Research Summary

Sources examined:
- **Commercial humanizers** (15 tools): Most expose only 2-3 user-facing dimensions (readability, purpose, rewrite strength). Only Humaniser.com's API exposes burstiness as a named parameter.
- **Writing assistants** (10 tools): Grammarly is most granular with 12 tone dimensions. ProWritingAid reports on 25 distinct analysis dimensions including sticky sentences, pacing, sentence starters, echoes.
- **Academic frameworks**: LIWC-22 (118 categories), Coh-Metrix (108 indices), Biber's MDA (7 dimensions, 67 features). These provide the measurement science for what makes writing distinct.
- **Open-source**: harshaneel/humanize uses 9 concrete levers (perplexity injection, burstiness enforcement, hedge surgery). ngpepin/stylometric-transfer has ~86 measurable features with fingerprint profiles.
- **AI detection research**: Top distinguishing signals are burstiness (sentence length variance), perplexity (word-level surprise), hedging frequency, sentence opener variety, and emotional range.

### Gap analysis: current profile vs. research

| Dimension | Our profiles | Research evidence |
|---|---|---|
| Hedging/confidence | Missing | Grammarly's top tone dimension, harshaneel Lever 3, LIWC `tentat` vs `certitude` |
| Paragraph structure | Missing | Coh-Metrix paragraph cohesion, ngpepin paragraph cadence, ProWritingAid pacing |
| Opening/closing patterns | Missing | ngpepin sentence-opener templates, AI detection (first-word POS distribution) |
| Vocabulary sophistication | Only `audience` level | Coh-Metrix (concreteness, familiarity, imageability), harshaneel Lever 1 |
| Discourse flow | Missing | Coh-Metrix connective types, Biber Dim 3, ProWritingAid transition report |
| Emotional texture | Only `humor` toggle | LIWC (6 emotion subcategories), Grammarly (confidence, friendliness, urgency) |
| Sentence length variance | `variation: low/moderate/high` | AI detection research: burstiness is the #1 human signal. Our enum is too coarse |
| Self-correction markers | Missing | AI detection: "I mean", "actually", "well" are key human signals |

## Approaches Considered

### A: Targeted human-readable additions (~10 new params)

Add parameters that humans can reason about and LLMs can follow reliably. Focus on the dimensions backed by detection research.

New parameters:
- `confidence` (0.0-1.0): hedged to assertive
- `paragraph_patterns.avg_length`: short/medium/long
- `paragraph_patterns.opening_style`: direct/contextual/anecdotal/varied
- `paragraph_patterns.transition_style`: explicit/organic/minimal
- `sentence_patterns.sentence_starters`: pronoun-heavy/varied/formal-lead
- `personality_traits.emotional_range`: flat/moderate/dynamic
- `personality_traits.self_correction`: boolean (markers like "I mean", "actually")
- `personality_traits.directness`: hedged/balanced/blunt
- `elaboration.specificity`: abstract/balanced/concrete

Pros: Small surface area, each param backed by research, no schema restructuring.
Cons: Doesn't cover vocabulary sophistication or discourse metrics as explicit knobs.

### B: Layered schema (three tiers)

Restructure into Tier 1 (essential, ~10), Tier 2 (detailed, ~20), Tier 3 (fingerprint, ~15). Most users only touch Tier 1.

Pros: Good discoverability, accommodates simple and power-user workflows.
Cons: Tier hierarchy is organizational, not functional. The LLM processes the whole profile at once, not tier-by-tier. Doesn't improve generation quality over A.

### C: Measurement section (extractor-populated)

Add a `measurements` section with numeric targets derived from writing samples by the voice-extractor. Not manually editable.

```yaml
measurements:
  sentence_length_mean: 16.2
  sentence_length_stdev: 7.8
  paragraph_length_mean: 4.3
  passive_voice_pct: 8
  hedge_density_per_1000: 3.2
  connector_variety: 0.72
  concrete_abstract_ratio: 1.4
  punctuation_entropy: 2.1
  one_sentence_paragraph_rate: 0.05
  contraction_rate_per_1000: 12.4
```

Pros: Grounded in measurement, gives self-audit subagent concrete validation targets, makes voice extraction more powerful.
Cons: Numbers are meaningless to humans setting up profiles manually (hence extractor-only).

## Decision

**Approach A + C combined.** This separates two fundamentally different concerns:

- **A (human-readable knobs)** guide the generator during writing. The LLM understands "write assertively" better than "hedge_density_per_1000: 3.2".
- **C (numeric measurements)** give the self-audit subagent concrete validation targets. "Your sentence length stdev is 3.2 but the target is 7.8" is actionable feedback that "use high variation" is not.

This split maps to how our skills already work: generate with human intent, validate with measurable targets.

**Why not B:** Tier hierarchy helps humans navigate the schema but doesn't improve generation quality. The LLM doesn't process tiers sequentially. The A+C split (intent vs. measurement) is more useful than a priority ranking.

**Measurements are extractor-only.** Numbers like `punctuation_entropy: 2.1` aren't things humans think about. They're statistical fingerprints that emerge from writing. Manual profile creators use the human-readable knobs; the measurements section stays empty until they run the extractor on samples.

## Key Requirements

1. Add ~10 new human-readable parameters to the voice profile schema (see Approach A list above)
2. Add a `measurements` section to the schema, populated only by the voice-extractor
3. Update all 8 built-in voice templates with values for the new parameters
4. Update the voice-extractor to populate the measurements section from writing samples
5. Update the content-generator to consume the new parameters during generation (Step 3)
6. Update the self-audit subagent prompt to validate against measurements when present
7. Update the humanizer to respect the new parameters during rewriting
8. Update the voice-architect to handle the new schema (create/edit workflows)
9. Add old-format auto-detection: when a voice profile is loaded that lacks the new parameters, offer to migrate it (add defaults for new params, leave measurements empty)
10. Update the pre-validator to check voice consistency against the expanded parameter set

## Open Questions

- Which specific measurements should the extractor compute? The list above is a starting point. Should we include all of ngpepin's 86 features or a curated subset?
- Should the self-audit subagent receive the measurements section, or should a separate validation step check measurements post-generation?
- How should measurements interact with inline voice matching (brainstorm #02)? Inline samples are too short for reliable measurement extraction.
- Should we add a `prose:measure` command that analyzes any text and reports its measurements (without creating a profile)?
