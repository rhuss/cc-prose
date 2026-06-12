# Brainstorm: False-positive guidance and human signal preservation

**Date:** 2026-06-12
**Status:** active

## Problem Framing

Our humanizer and pre-validator can over-correct. A professional writer with polished prose, consistent style, and formal vocabulary could get flagged for AI patterns they don't have. Worse, the humanizer might sand off authentic personality markers (specific details, mixed feelings, self-corrections) that are actually strong evidence of human writing.

The upstream humanizer v2.8.0 added two sections addressing this: "What NOT to flag (false positives)" and "Signs of human writing (preserve these)." We have neither.

This is especially important for the pre-validator, which produces a numeric score. False positives inflate severity counts and can cause a FAIL recommendation on genuinely human-written content.

## Context

### Current behavior
- **Humanizer**: Scans for 24 pattern categories and rewrites all matches. No guidance on what to leave alone.
- **Pre-validator**: Scores content on a 100-point scale across 7 phases. No false-positive awareness. A single em dash in a journalist's article gets flagged as HIGH severity.
- **Content-generator**: Self-validates against humanizer patterns. Could reject its own output for patterns that are actually fine in context.

### Upstream's false-positive list (from v2.8.0)
Things that are NOT reliable AI indicators on their own:
- Perfect grammar and consistent style (could be a professional writer or editor)
- Mixed casual and formal registers (common in technical fields, neurodivergent writers)
- "Bland" or "robotic" prose (generic dryness without specific AI tells is just dry writing)
- Formal or academic vocabulary (AI overuses *specific* fancy words, not all fancy words)
- Letter-style opening/closing on a comment (predates ChatGPT by centuries)
- Common transition words in isolation (one "however" is not a tell)
- Curly quotes alone (macOS/Word/Google Docs auto-curl by default)
- Em dashes alone (journalists and editors use them frequently)
- One short emphatic sentence (humans use clipped sentences for emphasis too)
- "Honestly" or "look" mid-sentence (ordinary in casual writing)
- Unsourced claims (most of the web is unsourced)
- Correct, complex formatting (visual editors produce clean output)

### Upstream's "signs of human writing" list
Markers to preserve, not remove:
- Specific, unusual, hard-to-fabricate detail (real addresses, weird quotes)
- Mixed feelings and unresolved tension ("I think this is mostly good, but it bothers me")
- Dated, era-bound references (slang/memes from a specific year)
- First-person editorial choices the writer can defend
- Variety in sentence length (short and long alternating)
- Genuine asides, parentheticals, self-corrections ("I keep wanting to say 'almost' here")

### Key insight from upstream
> "When in doubt, look for **clusters** of tells, not isolated ones. A single em dash means nothing; em dashes plus rule-of-three plus *vibrant tapestry* plus a 'Conclusion' section is a confession."

## Approaches Considered

### A: Add guidance to all three skills (Recommended)
- Humanizer: Add "What NOT to flag" and "Signs of human writing" sections
- Pre-validator: Add false-positive awareness to severity scoring. Individual tells below MEDIUM when isolated; only escalate when clustered.
- Content-generator: Add "preserve these human signals" to self-validation

- Pros: Comprehensive, all skills benefit
- Cons: Three files to update, slight increase in skill size

### B: Add to humanizer only, reference from others
- Put the full guidance in the humanizer SKILL.md
- Pre-validator and content-generator reference "see humanizer for false-positive guidance"
- Pros: Single source of truth
- Cons: Skills should be self-contained; cross-references add cognitive load during execution

### C: Create a shared knowledge-base document
- Put false-positive guidance in `prose/knowledge-base/false-positives.md`
- All skills load it as reference material
- Pros: True single source, easy to update
- Cons: Extra file read per skill invocation, skills need to know to load it

## Decision

Approach A: Add guidance to all three skills. Each skill needs the information in its own context. The humanizer needs it to avoid over-correcting. The pre-validator needs it to avoid false FAIL scores. The content-generator needs it to avoid rejecting its own natural-sounding output. The lists are short enough that duplication is acceptable.

## Key Requirements

1. **Humanizer additions:**
   - "What NOT to flag" section with the full false-positive list
   - "Signs of human writing (preserve these)" section
   - Cluster-detection principle: isolated tells are not reliable, look for co-occurrence
   - Position these sections after the pattern categories, before the Process section

2. **Pre-validator changes:**
   - Reduce severity of isolated tells: a single em dash alone is LOW, not HIGH
   - Add cluster-detection: escalate severity when 3+ different AI tells appear in the same paragraph
   - Add "human signal bonus": content with specific details, mixed feelings, or self-corrections should get positive score adjustments
   - Update scoring algorithm to account for false-positive awareness

3. **Content-generator changes:**
   - Self-validation should not reject output for isolated tells
   - "Preserve these human signals" guidance in the self-validation step
   - Don't flatten personality markers that the content-generator itself added

4. **Shared principles across all skills:**
   - Individual AI tells in isolation are weak signals
   - Clusters of 3+ co-occurring tells are strong signals
   - Specific, hard-to-fabricate details are human markers: preserve them
   - Context matters: em dashes in a journalism piece are different from em dashes in a corporate blog

## Open Questions

- Should the pre-validator's scoring algorithm literally subtract points for human signals (positive adjustment), or just not penalize isolated tells?
- How do we handle the tension between CLAUDE.md's hard "no em dashes" rule and the false-positive guidance that says "em dashes alone are not a tell"? The CLAUDE.md rule is a project-level style preference, not an AI detection rule. They serve different purposes and both can coexist.
- Should we contribute the cluster-detection principle back to upstream?
