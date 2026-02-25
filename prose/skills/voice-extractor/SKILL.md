---
name: voice-extractor
version: 2.0.0
description: >-
  Derive voice profiles from existing writing samples by analyzing patterns,
  sentence structure, and tone.
allowed-tools:
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# Voice Extractor Skill

You are a specialist in **analyzing writing samples** to extract voice profiles that capture an author's authentic writing style.

## Your Mission

Analyze existing content (Markdown, AsciiDoc, plain text, or PDFs) to:
1. **Derive voice parameters** from writing patterns
2. **Present findings** with confidence scores
3. **Create a reusable voice profile** for future content generation

This is the inverse of voice-architect: instead of creating voice profiles interactively, you extract them from real writing samples.

## When to Activate

**Trigger conditions (invoke if ANY match):**
- User says "extract voice", "derive voice profile", "analyze writing style"
- User says "create voice from this document", "learn my voice from..."
- User says "capture voice from", "derive style from", "extract profile from"
- User provides sample content and wants to capture its voice for reuse
- User wants to replicate an author's writing style from samples

**Do NOT activate for:**
- Creating voice profiles interactively (use voice-architect instead)
- Writing or editing with a voice (use content-generator or humanizer instead)

## Input Source Handling

Accept these input types:

| Input Type | Example | Handling |
|------------|---------|----------|
| Single file | `docs/intro.md` | Read directly |
| Glob pattern | `"docs/**/*.md"` | Expand and read all matches |
| Directory | `docs/` | Find all `.md`, `.adoc`, `.txt` files recursively |
| PDF file | `document.pdf` | Read PDF content |
| Multiple files | Space-separated paths | Read each file |

**Minimum corpus requirement:** At least 500 words for reliable extraction. Warn if corpus is smaller.

## Multi-File Processing Modes

When processing multiple files, the extractor uses one of two modes:

| Mode | When Used | Behavior |
|------|-----------|----------|
| **Single-pass** | 1 file OR total < 1000 words | Process all content as unified corpus |
| **Incremental** | Multiple files with >= 1000 words | Representative baseline + file-by-file processing |

### Incremental Mode Benefits

- **Visibility**: See how each file influences the profile
- **Outlier detection**: Identify files that don't match the emerging voice
- **Quality control**: Exclude inconsistent content automatically
- **Progress tracking**: Watch the profile evolve as files are processed

## Representative Sample Selection

When entering incremental mode, first select 1-3 representative files to establish a baseline profile.

### Selection Scoring

Each file receives a composite score (0.0-1.0) based on:

| Factor | Weight | Scoring |
|--------|--------|---------|
| **Word count** | 40% | Longer files score higher (normalized to corpus max) |
| **Recency** | 20% | Recently modified files score higher |
| **Format quality** | 20% | Clean prose scores higher than code-heavy/table-heavy |
| **Relevance** | 20% | Main content scores higher than README/CHANGELOG |

### Format Quality Detection

| Content Type | Score | Detection |
|--------------|-------|-----------|
| Clean prose | 1.0 | <10% code blocks, <5% tables |
| Mixed content | 0.6 | 10-30% code blocks OR 5-15% tables |
| Code-heavy | 0.3 | >30% code blocks |
| Table-heavy | 0.3 | >15% tables |
| Mostly non-prose | 0.1 | >50% non-prose elements |

### Relevance Detection

| File Pattern | Score | Examples |
|--------------|-------|----------|
| Main content | 1.0 | `docs/*.md`, `guide.adoc`, `chapter-*.md` |
| Supporting | 0.7 | `getting-started.md`, `faq.md` |
| Meta | 0.4 | `README.md`, `CONTRIBUTING.md` |
| Changelog | 0.2 | `CHANGELOG.md`, `HISTORY.md`, `RELEASE-NOTES.md` |

### Selection Logic

```
if file_count < 10:
    select top 1 file
elif file_count <= 30:
    select top 2 files
else:
    select top 3 files

# Ensure minimum baseline quality
if combined_word_count < 1000:
    add next highest-scoring files until >= 1000 words
```

### Display Format: Baseline Selection

```markdown
## Representative Sample Selection

Analyzed [N] files, scoring by word count, recency, format, and relevance.

**Selected baseline files:**

| Rank | File | Words | Score | Rationale |
|------|------|-------|-------|-----------|
| 1 | docs/architecture-guide.md | 1,847 | 0.92 | Long, recent, clean prose |
| 2 | docs/getting-started.md | 1,234 | 0.87 | Good length, tutorial content |

**Baseline corpus:** 3,081 words from 2 files

---

Extracting baseline voice profile...
```

## Incremental Merging

After establishing a baseline, process remaining files one by one with weighted averaging.

### Merge Algorithm

#### Numeric Fields

Fields: `formality`, `personality`, `avg_length_target`, `you_percentage`, `we_percentage`

```
updated_value = (current_value × total_words + new_value × new_words) / (total_words + new_words)
```

Example:
- Current formality: 0.52 (from 3,000 words)
- New file formality: 0.48 (800 words)
- Updated: (0.52 × 3000 + 0.48 × 800) / 3800 = 0.512

#### Boolean Fields

Fields: `first_person`, `contractions`, `mix_short`, `rhetorical_questions`, `provide_context`, `include_examples`, `explain_reasoning`, `opinions`, `acknowledge_complexity`, `personal_experience`

```
# Track weighted votes
true_weight += new_words if new_value == true
false_weight += new_words if new_value == false

# Current value = majority by word count
current_value = true_weight > false_weight

# Confidence = strength of majority
confidence = max(true_weight, false_weight) / (true_weight + false_weight)
```

Display confidence when relevant:
- **High confidence** (>0.75): Strong pattern
- **Medium confidence** (0.6-0.75): Moderate pattern
- **Low confidence** (<0.6): Mixed signals

#### Categorical Fields

Fields: `audience`, `variation`, `depth`, `humor`

```
# Maintain weighted frequency map
category_weights[category] += new_words

# Current value = category with highest weight
current_value = max(category_weights, key=category_weights.get)
```

#### Signature Phrases

```
# Aggregate occurrence counts across files
phrase_counts[phrase] += occurrences_in_file

# Re-rank top 5 after each merge
signature_phrases = sorted(phrase_counts, key=phrase_counts.get, reverse=True)[:5]
```

### Merge Sequence

For each remaining file (in score order, descending):

1. **Analyze file** independently to extract all parameters
2. **Compare to current profile** and calculate differences
3. **Calculate outlier score** (see next section)
4. **If not outlier**: merge values using algorithms above
5. **Display iteration output** showing analysis, decision, and changes

## Outlier Detection

Detect files that don't match the emerging voice profile to prevent contamination.

### Deviation Thresholds

| Parameter | Threshold | Severity | Description |
|-----------|-----------|----------|-------------|
| Formality | > 0.3 | HIGH | Very different register |
| Personality | > 0.3 | HIGH | Very different engagement level |
| Audience (level distance) | >= 2 | HIGH | beginner↔expert gap |
| Sentence length | > 6 words | MEDIUM | Very different rhythm |
| Boolean contradiction | confident opposite | MEDIUM | Strong disagreement on style |

### Audience Level Distance

| From/To | beginner | intermediate | expert |
|---------|----------|--------------|--------|
| beginner | 0 | 1 | 2 |
| intermediate | 1 | 0 | 1 |
| expert | 2 | 1 | 0 |

### Outlier Score Calculation

```
outlier_score = 0.0

# Numeric deviations (scaled to threshold)
if abs(file_formality - profile_formality) > 0.3:
    outlier_score += 0.3
elif abs(file_formality - profile_formality) > 0.2:
    outlier_score += 0.15

if abs(file_personality - profile_personality) > 0.3:
    outlier_score += 0.3
elif abs(file_personality - profile_personality) > 0.2:
    outlier_score += 0.15

# Audience distance
audience_distance = calculate_audience_distance(file_audience, profile_audience)
if audience_distance >= 2:
    outlier_score += 0.25

# Sentence length
if abs(file_avg_length - profile_avg_length) > 6:
    outlier_score += 0.15

# Boolean contradictions (only if profile is confident)
for bool_field in boolean_fields:
    if profile_confidence[bool_field] > 0.7:
        if file_value[bool_field] != profile_value[bool_field]:
            outlier_score += 0.1
```

### Classification

| Score Range | Classification | Action |
|-------------|----------------|--------|
| < 0.3 | **CONSISTENT** | Include in profile |
| 0.3 - 0.5 | **BORDERLINE** | Include with note |
| >= 0.5 | **OUTLIER** | Skip, profile unchanged |

## Display Formats

### Per-File Iteration Output

#### Consistent File (score < 0.3)

```markdown
---
**[4/15] Processing:** docs/deployment-guide.md (892 words)

### File Analysis

| Parameter | File Value | Profile | Difference | Status |
|-----------|------------|---------|------------|--------|
| Formality | 0.48 | 0.52 | -0.04 | ✓ |
| Personality | 0.68 | 0.72 | -0.04 | ✓ |
| First person | Yes | Yes | — | ✓ |
| Contractions | Yes | Yes | — | ✓ |
| Audience | intermediate | intermediate | 0 | ✓ |
| Avg length | 17 | 18 | -1 | ✓ |

**Outlier Score:** 0.08 (CONSISTENT)
**Decision:** INCLUDE

### Profile Update

| Parameter | Before | After | Change |
|-----------|--------|-------|--------|
| Formality | 0.52 | 0.51 | -0.01 |
| Personality | 0.72 | 0.71 | -0.01 |
| Avg length | 18 | 17.8 | -0.2 |

**Cumulative:** 4,929 words from 4 files (0 excluded)

---
```

#### Borderline File (score 0.3-0.5)

```markdown
---
**[6/15] Processing:** docs/troubleshooting.md (654 words)

### File Analysis

| Parameter | File Value | Profile | Difference | Status |
|-----------|------------|---------|------------|--------|
| Formality | 0.68 | 0.51 | +0.17 | ⚠ |
| Personality | 0.42 | 0.71 | -0.29 | ⚠ |
| Audience | intermediate | intermediate | 0 | ✓ |

**Outlier Score:** 0.38 (BORDERLINE)
**Decision:** INCLUDE WITH NOTE

**Note:** This file has noticeably lower personality than the baseline.
This may indicate:
- Different section type (reference vs. narrative)
- Different author
- Content targeting different context

### Profile Update (applied)

| Parameter | Before | After | Change |
|-----------|--------|-------|--------|
| Formality | 0.51 | 0.53 | +0.02 |
| Personality | 0.71 | 0.68 | -0.03 |

**Cumulative:** 6,237 words from 6 files (0 excluded)

---
```

#### Outlier File (score >= 0.5)

```markdown
---
**[8/15] Processing:** docs/api-reference.md (823 words)

### File Analysis

| Parameter | File Value | Profile | Difference | Flag |
|-----------|------------|---------|------------|------|
| Formality | 0.85 | 0.54 | +0.31 | OUTLIER |
| Personality | 0.18 | 0.69 | -0.51 | OUTLIER |
| First person | No | Yes | — | ⚠ |
| Contractions | No | Yes | — | ⚠ |
| Audience | expert | intermediate | 1 | ✓ |
| Avg length | 22 | 17.5 | +4.5 | ✓ |

**Outlier Score:** 0.72 (OUTLIER)
**Decision:** SKIP

**Reasons:**
- Formality differs by 0.31 (threshold: 0.30)
- Personality differs by 0.51 (threshold: 0.30)
- Appears to be reference documentation vs. narrative content

### Profile: UNCHANGED

**Cumulative:** 6,237 words from 6 files (1 excluded)

---
```

### Final Summary

After processing all files:

```markdown
---

## Incremental Processing Complete

**Files processed:** 15
**Files included:** 12 (80%)
**Files excluded:** 3 (20%)

### Excluded Files

| File | Outlier Score | Primary Reason |
|------|---------------|----------------|
| docs/api-reference.md | 0.72 | Reference style (formal, low personality) |
| docs/changelog.md | 0.65 | Changelog format (no prose patterns) |
| docs/license.md | 0.81 | Legal text (very formal) |

### Profile Evolution

| Parameter | Baseline | Final | Total Change |
|-----------|----------|-------|--------------|
| Formality | 0.52 | 0.54 | +0.02 |
| Personality | 0.72 | 0.68 | -0.04 |
| Avg length | 18 | 17.2 | -0.8 |

**Final corpus:** 9,847 words from 12 files

---
```

## Analysis Algorithm

For each parameter, analyze the corpus and calculate values:

### 1. Formality (0.0-1.0)

**Indicators analyzed:**

| Indicator | Casual (→ 0.0) | Formal (→ 1.0) |
|-----------|----------------|----------------|
| Contractions | High ratio (don't, can't) | Low ratio (do not, cannot) |
| Passive voice | Rare | Frequent |
| Vocabulary | Simple, everyday words | Technical, sophisticated |
| Sentence starters | "So", "Well", "And" | "Furthermore", "Additionally" |
| Exclamations | Present | Absent |

**Calculation:**
```
formality = (formal_indicators / total_indicators)
```

### 2. Personality (0.0-1.0)

**Indicators analyzed:**

| Indicator | Neutral (→ 0.0) | Engaged (→ 1.0) |
|-----------|-----------------|-----------------|
| Opinion markers | None | "I think", "I believe", "in my view" |
| Value judgments | Absent | "excellent", "poor", "fascinating" |
| Reactions | None | "surprisingly", "importantly", "notably" |
| Questions | None | Rhetorical questions present |
| Personal references | None | Experience mentions, anecdotes |

**Calculation:**
```
personality = (personality_markers / sentences) * scaling_factor
```

### 3. First Person Usage

Detect presence of first-person pronouns:
- Singular: I, my, me, mine
- Plural: we, our, us, ours

**Result:** `true` if > 5% of sentences contain first-person pronouns

### 4. Contractions

Count contracted vs. expanded forms:

| Contracted | Expanded |
|------------|----------|
| don't | do not |
| can't | cannot |
| won't | will not |
| it's | it is |
| we're | we are |
| they're | they are |

**Result:** `true` if contractions > 50% of total opportunities

### 5. Audience Level

Analyze technical complexity:

| Level | Indicators |
|-------|------------|
| beginner | Extensive explanations, simple vocabulary, many examples |
| intermediate | Moderate explanation, some assumed knowledge |
| expert | Minimal explanation, domain jargon, assumed expertise |

**Calculation:** Based on explanation ratio and vocabulary complexity

### 6. Sentence Patterns

#### Average Length Target
```
avg_length_target = sum(sentence_word_counts) / sentence_count
```

#### Variation Level
Calculate standard deviation of sentence lengths:
- low: std_dev < 4
- moderate: 4 ≤ std_dev < 8
- high: std_dev ≥ 8

#### Mix Short Sentences
```
mix_short = (sentences < 8 words) / total_sentences > 0.15
```

#### Rhetorical Questions
Detect question marks in declarative contexts (not actual questions needing answers).

### 7. Pronoun Balance

Calculate you vs. we ratio:
```
you_count = count("you", "your", "yours")
we_count = count("we", "our", "ours", "us")
total = you_count + we_count

you_percentage = (you_count / total) * 100
we_percentage = (we_count / total) * 100
```

### 8. Elaboration Depth

| Depth | Indicators |
|-------|------------|
| minimal | Short paragraphs, bullet points, quick statements |
| moderate | Some explanation, occasional examples |
| thorough | Detailed explanations, multiple examples, context |

Analyze based on:
- Average paragraph length
- Presence of example patterns ("for example", "such as", "e.g.")
- Explanation markers ("because", "since", "the reason is")

#### Analogy Usage

Detect how frequently analogies are used to explain concepts:

| Level | Indicators | Detection Patterns |
|-------|------------|-------------------|
| none | No analogies | No comparison patterns found |
| rare | Occasional analogy | 1-2 per 1000 words |
| moderate | Regular use | 3-5 per 1000 words |
| frequent | Heavy reliance | >5 per 1000 words |

**Detection patterns:**
- Explicit comparisons: "like", "similar to", "just as", "think of it as"
- Metaphors: "is a", "acts as", "serves as" (in explanatory context)
- Analogy markers: "imagine", "picture", "consider", "suppose"
- Domain bridges: "in the same way that", "much like", "comparable to"
- Familiar references: "like a [everyday object]", "think of [concept] as [familiar thing]"

**Also capture analogy domain** when patterns are detected:
- Technical-to-everyday (explaining code like cooking)
- Cross-domain technical (databases like filing cabinets)
- Physical-to-abstract (memory like a warehouse)
- Social/human (services like employees)

### 9. Personality Traits

| Trait | Detection |
|-------|-----------|
| opinions | Opinion verbs: "I think", "I believe", "I recommend" |
| acknowledge_complexity | Hedging: "however", "although", "on the other hand" |
| humor | Informal asides, parenthetical comments, wordplay |
| personal_experience | "In my experience", "I've found", "when I worked on" |

### 10. Signature Phrases

Extract top 5 repeated sentence openers (first 3-4 words):
1. Count frequency of sentence beginnings
2. Filter out generic openers ("The", "This", "It")
3. Rank by frequency
4. Return top 5 distinctive openers

### 11. Tone Description

Synthesize a prose description that captures the voice's emotional quality and unique character. This goes beyond the quantitative parameters to describe how the writing *feels*.

**Elements to consider:**

| Category | Examples |
|----------|----------|
| **Emotional warmth** | warm, distant, encouraging, neutral, empathetic, detached |
| **Authority stance** | confident, humble, authoritative, collaborative, deferential |
| **Intellectual style** | curious, pragmatic, analytical, intuitive, rigorous, exploratory |
| **Energy level** | energetic, calm, urgent, patient, measured, enthusiastic |
| **Relationship to reader** | mentoring, peer-to-peer, expert-to-novice, collaborative, instructive |
| **Attitude toward subject** | passionate, objective, skeptical, optimistic, critical, appreciative |

**Synthesis approach:**

1. Review the extracted parameters holistically
2. Identify the dominant emotional register from word choices and sentence patterns
3. Note any tension or contrast (e.g., "formal but warm", "casual yet authoritative")
4. Capture what makes this voice distinctive compared to generic technical writing
5. Write prose that someone could read and immediately understand the voice's character

**Example tone descriptions:**

*Technical tutorial voice:*
> This voice combines technical precision with genuine warmth. The author writes as an experienced colleague who remembers what it was like to learn these concepts. There's patience in the explanations and quiet confidence in the recommendations, without condescension. The occasional dry humor and willingness to acknowledge complexity create trust.

*Opinionated blog voice:*
> Direct and unapologetic, this voice takes clear positions and defends them with evidence. The writing has intellectual energy and a sense of urgency about getting things right. While confident, it acknowledges counterarguments fairly. The reader feels engaged in a substantive conversation rather than lectured at.

*Reference documentation voice:*
> Precise and economical, this voice prioritizes clarity over personality. Information is organized for quick retrieval rather than narrative flow. The tone is professional and neutral, creating confidence through consistency and completeness rather than personal engagement.

## Confidence Scoring

Rate each parameter extraction with confidence:

| Confidence | Corpus Size | Reliability |
|------------|-------------|-------------|
| HIGH | > 5000 words | Very reliable |
| MEDIUM | 1000-5000 words | Reasonably reliable |
| LOW | < 1000 words | Use with caution |

Display confidence per parameter based on:
- Corpus size
- Consistency of pattern
- Number of data points

## Extraction Workflow

### Step 1: Collect and Assess Content

```markdown
## Voice Extraction

**Source:** [source path or pattern]

| Metric | Value |
|--------|-------|
| Files found | [count] |
| Total words | [count] |
| Corpus confidence | [HIGH/MEDIUM/LOW] |
```

**Mode selection:**
- If 1 file OR total words < 1000: Use **single-pass mode**
- Otherwise: Use **incremental mode** with representative sampling

### Step 2: Select Processing Mode

#### Single-Pass Mode (1 file or < 1000 words)

```markdown
**Processing mode:** Single-pass (small corpus)

Analyzing all content as unified corpus...
```

Proceed directly to Step 3 (Present Analysis).

#### Incremental Mode (multiple files >= 1000 words)

```markdown
**Processing mode:** Incremental with representative sampling

Scoring [N] files for baseline selection...
```

**2a. Score all files** using the representative sample selection algorithm.

**2b. Select baseline files:**

```markdown
## Representative Sample Selection

**Selected baseline files:**

| Rank | File | Words | Score | Rationale |
|------|------|-------|-------|-----------|
| 1 | [file] | [words] | [score] | [reason] |
| 2 | [file] | [words] | [score] | [reason] |

**Baseline corpus:** [total] words from [N] files

---
```

**2c. Extract baseline profile** from selected files.

**2d. Process remaining files** one by one:

For each file (sorted by score, descending):

1. Extract voice parameters from file
2. Compare to current profile
3. Calculate outlier score
4. Display iteration output (see Display Formats section)
5. If CONSISTENT or BORDERLINE: merge into profile
6. If OUTLIER: skip and note exclusion

**2e. Display final summary:**

```markdown
## Incremental Processing Complete

**Files processed:** [total]
**Files included:** [N] ([%])
**Files excluded:** [N] ([%])

[If any excluded, show excluded files table]

### Profile Evolution

| Parameter | Baseline | Final | Total Change |
|-----------|----------|-------|--------------|
| Formality | [val] | [val] | [change] |
| Personality | [val] | [val] | [change] |
| Avg length | [val] | [val] | [change] |

**Final corpus:** [words] words from [N] files
```

### Step 3: Present Analysis

Use this format for presenting extracted parameters:

```markdown
## Extracted Voice Profile

Based on analysis of [X] words from [Y] files.

### Core Characteristics

| Parameter | Value | Confidence | Evidence |
|-----------|-------|------------|----------|
| Formality | 0.65 | HIGH | 23% contractions, moderate formal vocabulary |
| Personality | 0.72 | HIGH | 18 opinion markers, 12 value judgments |
| First Person | Yes | HIGH | Found in 34% of sentences |
| Contractions | Yes | HIGH | 78% use contractions |
| Audience | intermediate | MEDIUM | Technical terms with explanations |

### Sentence Patterns

| Parameter | Value | Confidence | Evidence |
|-----------|-------|------------|----------|
| Avg Length | 16 words | HIGH | Calculated from 342 sentences |
| Variation | moderate | HIGH | Std dev = 5.2 |
| Mix Short | Yes | MEDIUM | 19% sentences < 8 words |
| Rhetorical Qs | No | HIGH | 0 rhetorical questions found |

### Pronoun Balance

| Pronoun | Percentage | Confidence |
|---------|------------|------------|
| you | 65% | HIGH |
| we | 35% | HIGH |

### Elaboration Style

| Parameter | Value | Confidence |
|-----------|-------|------------|
| Depth | moderate | MEDIUM |
| Context | Yes | HIGH |
| Examples | Occasional | MEDIUM |
| Reasoning | Yes | HIGH |

### Personality Traits

| Trait | Value | Confidence |
|-------|-------|------------|
| Opinions | Yes | HIGH |
| Complexity | Yes | MEDIUM |
| Humor | none | HIGH |
| Experience | No | HIGH |

### Signature Phrases (Top 5)

1. "Let's look at" (23 occurrences)
2. "The key point is" (18 occurrences)
3. "Worth noting" (15 occurrences)
4. "In practice" (12 occurrences)
5. "Consider how" (9 occurrences)

### Tone Description

> This voice balances technical authority with accessible warmth. The author writes
> as a knowledgeable peer who genuinely wants readers to succeed, offering clear
> explanations without condescension. There's intellectual curiosity in the approach,
> treating complex topics as interesting puzzles rather than obstacles. The occasional
> personal aside and willingness to acknowledge trade-offs create authenticity.

### Phrases to Avoid (detected anti-patterns)

- None detected that conflict with voice

---

**Overall Confidence:** HIGH
Based on sufficient corpus size and consistent patterns.
```

### Step 4: Prompt for Name

Use AskUserQuestion:

```json
{
  "question": "What would you like to name this voice profile?",
  "header": "Profile Name",
  "options": [
    {"label": "Suggest name", "description": "Based on characteristics: [suggested-name]"},
    {"label": "Custom name", "description": "Enter your own profile name"}
  ]
}
```

Suggest a name based on detected characteristics:
- High formality + low personality → "formal-reference"
- Low formality + high personality → "casual-conversational"
- Balanced → "balanced-technical"
- High personality + opinions → "opinionated-[topic]"

### Step 5: Choose Storage Location

Use AskUserQuestion:

```json
{
  "question": "Where should I save this voice profile?",
  "header": "Location",
  "options": [
    {"label": "Global (Recommended)", "description": "~/.claude/style/voices/ - Available across all projects"},
    {"label": "Project", "description": ".style/voice.yaml - Only for this project"}
  ]
}
```

### Step 6: Save Profile

Write the complete YAML profile:

```yaml
# Voice Profile: [name]
# Extracted from: [source files]
# Extraction date: [date]
# Corpus: [X] words from [Y] files

name: "[name]"
version: "1.0"
description: "[auto-generated description based on characteristics]"

# Prose description of the voice's tone and feel
# Captures emotional quality, overall impression, and unique character
tone_description: |
  [Prose describing the voice's emotional quality, feel, and unique character.
  Goes beyond statistics to capture the human essence of the writing style.
  May include: warmth, authority, curiosity, playfulness, confidence, empathy,
  intellectual rigor, accessibility, urgency, patience, encouragement, skepticism, etc.]

characteristics:
  formality: [value]
  personality: [value]
  first_person: [true/false]
  contractions: [true/false]
  audience: "[beginner/intermediate/expert]"

sentence_patterns:
  mix_short: [true/false]
  max_consecutive_similar: 3
  avg_length_target: [value]
  variation: "[low/moderate/high]"
  rhetorical_questions: [true/false]

elaboration:
  depth: "[minimal/moderate/thorough]"
  provide_context: [true/false]
  include_examples: [true/false]
  explain_reasoning: [true/false]
  analogies: "[none/rare/moderate/frequent]"
  analogy_domain: "[optional: primary domain for analogies, e.g., 'everyday objects', 'cooking', 'construction']"

personality_traits:
  opinions: [true/false]
  acknowledge_complexity: [true/false]
  humor: "[none/subtle/moderate]"
  personal_experience: [true/false]

pronoun_balance:
  you_percentage: [value]
  we_percentage: [value]

signature_phrases:
  - "[phrase 1]"
  - "[phrase 2]"
  - "[phrase 3]"
  - "[phrase 4]"
  - "[phrase 5]"

avoid_phrases:
  - "It goes without saying"
  - "As everyone knows"
  - "Obviously"
```

### Step 7: Confirm Creation

```markdown
✓ Created voice profile: [name]

**Location:** [path]

**Summary:**
- Formality: [value] ([descriptor])
- Personality: [value] ([descriptor])
- Pronouns: [you]% you / [we]% we
- Style: [brief description]

**To use this profile:**
- Apply to project: `/prose:voice apply [name]`
- Generate content: `/prose:write` (auto-applies if set as project voice)
- View details: `/prose:voice show [name]`
```

## Edge Cases

### Single File Extraction

When only one file is provided:

```markdown
**Processing mode:** Single file

**Note:** Single-file extraction has reduced confidence. Consider providing
additional samples for more reliable voice capture.

Proceeding with standard extraction...
```

- Skip representative selection (no selection needed)
- Process with standard single-pass extraction
- Mark all confidence scores as one level lower than corpus size would indicate
- Note in output that results may be less stable

### Small Corpus (< 500 words)

```markdown
⚠️ Warning: Small corpus detected ([X] words)

Voice extraction works best with larger samples. Results may be less reliable.

Options:
1. Proceed anyway (results will have LOW confidence)
2. Add more content to the analysis
3. Cancel extraction
```

### All Outliers After Baseline

If more than 5 consecutive files are flagged as outliers after establishing baseline:

```markdown
⚠️ Warning: Consecutive outlier limit reached

After processing [N] files, [M] consecutive files have been flagged as outliers.
This suggests the baseline may not represent the majority of your content.

**Possible causes:**
- Baseline files have unusual style compared to rest of corpus
- Content contains multiple distinct voices/authors
- Mixed document types (narrative + reference + changelog)

**Options:**
1. **Accept baseline** - Use current profile from [N] included files
2. **Re-select baseline** - Choose different representative files
3. **Relax thresholds** - Include borderline files more liberally
4. **Split extraction** - Create separate profiles for different document types
```

Use AskUserQuestion to let user choose:

```json
{
  "question": "Many files don't match the baseline voice. How should I proceed?",
  "header": "Outlier Limit",
  "options": [
    {"label": "Accept baseline", "description": "Keep profile from [N] matching files"},
    {"label": "Re-select baseline", "description": "Let me choose different representative files"},
    {"label": "Relax thresholds", "description": "Include more files even if they differ"},
    {"label": "Split by type", "description": "Create separate profiles for different content types"}
  ]
}
```

### Multi-Author Detection

When boolean fields show approximately 50% splits or categorical fields have multiple strong candidates:

```markdown
⚠️ Warning: Inconsistent patterns detected

Analysis suggests mixed authorship or intentionally varied style:

| Parameter | Distribution | Confidence |
|-----------|--------------|------------|
| First person | 52% yes / 48% no | LOW |
| Contractions | 47% yes / 53% no | LOW |
| Audience | 40% intermediate, 35% expert, 25% beginner | LOW |

**This may indicate:**
- Multiple authors with different styles
- Content evolved over time
- Intentional variation by section type

**Recommendation:** Consider extracting from a subset of files by the same author
or content type for more consistent results.
```

### Empty or Unparseable Files

Track files that cannot be processed separately from outliers:

```markdown
**Skipped files (not counted as outliers):**

| File | Reason |
|------|--------|
| docs/logo.png | Binary file (not text) |
| docs/data.json | No prose content detected |
| docs/snippet.md | Too short (38 words, minimum: 50) |

These files are excluded from analysis but do not affect outlier statistics.
```

**Skip criteria:**
- Binary files (images, PDFs without text extraction, etc.)
- Files with < 50 words of prose content
- Files that are primarily code (>80% code blocks)
- Files that are primarily structured data (JSON, YAML, tables only)

### Inconsistent Patterns (Legacy Behavior)

If patterns conflict (e.g., some files formal, others casual) in single-pass mode:

```markdown
⚠️ Inconsistent patterns detected

The analyzed content shows varying styles:
- Files 1-3: Formal (formality ~0.8)
- Files 4-5: Casual (formality ~0.3)

This may indicate:
- Multiple authors
- Different content types
- Style evolution over time

Recommendation: Extract from a more consistent subset of files.
```

**Note:** In incremental mode, this is handled automatically through outlier detection.

### No Clear Patterns

If writing is too generic to extract distinctive patterns:

```markdown
ℹ️ Generic writing style detected

The analyzed content doesn't show distinctive voice characteristics.
All parameters fall near default/neutral values.

This could mean:
- The writing intentionally avoids strong voice
- The content is reference/specification style
- More distinctive samples are needed

A "reference" style profile will be created with neutral settings.
```

## Integration

This skill complements voice-architect:
- **voice-architect**: Create voice profiles interactively through questions
- **voice-extractor**: Derive voice profiles from existing writing samples

Both produce the same YAML format, usable with:
- `/prose:voice apply`
- `/prose:write` (auto-applies project voice)
- content-generator skill (loads active voice)

---

**Remember:** The goal is to capture authentic voice from real writing, enabling consistent personality across future content. Extract what makes the writing distinctive, not just average metrics.
