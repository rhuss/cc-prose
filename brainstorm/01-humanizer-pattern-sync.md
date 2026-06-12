# Brainstorm: Humanizer pattern sync with upstream v2.8.0

**Date:** 2026-06-12
**Status:** active
**Upstream:** https://github.com/blader/humanizer

## Problem Framing

The cc-prose humanizer skill (v2.1.1) is 8 pattern categories behind the upstream humanizer (v2.8.0, blader/humanizer). The upstream has added categories that catch real AI tells we're currently missing. Additionally, the upstream scoped its "Personality and Soul" section to only apply to opinion/blog content, which is a better default than our current unconditional application.

The upstream version is also the canonical community-maintained version based on Wikipedia's "Signs of AI writing" guide, so staying in sync keeps us aligned with the evolving detection landscape.

## Context

### Current state (our v2.1.1)
- 24 pattern categories
- Personality/soul section applies unconditionally to all content
- Numbering: categories 1-24
- "Actually" not in AI vocabulary watchlist
- Em dash rule says "overuse" (soft)
- Negative parallelisms: no tailing negation coverage
- Knowledge-cutoff: no speculative gap-filling coverage
- Our recent local additions: "Here's the twist/kicker/..." in filler phrases, density detection in rule-of-three

### Upstream state (v2.8.0)
- 33 pattern categories (8 new)
- Personality/soul scoped to blog/essay/opinion only
- "Actually" added to AI vocabulary
- Em dash rule is hard "cut them all" including en dashes
- Negative parallelisms expanded with tailing negations
- Knowledge-cutoff expanded with speculative gap-filling

### Files affected
- `prose/skills/humanizer/SKILL.md` (plugin copy)
- `~/.claude/skills/humanizer/SKILL.md` (canonical source)
- `prose/skills/pre-validator/SKILL.md` (needs updated category count references)
- `prose/skills/content-generator/SKILL.md` (references "24 categories")

## Approaches Considered

### A: Full wholesale adoption of upstream SKILL.md (Recommended)
- Replace our SKILL.md with upstream's, then merge back our local additions (rule-of-three density, "Here's the..." filler entries)
- Pros: Gets all improvements at once, stays in sync, minimal ongoing divergence
- Cons: Need to carefully merge our local additions back in; numbering shift (our 13-24 become 14-25+) may affect pre-validator references

### B: Cherry-pick new categories only
- Add the 8 new categories to our existing file, keep our structure
- Pros: Minimal disruption, no renumbering
- Cons: Miss the expanded existing categories (tailing negations, gap-filling, hard em-dash rule), growing divergence from upstream makes future syncs harder

### C: Fork permanently
- Take what we want now, stop tracking upstream
- Pros: Full control
- Cons: Lose community improvements, Wikipedia-sourced pattern updates

## Decision

Approach A: Full wholesale adoption with local additions merged back. The upstream is well-maintained and tracks Wikipedia's evolving detection patterns. Staying in sync is more valuable than avoiding a one-time merge effort.

## Key Requirements

1. Adopt all 8 new pattern categories from upstream v2.8.0:
   - #13: Passive Voice and Subjectless Fragments
   - #26: Hyphenated Word Pair Overuse
   - #27: Persuasive Authority Tropes
   - #28: Signposting and Announcements
   - #29: Fragmented Headers
   - #30: Diff-Anchored Writing
   - #31: Manufactured Punchlines and Staccato Drama
   - #32: Aphorism Formulas
   - #33: Conversational Rhetorical Openers (subsumes our "Here's the..." additions)

2. Adopt expanded existing categories:
   - #9: Add tailing negations ("no guessing" fragments)
   - #14: Hard "cut them all" em/en dash rule (replaces soft "overuse")
   - #21: Add speculative gap-filling
   - #7: Add "Actually" to AI vocabulary

3. Scope personality/soul section:
   - Apply only to blog posts, essays, opinion pieces, personal writing
   - For technical, legal, encyclopedic, or reference text: neutral voice IS the correct human voice
   - Don't inject opinions or first person in technical docs

4. Merge back our local additions that upstream doesn't have:
   - Rule-of-three density detection (count triples across whole text, not just individual instances)
   - Any filler phrase entries not already covered by upstream's #33

5. Update references in other skills:
   - pre-validator: update category count from 24 to 33
   - content-generator: update "24 categories" reference

6. Update version number (align with or exceed upstream)

## Open Questions

- Do we want to contribute our rule-of-three density detection back to upstream?
- The upstream's full example now has a 3-pass process (draft, self-audit, final). That's covered by brainstorm #04. Should we adopt it here or wait for that brainstorm?

---

## Revisit: 2026-06-12

### Updated Problem Framing

The original brainstorm covered both WHAT patterns to sync (content) and HOW to sync them (mechanism). The sync mechanism has been split into its own brainstorm (#05 humanizer-upstream-sync) to keep concerns separate. This brainstorm now focuses purely on the content update: adopting upstream v2.8.0 patterns.

### Changes

- **Sync mechanism extracted**: The open question about `make sync-humanizer` pulling from upstream is now addressed in brainstorm #05, which designs a proper delta-aware sync system modeled on cc-spex's superpowers integration.
- **Dependency created**: This content sync (#01) should be executed using the sync mechanism from #05. The first sync will serve as the initial baseline for the new tracking system.

### Updated Decision

Approach A (full wholesale adoption) remains correct. The execution path changes: instead of a manual copy-and-merge, the first sync will be performed via the `/update-humanizer` command designed in brainstorm #05, which will handle the merge intelligently and establish the tracking baseline.

### Open Threads

- Content sync (#01) depends on sync mechanism (#05) being implemented first
- First sync doubles as the initial baseline for the new tracking system
