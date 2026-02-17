# Voice Auto-Detection Guide

When the voice profile is set to `auto` (or not specified), detect the appropriate voice based on the user's request and context.

**IMPORTANT:** Always announce the detected voice before generating content:
> "Using **[voice-name]** voice for this content."

## Detection Algorithm

Analyze the request for keywords, context, and intent. Match against patterns below in priority order (first match wins).

### 1. POV (Point of View)
**Confidence triggers:**
- Keywords: "opinion", "I think", "argue", "position", "stance", "take", "believe", "advocate"
- Phrases: "make a case for", "defend", "push back on", "strong view"
- Context: ADRs, position papers, op-eds, blog posts with thesis

**Announce:** `Using **pov** voice (strong opinion, advocacy).`

### 2. Reasoning
**Confidence triggers:**
- Keywords: "propose", "RFC", "design", "justify", "compare", "evaluate", "recommend"
- Phrases: "build a case", "pros and cons", "trade-offs", "which approach", "decision"
- Context: Proposals, technical decisions, architecture reviews, comparisons

**Announce:** `Using **reasoning** voice (persuasive, evidence-based).`

### 3. Tutorial
**Confidence triggers:**
- Keywords: "how to", "getting started", "learn", "step by step", "beginner", "teach", "guide"
- Phrases: "walk me through", "show me how", "explain how to", "for beginners"
- Context: Learning materials, workshops, onboarding docs

**Announce:** `Using **tutorial** voice (friendly, step-by-step).`

### 4. Narrative
**Confidence triggers:**
- Keywords: "story", "case study", "post-mortem", "experience", "happened", "incident"
- Phrases: "tell the story", "what happened", "lessons learned", "retrospective"
- Context: Incident reports, case studies, conference talks, blog stories

**Announce:** `Using **narrative** voice (storytelling, engaging).`

### 5. Analytical
**Confidence triggers:**
- Keywords: "benchmark", "performance", "data", "results", "analysis", "metrics", "measure"
- Phrases: "the numbers show", "compare performance", "analyze results"
- Context: Performance reports, research findings, data analysis

**Announce:** `Using **analytical** voice (data-driven, objective).`

### 6. Reference
**Confidence triggers:**
- Keywords: "API", "reference", "specification", "man page", "syntax", "parameters"
- Phrases: "document the API", "reference documentation", "spec for"
- Context: API docs, CLI reference, specification documents

**Announce:** `Using **reference** voice (neutral, authoritative).`

### 7. Conversational
**Confidence triggers:**
- Keywords: "blog", "casual", "friendly", "README", "intro"
- Phrases: "keep it casual", "friendly tone", "approachable"
- Context: Blog posts (general), READMEs, introductions

**Announce:** `Using **conversational** voice (casual, engaging).`

### 8. Technical (Default)
**Fallback when no strong match:**
- General technical documentation
- No specific voice indicators
- Professional context without strong personality needs

**Announce:** `Using **technical** voice (professional, balanced).`

## Priority Resolution

When multiple patterns match, use this priority:
1. Explicit user request ("use pov voice") → Use requested voice
2. Strong keyword match (3+ triggers) → Use matched voice
3. Context inference (document type) → Use contextual voice
4. Default → Technical voice

## Configuration

To enable auto-detection, set in project or global config:

```yaml
# .style/voice.yaml or ~/.claude/style/voices/default.yaml
voice: "auto"
```

Or specify a default with auto-fallback:

```yaml
voice: "technical"      # Primary voice
auto_detect: true       # Override based on context
```

## Examples

| User Request | Detected Voice | Reason |
|-------------|----------------|--------|
| "Write a blog post arguing for Rust" | pov | "arguing for" + blog context |
| "Create an RFC for the new auth system" | reasoning | "RFC" + design proposal |
| "Write a getting started guide" | tutorial | "getting started" + guide |
| "Document what happened during the outage" | narrative | "what happened" + incident |
| "Write up the benchmark results" | analytical | "benchmark results" |
| "Document the API endpoints" | reference | "API" + documentation |
| "Write a README for this project" | conversational | "README" |
| "Write documentation for this feature" | technical | Default, general docs |

## Voice Transitions

For long documents, voice may shift between sections:
- Introduction → conversational or narrative
- Technical details → technical or reference
- Recommendations → reasoning or pov
- Conclusion → matches introduction

When transitioning, announce: `Shifting to **[voice-name]** voice for this section.`
