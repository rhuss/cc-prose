# Deep Review Findings

**Date:** 2026-06-12
**Branch:** 004-self-audit-rewrite-loop
**Rounds:** 1
**Gate Outcome:** PASS
**Invocation:** quality-gate

## Summary

| Severity | Found | Fixed | Remaining |
|----------|-------|-------|-----------|
| Critical | 0 | 0 | 0 |
| Important | 2 | 2 | 0 |
| Minor | 5 | 1 | 4 |
| **Total** | **7** | **3** | **4** |

**Agents completed:** 5/5 (+ 1 external tool)
**Agents failed:** None

## Findings

### FINDING-1
- **Severity:** Important
- **Confidence:** 92
- **File:** prose/skills/content-generator/SKILL.md:544-546
- **Category:** correctness
- **Source:** correctness-agent (also reported by: architecture-agent)
- **Round found:** 1
- **Resolution:** fixed (round 1)

**What is wrong:**
Content-generator Step 6b had no re-validation step after the self-audit conditional rewrite. If the rewrite addressing self-audit tells introduced new pattern violations (e.g., an em-dash, a stoplist word), nothing caught them. The humanizer has an explicit Step 5 ("Re-validate and correct") with a single-correction-pass bound, but the content-generator lacked this entirely.

**Why this matters:**
Without re-validation, the content-generator could deliver content with pattern violations introduced by the self-audit rewrite, undermining the "publication-ready" claim. The spec's edge case section states generically that final rewrites must comply with all pattern rules.

**How it was resolved:**
Added re-validation instructions to Step 6b's conditional rewrite section: "After the rewrite, re-run Step 6 self-validation checks (pattern rules, stoplist, style). If the rewrite introduced new violations, perform exactly one correction pass, then proceed to Step 7."

### FINDING-2
- **Severity:** Important
- **Confidence:** 90
- **File:** prose/skills/humanizer/SKILL.md:658
- **Category:** architecture
- **Source:** architecture-agent
- **Round found:** 1
- **Resolution:** fixed (round 1)

**What is wrong:**
The example annotation "*(Steps 1-2 are internal. The draft rewrite is not shown to the user.)*" was misleading. Step 1 is "Read the input" which is not internal in the same sense as Step 2 (draft rewrite). The annotation also didn't mention that Steps 5-6 (re-validation and delivery formatting) are also omitted from the example.

**Why this matters:**
An LLM following this example could misinterpret what "internal" means or think only Steps 1-2 are omitted when Steps 5-6 are also not shown.

**How it was resolved:**
Changed to: "*(Step 1 reads the input; Step 2 produces a draft rewrite. Neither is shown to the user. Steps 5-6, re-validation and delivery formatting, are mechanical and omitted from this example.)*"

### FINDING-3
- **Severity:** Minor
- **Confidence:** 75
- **File:** prose/skills/content-generator/SKILL.md:550
- **Category:** correctness
- **Source:** correctness-agent (also reported by: architecture-agent)
- **Round found:** 1
- **Resolution:** fixed (round 1)

**What is wrong:**
Step 7's guard condition read "Only after self-validation passes, present to user:" but Step 6b (Adversarial Self-Audit) now runs between self-validation (Step 6) and presentation (Step 7). The guard condition was stale.

**Why this matters:**
A strict reading could suggest that only Step 6 needs to pass before presenting, ignoring Step 6b.

**How it was resolved:**
Changed to "Only after self-validation (Step 6) and self-audit (Step 6b) are complete, present to user:"

### FINDING-4
- **Severity:** Minor
- **Confidence:** 65
- **File:** prose/skills/content-generator/SKILL.md:544-546
- **Category:** correctness
- **Source:** correctness-agent
- **Round found:** 1
- **Resolution:** fixed (round 1)

**What is wrong:**
Content-generator used "Note" for the no-findings case while humanizer uses "Report." Minor wording inconsistency.

**Why this matters:**
Inconsistency between skills that are intended to mirror each other.

**How it was resolved:**
Changed to "Report" to match the humanizer's wording.

### FINDING-5
- **Severity:** Minor
- **Confidence:** 85
- **File:** prose/skills/content-generator/SKILL.md:65-74
- **Category:** architecture
- **Source:** architecture-agent
- **Round found:** 1
- **Resolution:** remaining (pre-existing, not introduced by this change)

**What is wrong:**
The "Your Mission" summary lists 6 steps that map to 9 actual workflow steps (counting 5b and 6b). The new Step 5 ("Self-audit") was added to the Mission but the abstraction gap grew slightly.

**Why this matters:**
Minor navigation issue. The abstraction is defensible since the Mission is an executive summary.

### FINDING-6
- **Severity:** Minor
- **Confidence:** 70
- **File:** prose/.humanizer-sync:16-19
- **Category:** architecture
- **Source:** architecture-agent
- **Round found:** 1
- **Resolution:** remaining

**What is wrong:**
The .humanizer-sync description captures semantic changes but not the structural change from flat 4-step paragraph to 6 numbered steps with sub-sections.

**Why this matters:**
During upstream merge, the merge operator should know the step structure itself changed.

### FINDING-7
- **Severity:** Minor
- **Confidence:** 60
- **File:** prose/skills/content-generator/SKILL.md:9-10
- **Category:** correctness
- **Source:** correctness-agent
- **Round found:** 1
- **Resolution:** remaining (pre-existing)

**What is wrong:**
The capabilities list says "Humanizer pattern prevention (33 categories)" but the count may be outdated if categories have been added or removed.

**Why this matters:**
Minor factual accuracy in metadata. Pre-existing issue not introduced by this change.

## Test Suite Results

No test command detected; post-fix test step was skipped.

## Remaining Findings

4 Minor findings remain, all either pre-existing issues not introduced by this change or low-impact documentation improvements. None block the gate.
