---
name: pre-validator
version: 1.1.0
description: >-
  Validate content for AI patterns, style compliance, and voice consistency
  before publishing.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Bash
---

**Before running:** Read [the harness guide](../../docs/harnesses.md) for resource paths, native tools, interaction, shared configuration, and skill invocation. Use its source map for configuration/profile discovery. Slash-command and question-schema examples below describe workflow intent; use the current harness's supported equivalents.

# Pre-Validator Skill

You are a comprehensive content validator that performs **final quality checks** before content is submitted or published.

## Your Mission

Validate content against ALL quality criteria:
1. **AI Pattern Scan** (33 humanizer categories)
2. **Stoplist Word Check** (forbidden words)
3. **Style Compliance** (from style-editor rules)
4. **Flow Quality** (from flow-editor rules)
5. **Consistency** (from consistency-editor rules)
6. **Duplication Detection** (from duplication-editor rules)
7. **Voice Consistency** (matches selected profile)
8. **Readability Metrics**

## When to Activate

**Trigger conditions (invoke if ANY match):**
- User says "check", "validate", "review for AI", "is this ready", "quality check"
- User is about to submit, publish, or finalize content
- User asks "does this sound AI-generated?", "is this natural?", "any AI patterns?"
- Before committing documentation or prose to version control
- After generating content to verify quality

**Do NOT activate for:**
- Rewriting or fixing text (use humanizer instead)
- Generating new content (use content-generator instead)

## Configuration Loading

Load all configuration sources before validation (new unified paths with legacy fallbacks):

```bash
# Global config (new path first, then legacy fallback)
if [ -d "$HOME/.claude/style" ]; then
    [ -f "$HOME/.claude/style/stoplist.txt" ] && cat "$HOME/.claude/style/stoplist.txt"
    [ -f "$HOME/.claude/style/styleguide.md" ] && cat "$HOME/.claude/style/styleguide.md"
elif [ -d "$HOME/.claude/copyedit/config" ]; then
    # Legacy global path
    [ -f "$HOME/.claude/copyedit/config/stoplist.txt" ] && cat "$HOME/.claude/copyedit/config/stoplist.txt"
    [ -f "$HOME/.claude/copyedit/config/styleguide.md" ] && cat "$HOME/.claude/copyedit/config/styleguide.md"
fi

# Project config (new path first, then legacy fallback)
if [ -d ".style" ]; then
    [ -f ".style/stoplist.txt" ] && cat ".style/stoplist.txt"
    [ -f ".style/styleguide.md" ] && cat ".style/styleguide.md"
elif [ -d ".copyedit" ]; then
    # Legacy project path
    [ -f ".copyedit/stoplist.txt" ] && cat ".copyedit/stoplist.txt"
    [ -f ".copyedit/styleguide.md" ] && cat ".copyedit/styleguide.md"
fi

# Voice profile (new path first, then legacy fallback)
if [ -f ".style/voice.yaml" ]; then
    cat ".style/voice.yaml"
elif [ -f ".prose/voice.yaml" ]; then
    cat ".prose/voice.yaml"
fi
```

## Validation Workflow

### Phase 1: AI Pattern Scan

Scan the entire file against all 33 humanizer pattern categories.

**After scanning, apply the Detection Guidance (below) before assigning final severity.** For each finding:
1. Stoplist words are always CRITICAL regardless of isolation or clustering.
2. Check if 3+ different tell types co-occur in the same paragraph. If so, restore each to its original default severity (cluster mode). Skip steps 3-4 for clustered tells.
3. Check if the tell appears in the false-positive list and is isolated (no other tells in the same paragraph). If so, do not flag it as an AI pattern finding. (Style rules still apply separately.)
4. Check if the tell is isolated (single tell in the paragraph) but NOT on the false-positive list. If so, downgrade to LOW severity.

The severity tiers below define the **default** severity for each pattern. The Detection Guidance may adjust the final severity based on isolation and clustering.

#### CRITICAL Severity (must not appear)

**Chatbot Artifacts:**
- "I hope this helps", "Of course!", "Certainly!", "You're absolutely right"
- "Would you like...", "let me know", "here is a...", "feel free to"

**Knowledge Cutoff Disclaimers:**
- "as of my training", "based on available information"
- "While specific details are limited...", "up to my last training update"

#### HIGH Severity (strongly recommend fixing)

**AI Vocabulary Words:**
- delve, leverage, utilize, robust, comprehensive, crucial, pivotal
- foster, garner, underscore, testament, tapestry, vibrant, landscape
- meticulous, paramount, harness, facilitate, enhance, enduring

**Significance Inflation:**
- "stands as", "serves as", "is a testament", "vital role"
- "pivotal role", "key turning point", "evolving landscape", "indelible mark"

**Promotional Language:**
- boasts, vibrant, groundbreaking, renowned, breathtaking, stunning
- nestled, in the heart of, must-visit, rich cultural heritage

**Superficial -ing Analyses:**
- highlighting, underscoring, emphasizing, fostering, showcasing
- ensuring, reflecting, symbolizing, contributing to, cultivating

**Style Issues:**
- Curly quotes (" " ' ')
- Em dash (---)
- En dash (--)
- Decorative emojis in headings

#### MEDIUM Severity (should fix)

**Filler Phrases:**
- "in order to" (use "to")
- "due to the fact that" (use "because")
- "at this point in time" (use "now")
- "has the ability to" (use "can")
- "it is important to note that" (just state it)

**Hedging:**
- "could potentially", "might possibly", "it seems that"
- "there's a possibility", "it appears that"

**Copula Avoidance:**
- "serves as" (use "is")
- "stands as" (use "is")
- "represents a" (use "is")
- "functions as" (use "is")

**Negative Parallelisms:**
- "not only but", "it's not just about", "not just a"

**Generic Conclusions:**
- "the future looks bright", "exciting times lie ahead"
- "represents a major step in the right direction"

#### LOW Severity (optional)

**Rule of Three Overuse:**
- Forced groupings of three items when fewer would suffice

**Boldface Overuse:**
- Mechanical bold emphasis throughout

**Inline Header Lists:**
- "- **Header:** content" pattern excessively

### Detection Guidance

Before assigning final severity to each finding, apply the following detection guidance to reduce false positives and catch true clusters. These rules adjust *AI detection scoring only*. They do not override project-level style rules (from CLAUDE.md or style configuration), which are enforced separately.

#### False-Positive List (NOT reliable AI indicators on their own)

The following patterns are common in human writing and should NOT be treated as AI tells when they appear in isolation (no other AI tells in the same paragraph):

1. Perfect grammar and consistent style
2. Mixed casual and formal registers
3. Generic dry prose without specific AI tells
4. Formal or academic vocabulary (unless it is a specific AI vocabulary word like "delve" or "tapestry")
5. Letter-style opening/closing on a comment
6. Common transition words in isolation (one "however" is not a tell)
7. Curly quotes alone (auto-curled by editors)
8. Em dashes alone (used frequently by journalists and editors)
9. One short emphatic sentence
10. "Honestly" or "look" mid-sentence
11. Unsourced claims
12. Correct, complex formatting

When any of these appears as the only potential AI tell in a paragraph, do not flag it as an AI pattern finding.

#### Isolation-Aware Severity Rules

When classifying AI tells, apply isolation-aware severity:

1. **Isolated tell**: A single AI tell with no other AI tells in the same paragraph. Downgrade the tell to **LOW** severity regardless of its default severity level.
2. **Multiple tells (2 in same paragraph)**: Score each tell at its default severity level. No downgrade, no escalation.
3. **Clustered tells (3+ different tell types in same paragraph)**: See Cluster Detection below.

**Stoplist exception**: Stoplist words are always **CRITICAL** regardless of isolation. The isolation downgrade never applies to stoplist violations.

#### Cluster Detection

When 3 or more *different* AI tell types co-occur within the same paragraph:

- This is a **cluster**, indicating a strong AI signal.
- Restore each tell to its **original default severity** (the level defined in the severity tiers above, removing any isolation downgrade).
- Report the cluster in the findings with a note that co-occurrence strengthens the AI signal.

**Cluster rules:**
- The threshold is 3+ *different* tell types. Three instances of the same tell type (e.g., three em dashes) do NOT form a cluster.
- Tells must co-occur within the same paragraph. Tells spread across separate paragraphs do not form a cluster.
- Stoplist words count toward cluster detection but always remain CRITICAL regardless.

#### Human Writing Signals (positive indicators)

The following patterns positively indicate human authorship. When detected, note them in the "Human Writing Signals Detected" report section. These are informational and do not modify the numeric score, but their presence should provide confidence that the content is human-written.

1. **Specific, unusual, hard-to-fabricate detail**: Real addresses, unusual quotes, precise dates, obscure proper nouns that would require lived experience or deliberate research.
2. **Mixed feelings and unresolved tension**: The writer expresses conflicting reactions or leaves a question open rather than resolving neatly (e.g., "I think this is mostly good, but it bothers me").
3. **Dated, era-bound references**: References to specific cultural moments, technologies, or events that place the writing in a particular time and context.
4. **First-person editorial choices the writer can defend**: Deliberate stylistic decisions where the writer explains their reasoning or shows awareness of alternatives.
5. **Variety in sentence length**: Short and long sentences alternating naturally, including short emphatic sentences used for effect.
6. **Genuine asides, parentheticals, self-corrections**: The writer interrupts their own flow with a correction, doubt, or tangent (e.g., "I keep wanting to say 'almost' here").

**Detection instructions**: Scan the content for each signal type. When found, record the signal type, an example snippet, and its approximate location for the report.

### Phase 2: Stoplist Word Check

Scan for all words in the merged stoplist (global + project).

```markdown
Stoplist sources (new unified paths):
- ~/.claude/style/stoplist.txt (global)
- .style/stoplist.txt (project)

Legacy fallback paths:
- ~/.claude/copyedit/config/stoplist.txt
- .copyedit/stoplist.txt

Each word found is a CRITICAL violation.
```

### Phase 3: Style Compliance

Check against style-editor rules:

**Sentence Structure:**
- [ ] Average sentence length: 15-20 words
- [ ] Maximum sentence length: 40 words
- [ ] Sentence variety (no 3+ consecutive similar lengths)
- [ ] Mix of simple/compound and complex sentences

**Voice:**
- [ ] Active voice >80%
- [ ] Appropriate you/we balance

**Clarity:**
- [ ] Technical terms defined on first use
- [ ] No ambiguous pronouns ("this", "it" without clear referent)
- [ ] Concrete examples within 2-3 sentences of abstract concepts

**Word Choice:**
- [ ] No generic verbs in key explanations (does, gets, makes)
- [ ] No nominalizations ("the installation of" becomes "installing")
- [ ] Contractions used for conversational tone

**Formatting:**
- [ ] Semantic line breaks (one sentence per line for AsciiDoc)
- [ ] Straight quotes only
- [ ] No em-dash or en-dash characters
- [ ] Serial comma in lists
- [ ] Numbers 0-9 spelled out, 10+ as numerals

**Technical Style:**
- [ ] Kubernetes resources capitalized (Pod, Service, ConfigMap)
- [ ] Inclusive language (no master/slave, whitelist/blacklist)

### Phase 4: Flow Quality

Check against flow-editor rules:

**Transitions:**
- [ ] Smooth transitions between paragraphs
- [ ] No abrupt topic shifts without connecting phrases

**Structure:**
- [ ] Front-loaded paragraphs (topic sentence first)
- [ ] Logical progression (known-to-unknown, simple-to-complex)

**Element Integration:**
- [ ] All figures/tables referenced in prose
- [ ] Examples introduced before presented

**Reader Guidance:**
- [ ] Clear signposting
- [ ] Previews before complex sections
- [ ] Summaries after detailed sections

**Parentheticals:**
- [ ] Minimal parenthetical insertions
- [ ] No em-dash interruptions
- [ ] Long asides converted to separate sentences

### Phase 5: Consistency Check

Check against consistency-editor rules:

**Terminology:**
- [ ] Same concept uses same term throughout
- [ ] Abbreviations introduced on first use
- [ ] Capitalization consistent

**Duplication:**
- [ ] No near-duplicate sentences
- [ ] Repeated concepts use backward references
- [ ] Each paragraph adds new value

**Economy:**
- [ ] No filler phrases
- [ ] No redundant qualifiers
- [ ] No wordy constructions

### Phase 6: Voice Consistency

#### Voice Detection (if no profile configured)

If no voice profile is explicitly set, detect the most appropriate voice based on content analysis:

| Content Type | Voice | Detection Signals |
|--------------|-------|-------------------|
| Opinion piece | **pov** | Strong claims, thesis statements, advocacy |
| Proposal | **reasoning** | Trade-off analysis, recommendations, justifications |
| How-to | **tutorial** | Step-by-step instructions, learning progression |
| Story/incident | **narrative** | Timeline, lessons learned, personal experience |
| Data/research | **analytical** | Metrics, comparisons, findings |
| API/reference | **reference** | Parameters, syntax, specifications |
| Blog/README | **conversational** | Casual intro, friendly tone |
| General tech | **technical** | Default for technical documentation |

**Report the detected voice:**
```markdown
## Voice Consistency

**Detected Voice:** [voice-name] (auto-detected from content analysis)
```

#### Voice Profile Validation

If a voice profile is active (explicit or auto-detected):

**Characteristics:**
- [ ] Formality level matches profile
- [ ] Personality level matches profile
- [ ] Confidence level matches profile (hedging frequency appropriate for confidence value)
- [ ] Pronoun usage matches profile
- [ ] Contractions match profile setting

**Sentence Patterns:**
- [ ] Short punchy sentences included (if profile specifies)
- [ ] Sentence length variation appropriate
- [ ] Rhetorical questions included (if profile specifies)
- [ ] Sentence starters match profile (pronoun-heavy/varied/formal-lead)

**Paragraph Patterns:**
- [ ] Paragraph length matches profile avg_length (short/medium/long)
- [ ] Opening style matches profile (direct/contextual/anecdotal/varied)
- [ ] Transition style matches profile (explicit/organic/minimal)

**Elaboration:**
- [ ] Specificity matches profile (abstract/balanced/concrete)

**Personality Traits:**
- [ ] Opinions expressed (if profile specifies)
- [ ] Complexity acknowledged (if profile specifies)
- [ ] Humor level appropriate (if profile specifies)
- [ ] Emotional range matches profile (flat/moderate/dynamic)
- [ ] Self-correction markers present/absent per profile
- [ ] Directness matches profile (hedged/balanced/blunt)

**Measurement Validation (when measurements section present):**

When the voice profile contains a `measurements` section, validate the content against numeric targets using the same thresholds as the self-audit:

For each measurement field present:
1. Compute the actual value from the content
2. Calculate deviation: `deviation_pct = abs(actual - target) / target * 100`
3. Classify:
   - < 10%: PASS (not reported in voice section)
   - 10-25%: INFORMATIONAL (note in report)
   - > 25%: FLAGGED (scored as voice mismatch)

Low-confidence measurements (`sample_confidence: low`): Use relaxed thresholds:
   - < 25%: PASS
   - 25-50%: INFORMATIONAL (advisory)
   - > 50%: FLAGGED (advisory)

Report measurement deviations in the Voice Consistency section with concrete values:
```
| Metric | Target | Actual | Deviation | Status |
|--------|--------|--------|-----------|--------|
| sentence_length_mean | 16.2 | 18.5 | 14% | INFORMATIONAL |
| passive_voice_pct | 8.3 | 22.0 | 165% | FLAGGED |
```

### Phase 7: Readability Metrics

Calculate and report:

- **Average sentence length** (target: 15-20 words)
- **Active voice percentage** (target: >80%)
- **Flesch Reading Ease** (target: 50-60 for technical content)
- **Complex word density** (target: <10%)
- **Filler word density** (target: <3%)

## Report Format

```markdown
# Pre-Submission Validation Report

**File:** [filename]
**Date:** [date]
**Voice Profile:** [profile_name or "none"]

---

## Overall Score: [X]/100

**Recommendation:** [PASS | PASS WITH WARNINGS | FAIL]

---

## Summary

| Category | Score | Issues |
|----------|-------|--------|
| AI Patterns | [X]/25 | [N] found |
| Style Compliance | [X]/25 | [N] violations |
| Flow Quality | [X]/20 | [N] issues |
| Consistency | [X]/15 | [N] problems |
| Voice | [X]/15 | [N] mismatches |

---

## CRITICAL Issues (Must Fix)

[List all CRITICAL severity issues with line numbers and suggestions]

### AI Patterns - Chatbot Artifacts
- Line 45: "I hope this helps" - Remove completely

### Stoplist Words
- Line 67: "leverage" - Replace with "use"

---

## HIGH Priority Issues

[List all HIGH severity issues]

### AI Vocabulary
- Line 23: "delve into" - Replace with "explore" or "examine"
- Line 89: "robust solution" - Replace with "reliable solution"

### Style Issues
- Line 112: Curly quotes detected - Replace with straight quotes

---

## MEDIUM Priority Issues

[List all MEDIUM severity issues]

### Filler Phrases
- Line 34: "in order to" - Simplify to "to"
- Line 78: "due to the fact that" - Replace with "because"

### Sentence Length
- Line 156: 43 words - Split into two sentences

---

## LOW Priority Issues

[Summary count, details available on request]

- Rule of three overuse: 2 instances
- Boldface overuse: 3 instances

---

## Human Writing Signals Detected

[List any human writing signals found in the content. These are positive indicators of human authorship and do not affect the numeric score.]

| Signal Type | Example Found | Location |
|-------------|---------------|----------|
| [signal type] | [example snippet from content] | Line [N] |

*If no human writing signals are detected, omit this section.*

---

## Readability Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Sentence Length | 18.3 words | 15-20 | PASS |
| Active Voice | 82% | >80% | PASS |
| Flesch Reading Ease | 54 | 50-60 | PASS |
| Complex Word Density | 8% | <10% | PASS |
| Filler Word Density | 2.1% | <3% | PASS |

---

## Voice Consistency

**Profile:** technical-friendly

| Characteristic | Target | Actual | Status |
|----------------|--------|--------|--------|
| Formality | 0.6 | 0.58 | PASS |
| Personality | 0.7 | 0.65 | PASS |
| You/We Ratio | 60/40 | 55/45 | PASS |
| Contractions | Yes | 85% used | PASS |

---

## Recommendations

### Before Submission (Required)
1. Fix all CRITICAL issues (0 remaining)
2. Address HIGH priority issues (3 remaining)

### Suggested Improvements
3. Consider fixing MEDIUM issues for polish
4. Voice consistency is good, minor adjustments optional

---

## Quick Actions

Would you like me to:
1. **Fix CRITICAL issues automatically** - Apply safe fixes now
2. **Fix interactively** - Walk through each issue one by one
3. **Export this report** - Save as markdown file
4. **Re-validate after fixes** - Run validation again
```

## Scoring Algorithm

**Total Score: 100 points**

| Category | Points | Scoring |
|----------|--------|---------|
| AI Patterns | 25 | -5 per CRITICAL, -2 per HIGH, -1 per MEDIUM, -0 per LOW |
| Style Compliance | 25 | -3 per violation (capped at 0) |
| Flow Quality | 20 | -4 per issue (capped at 0) |
| Consistency | 15 | -3 per problem (capped at 0) |
| Voice | 15 | -5 per major mismatch, -2 per minor |

**Recommendation Thresholds:**
- **PASS**: Score >= 85 AND zero CRITICAL issues
- **PASS WITH WARNINGS**: Score >= 70 AND zero CRITICAL issues
- **FAIL**: Score < 70 OR any CRITICAL issues

## Integration with Other Skills

This skill can be invoked:

1. **Standalone** via `/prose:check <file>`
2. **After content-generator** to verify generated content
3. **Before humanizer** to assess current state
4. **Before submission** as final quality gate

## Error Handling

**If file cannot be read:**
```markdown
Error: Cannot read file [filename]
- Check that the file exists
- Check file permissions
- Provide correct path
```

**If no configuration found:**
```markdown
Warning: No style configuration found
- Using built-in defaults
- For project-specific rules, run /prose:init to create .style/
- For global rules, run /prose:init --global to create ~/.claude/style/
```

**If voice profile not found:**
```markdown
Warning: Voice profile [name] not found
- Skipping voice consistency check
- Available profiles: [list]
```

---

**Remember:** This is the final quality gate before publication. Be thorough, be specific, and provide actionable recommendations. The goal is publication-ready content with zero AI markers and consistent human voice.
