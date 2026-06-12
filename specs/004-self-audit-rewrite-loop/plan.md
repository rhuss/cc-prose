# Implementation Plan: Self-Audit Rewrite Loop

**Branch**: `004-self-audit-rewrite-loop` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-self-audit-rewrite-loop/spec.md`

## Summary

Add an adversarial self-audit step to both the humanizer and content-generator skills. The humanizer already has a basic self-audit in its "Process and Output" section (steps 3-4); this feature formalizes it with false-positive awareness, a single-correction-pass bound, and output format changes. The content-generator gains an entirely new self-audit step inserted between its existing self-validation (Step 6) and content presentation (Step 7).

## Technical Context

**Language/Version**: Markdown (SKILL.md files for Claude Code plugin)
**Primary Dependencies**: Claude Code plugin framework, humanizer skill v2.8.0, content-generator skill v1.1.0
**Storage**: File-based (SKILL.md markdown files)
**Testing**: Manual testing via Claude Code (invoke skills and verify output)
**Target Platform**: Claude Code CLI / IDE extensions
**Project Type**: Claude Code plugin (skill-based, no compiled code)
**Performance Goals**: N/A (LLM generation time, not measurable in code)
**Constraints**: SKILL.md format, voice profile compatibility, humanizer upstream sync considerations
**Scale/Scope**: 2 skills modified (humanizer SKILL.md, content-generator SKILL.md)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution is unconfigured (template placeholders only). No gates to enforce. Proceeding.

## Project Structure

### Documentation (this feature)

```text
specs/004-self-audit-rewrite-loop/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
└── tasks.md             # Phase 2 output (from /speckit.tasks)
```

### Source Code (repository root)

```text
prose/
├── skills/
│   ├── humanizer/
│   │   └── SKILL.md         # Modified: self-audit formalization
│   ├── content-generator/
│   │   └── SKILL.md         # Modified: new self-audit step
│   ├── pre-validator/
│   │   └── SKILL.md         # Unchanged (per spec assumption)
│   ├── voice-architect/
│   │   └── SKILL.md         # Unchanged
│   └── voice-extractor/
│       └── SKILL.md         # Unchanged
├── commands/
│   └── *.md                 # Unchanged (thin wrappers)
└── knowledge-base/
    └── voice-templates/     # Unchanged
```

**Structure Decision**: No new files needed. Both changes are modifications to existing SKILL.md files. No contracts directory needed (no external interfaces exposed by this feature).

## Complexity Tracking

No constitution violations to justify.

## Phase 0: Research

### Research Summary

No NEEDS CLARIFICATION items exist. All unknowns were resolved during the clarification phase. The following decisions were confirmed:

**Decision 1: Correction loop bound**
- Decision: Single correction pass (one re-validation + correction, then deliver as-is)
- Rationale: Prevents infinite loops; in practice one round catches introduced violations
- Alternatives considered: Up to 3 passes (rejected: unnecessary complexity), unbounded loop (rejected: risk of non-convergence)

**Decision 2: Content-generator flow**
- Decision: Mirror humanizer flow (generate → self-validate → self-audit → rewrite → deliver)
- Rationale: Consistent architecture across both skills; self-audit logic pattern is reusable
- Alternatives considered: Inline fixes during generation (rejected: loses separation of concerns), audit-only without rewrite (rejected: findings without action are low value)

**Decision 3: Self-audit prompt style**
- Decision: Single open-ended adversarial question ("What makes this still obviously AI-generated?")
- Rationale: Open-ended form surfaces unexpected tells that a fixed checklist would miss
- Alternatives considered: Structured checklist (rejected: becomes another pattern-rule system), open-ended with hints (rejected: hints constrain the adversarial nature)

**Decision 4: Output placement**
- Decision: Self-audit findings appear after content in a clearly labeled section
- Rationale: Primary deliverable (the text) stays front and center
- Alternatives considered: Before content (rejected: buries the main output), inline annotations (rejected: clutters content)

**Decision 5: False-positive access**
- Decision: Embed false-positive guidance inline in the self-audit prompt instructions
- Rationale: Keeps self-audit self-contained; avoids runtime file lookups
- Alternatives considered: External file reference (rejected: adds runtime dependency), rely on existing pattern rules (rejected: insufficient for the adversarial question)

### Existing Codebase Analysis

**Humanizer current state** (SKILL.md lines 594-601):
The humanizer already has a rudimentary self-audit in "Process and Output":
1. Identify patterns, write draft rewrite
2. Ask "What makes the below so obviously AI generated?" and list remaining tells
3. Revise into final rewrite addressing tells
4. Deliver draft, bullets, final rewrite, and change summary

What needs to change:
- Add false-positive guidance inline in the self-audit step
- Add FR-006 instruction: focus on higher-order signals, not pattern rules
- Add FR-010: single correction pass after re-validation
- Change output format: deliver ONLY final rewrite + findings after content (not draft)
- Add FR-009: skip final rewrite when no tells found
- Restructure delivery to match FR-003

**Content-generator current state** (SKILL.md Steps 1-7):
The content-generator has no self-audit. Its flow is:
1. Understand request → 2. Apply voice → 3. Generate content → 4. Avoid patterns → 5. Inject personality / 5b. Preserve human signals → 6. Self-validation → 7. Present content

What needs to be added:
- New Step 6b: Self-audit (after self-validation, before presentation)
- Self-audit asks the open-ended adversarial question
- If findings exist, perform a rewrite pass
- Include findings after content in output (Step 7 modification)
- Add FR-009: skip rewrite when no tells found

**False-positive guidance to embed** (sourced from humanizer "What NOT to flag" section and content-generator "Preserve Human Writing Signals"):
- Perfect grammar / consistent style (not an AI tell)
- Mixed casual/formal registers
- Formal/academic vocabulary matching voice profile
- Single em dash in isolation (tell only when clustered)
- Common transition words in isolation
- Short emphatic sentences (human voice technique)
- Genuine asides and self-corrections
- Mixed feelings / unresolved tension
- First-person editorial choices
- Specific concrete details
- Era-bound references

## Phase 1: Design

### Data Model

**Self-Audit Finding** (conceptual, not code):
- `tell_description`: string - Brief description of the higher-order AI tell
- `affected_area`: string - Which part of the text is affected
- `severity`: enum (high, medium, low) - Impact on perceived AI-ness

**Audit Result** (conceptual):
- `findings`: list[Self-Audit Finding] - Ordered list of tells found
- `has_findings`: boolean - Whether any tells were identified
- `rewrite_performed`: boolean - Whether a rewrite pass was triggered

Note: These are conceptual entities for the SKILL.md prose instructions, not data structures in code. They guide the language used in the skill templates.

### Design: Humanizer Changes

The humanizer's "Process and Output" section (lines 594-601) will be restructured:

**Current flow**: Read → Draft rewrite → Self-audit question → Final rewrite → Deliver (draft + bullets + final + summary)

**New flow**: Read → Draft rewrite → Self-audit (with false-positive guidance + higher-order focus) → Conditional final rewrite → Re-validate → Conditional correction pass → Deliver (final only + findings after content + summary)

Key structural changes:
1. **Self-audit step expanded**: Add inline false-positive guidance, FR-006 higher-order signal focus, and explicit instruction not to re-check pattern rules
2. **Conditional rewrite**: FR-009 - skip rewrite when no tells found
3. **Re-validation + correction bound**: FR-010 - one correction pass maximum
4. **Output restructured**: FR-003 - final rewrite only (no draft), findings after content

The line at the top of the SKILL.md (line 35) referencing "Process and Output" will need updating if section naming changes.

### Design: Content-Generator Changes

The content-generator gains a new step between existing Steps 6 and 7:

**New Step 6b: Adversarial Self-Audit**
- Placed after self-validation (Step 6) and before presentation (Step 7)
- Uses the same open-ended question as the humanizer
- Includes inline false-positive guidance
- References Step 5b's protected categories (human writing signals)
- If findings exist: perform a distinct rewrite pass addressing them
- If no findings: skip rewrite, note "no additional AI tells found"
- Include findings in output (modify Step 7 format)

The content-generator's Step 7 output format changes:
- Add a "Self-audit findings" section after the generated content
- When no findings: include "No additional AI tells found" line

### Design: Shared Self-Audit Prompt Pattern

Both skills use the same core pattern (kept consistent but not extracted into a shared file, since SKILL.md files are self-contained):

```
Self-audit question: "What makes this still obviously AI-generated?"

Focus on higher-order signals:
- Rhythm and cadence (too uniform, too tidy)
- Structure (overly balanced paragraphs, predictable flow)
- Tone (evenly neutral, lacks genuine voice variation)
- Specificity (generic where concrete detail would be natural)
- Emotional range (flatlined, no mixed feelings)

Do NOT re-check individual pattern rules (those are already enforced).

Do NOT flag as AI tells:
- Deliberate stylistic choices matching the voice profile
- Intentional repetition for emphasis
- Rhetorical list structures the author chose
- Genuine asides, self-corrections, or parenthetical interruptions
- Mixed feelings or unresolved tension (these are human signals)
- Short emphatic sentences used for effect
- Specific concrete details
- Common transition words in isolation
- Formal vocabulary that matches the content's register
```

### Integration Points

1. **Humanizer ↔ upstream sync**: The humanizer tracks upstream `blader/humanizer`. Changes to "Process and Output" are local additions. The `.humanizer-sync` file tracks which sections are local. This feature modifies a section that is already partially local (the current process steps). The sync mechanism should handle this, but the `update-humanizer` command should be tested after implementation.

2. **Content-generator ↔ voice profiles**: The self-audit must respect voice-consistent traits. The false-positive guidance inline addresses this. No changes to voice profiles or templates needed.

3. **Pre-validator**: Per spec assumption, the pre-validator does not need changes. The self-audit is a rewriting concern, not a validation concern.

### Constitution Re-Check

Constitution unconfigured. No re-check needed.

---

**Artifacts generated**: plan.md, research.md (inline above), data-model.md
**Next command**: `/speckit-tasks`
