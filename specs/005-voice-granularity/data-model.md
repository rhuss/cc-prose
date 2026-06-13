# Data Model: Voice Profile Granularity Refinement

## Voice Profile (YAML file)

The voice profile is a YAML configuration file. This feature extends it with new fields (marked with **NEW**).

```yaml
# Identity
name: string                    # Profile identifier
version: string                 # Profile version
description: string             # Brief description
tone_description: string        # Prose description of voice feel

# Characteristics
characteristics:
  formality: float              # 0.0 (casual) to 1.0 (formal)
  personality: float            # 0.0 (neutral) to 1.0 (opinionated)
  confidence: float             # **NEW** 0.0 (hedged) to 1.0 (assertive)
  first_person: boolean         # Use I/we pronouns
  contractions: boolean         # Use don't/can't/won't
  audience: enum                # beginner | intermediate | expert

# Sentence Patterns
sentence_patterns:
  mix_short: boolean            # Include short punchy sentences
  max_consecutive_similar: int  # Max same-length sentences in a row
  avg_length_target: int        # Target avg words per sentence
  variation: enum               # low | moderate | high
  rhetorical_questions: boolean # Include rhetorical questions
  sentence_starters: enum       # **NEW** pronoun-heavy | varied | formal-lead

# Paragraph Patterns (**NEW group**)
paragraph_patterns:
  avg_length: enum              # **NEW** short | medium | long
  opening_style: enum           # **NEW** direct | contextual | anecdotal | varied
  transition_style: enum        # **NEW** explicit | organic | minimal

# Elaboration
elaboration:
  depth: enum                   # minimal | moderate | thorough
  provide_context: boolean      # Background before main points
  include_examples: boolean     # Add examples
  explain_reasoning: boolean    # Explain why not just what
  analogies: enum               # none | rare | moderate | frequent
  analogy_domain: string        # Domain for analogies (optional)
  specificity: enum             # **NEW** abstract | balanced | concrete

# Personality Traits
personality_traits:
  opinions: boolean             # Express opinions and reactions
  acknowledge_complexity: boolean # Acknowledge uncertainty
  humor: enum                   # none | subtle | moderate
  personal_experience: boolean  # Reference personal experience
  emotional_range: enum         # **NEW** flat | moderate | dynamic
  self_correction: boolean      # **NEW** Include "I mean", "actually" markers
  directness: enum              # **NEW** hedged | balanced | blunt

# Pronoun Balance
pronoun_balance:
  you_percentage: int           # Target % of you/your/yours (0-100)
  we_percentage: int            # Target % of we/our/ours (0-100)

# Phrases
signature_phrases: list[string] # Characteristic phrases to use
avoid_phrases: list[string]     # Phrases to never use

# Measurements (**NEW group**, extractor-only, optional)
measurements:
  sentence_length_mean: float           # Mean words per sentence
  sentence_length_stdev: float          # Std dev of words per sentence
  paragraph_length_mean: float          # Mean sentences per paragraph
  passive_voice_pct: float              # Passive constructions as % of total sentences
  hedge_density_per_1000: float         # Hedge words per 1000 words
  connector_variety: float              # Unique connectors / total connectors (0.0-1.0)
  concrete_abstract_ratio: float        # Concrete nouns / abstract nouns
  punctuation_entropy: float            # Shannon entropy of punctuation distribution
  one_sentence_paragraph_rate: float    # Single-sentence paragraphs / total paragraphs (0.0-1.0)
  contraction_rate_per_1000: float      # Contractions per 1000 words
  sample_confidence: enum               # **NEW** low | medium | high (corpus reliability)

# Optional domain-specific sections (unchanged)
# domain_vocabulary: ...
# document_structure: ...
# stylistic_fingerprints: ...
```

## Field Relationships

- `confidence` and `directness` are independent dimensions. High confidence + hedged directness = "certain but diplomatically expressed."
- `measurements` values are derived from writing samples, not set manually. The `sample_confidence` field indicates corpus reliability.
- Human-readable params guide generation. Measurements validate post-generation via the self-audit subagent.
- When measurements conflict with human-readable params, generation intent wins; the self-audit reports the discrepancy.

## Validation Rules

- `confidence` must be in range [0.0, 1.0]
- `paragraph_patterns.avg_length` must be one of: short, medium, long
- `paragraph_patterns.opening_style` must be one of: direct, contextual, anecdotal, varied
- `paragraph_patterns.transition_style` must be one of: explicit, organic, minimal
- `sentence_starters` must be one of: pronoun-heavy, varied, formal-lead
- `emotional_range` must be one of: flat, moderate, dynamic
- `directness` must be one of: hedged, balanced, blunt
- `specificity` must be one of: abstract, balanced, concrete
- `self_correction` must be boolean
- All `measurements` fields are optional floats (absent when not extracted)
- `sample_confidence` must be one of: low, medium, high (when measurements present)
