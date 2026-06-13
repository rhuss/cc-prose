# Research: Voice Profile Granularity Refinement

## R1: Where to place new parameters in existing YAML schema

**Decision**: New parameters integrate into existing groups, plus one new group.

- `confidence` (float 0.0-1.0) goes into `characteristics` alongside `formality` and `personality`
- `paragraph_patterns` is a new top-level group (like `sentence_patterns`) with `avg_length`, `opening_style`, `transition_style`
- `sentence_starters` goes into existing `sentence_patterns` group
- `emotional_range`, `self_correction`, `directness` go into existing `personality_traits` group
- `specificity` goes into existing `elaboration` group
- `measurements` is a new top-level group, optional, extractor-only

**Rationale**: Follows existing convention of grouping by concern. No restructuring needed.

**Alternatives**: Flat namespace (rejected: loses grouping), nested tiers (rejected: organizational only, doesn't improve generation).

## R2: How skills consume voice profile parameters

**Decision**: Skills read voice profiles as YAML, then use the values as prompt instructions during generation/rewriting. No code execution, no runtime libraries.

**Current flow**:
1. Skill reads `.style/voice.yaml` or `.prose/voice.yaml` via shell commands
2. YAML values are interpreted as generation guidance in the skill's prompt
3. Self-validation checks output against profile settings

**Impact**: New parameters are consumed the same way. The skill SKILL.md files need updated sections describing how to interpret each new parameter. No architectural change.

## R3: How the self-audit subagent should receive measurements

**Decision**: The measurements section is included in the self-audit subagent prompt alongside the draft text, as an additional validation block after the higher-order signal checks.

**Rationale**: The subagent already receives the draft in isolation. Adding measurements as "validate these numeric targets" is a natural extension. No separate validation step needed.

**Implementation**: The humanizer and content-generator skills append a "Measurement Validation" section to the subagent prompt when `measurements` is present in the loaded profile.

## R4: How the voice-extractor computes measurement values

**Decision**: The extractor computes measurements using text analysis within its existing corpus processing workflow, after parameter extraction.

**Measurements and computation approach**:
- `sentence_length_mean`: Count words per sentence, compute mean
- `sentence_length_stdev`: Standard deviation of words per sentence
- `paragraph_length_mean`: Count sentences per paragraph, compute mean
- `passive_voice_pct`: Count passive constructions / total sentences * 100
- `hedge_density_per_1000`: Count hedge words ("perhaps", "might", "somewhat", "arguably", "possibly") per 1000 words
- `connector_variety`: Unique connectors / total connectors (0.0-1.0 ratio)
- `concrete_abstract_ratio`: Ratio of concrete nouns to abstract nouns
- `punctuation_entropy`: Shannon entropy of punctuation character distribution
- `one_sentence_paragraph_rate`: Single-sentence paragraphs / total paragraphs (0.0-1.0)
- `contraction_rate_per_1000`: Contractions per 1000 words

**Rationale**: All measurements can be approximated by the LLM analyzing the corpus text directly. No external NLP libraries needed since the extractor runs as a Claude Code skill (LLM-based analysis).

## R5: Old-format detection strategy

**Decision**: Detect old format by checking for the absence of the `confidence` field in `characteristics`. If missing, the profile is old-format.

**Migration defaults**:
- `confidence`: 0.5
- `paragraph_patterns.avg_length`: medium
- `paragraph_patterns.opening_style`: varied
- `paragraph_patterns.transition_style`: organic
- `sentence_starters`: varied
- `emotional_range`: moderate
- `self_correction`: false
- `directness`: balanced
- `specificity`: balanced

**Rationale**: `confidence` is the most distinctive new field. Checking one field is simpler than checking all. Defaults are middle-of-the-road values that won't change existing behavior.
