# Review Guide: Self-Audit Rewrite Loop

**Generated**: 2026-06-12 | **Spec**: [spec.md](spec.md)

## Why This Change

The humanizer and content-generator skills check text against individual pattern rules (em dashes, AI vocabulary, promotional language, etc.), but text can pass every rule check and still read as obviously AI-generated. The missing piece is a higher-order adversarial check that asks "does this still sound like a machine wrote it?" after pattern rules are satisfied. The humanizer already has a rudimentary self-audit question in its process, but it lacks false-positive awareness, a convergence bound, and a consistent output format.

## What Changes

Both the humanizer and content-generator SKILL.md files gain a formalized self-audit step. The humanizer's existing self-audit (a simple "ask and revise" pair in its Process and Output section) is restructured into a bounded flow with false-positive guidance, conditional rewrite, re-validation, and a single correction pass limit. The content-generator, which currently has no self-audit, gains a new step (6b) inserted between its rule-based self-validation and content presentation. Both skills output self-audit findings after the content in a labeled section. No new files are created; no other skills are modified.

## How It Works

The implementation modifies two existing SKILL.md files:

**Humanizer** (`prose/skills/humanizer/SKILL.md`): The "Process and Output" section (currently steps 1-4 plus a delivery line) is restructured into a 7-step flow: read, draft rewrite, self-audit question with inline false-positive guidance, conditional final rewrite (skip if no tells found), re-validate against pattern rules, single correction pass (if violations introduced), deliver final only with findings after content. The full example section is updated to demonstrate the new output format.

**Content-generator** (`prose/skills/content-generator/SKILL.md`): A new Step 6b is inserted between self-validation (Step 6) and presentation (Step 7). It uses the same adversarial question and false-positive guidance as the humanizer. Step 7's output template is modified to include a findings section.

Both skills embed the false-positive guidance inline (no external file references) and use the same open-ended adversarial question: "What makes this still obviously AI-generated?"

## When It Applies

**Applies when**:
- The humanizer processes any text (the self-audit runs on every invocation)
- The content-generator creates any new content (the self-audit runs after self-validation)
- Text passes all individual pattern checks but still has higher-order AI tells (rhythm, cadence, structure, tone)

**Does not apply when**:
- Pre-validator runs (it already has its own multi-phase validation; the self-audit is a rewriting concern, not a validation concern)
- Voice profile management (voice-architect, voice-extractor are unchanged)
- Very short texts (under 100 words) may not benefit significantly from the self-audit
- The self-audit finds no tells (the rewrite step is skipped, and "no additional AI tells found" is reported)

## Key Decisions

1. **Single correction pass (FR-010)**: If the final rewrite introduces new pattern violations, exactly one correction pass runs, then the result is delivered as-is. Alternatives: up to 3 passes (unnecessary complexity), unbounded loop (risk of non-convergence). Chosen to prevent infinite loops while still catching introduced violations.

2. **Content-generator mirrors humanizer flow (FR-004)**: The content-generator uses the same generate, self-validate, self-audit, rewrite, deliver sequence. Alternative: inline fixes during generation (loses separation of concerns). Chosen for architectural consistency and testability.

3. **Single open-ended adversarial question (FR-006)**: The self-audit asks "What makes this still obviously AI-generated?" rather than running a structured checklist. Alternative: checklist of signal categories (becomes another pattern-rule system). Chosen because open-ended form surfaces unexpected tells.

4. **Findings after content (FR-003, FR-011)**: Self-audit findings appear after the content in a labeled section. Alternative: before content (buries the main output). Chosen to keep the primary deliverable front and center.

5. **False-positive guidance inline (FR-007)**: Guidance is embedded in the self-audit prompt instructions rather than referenced from an external file. Alternative: external file (adds runtime dependency). Chosen for self-containment.

## Areas Needing Attention

- **Upstream sync risk**: The humanizer tracks `blader/humanizer` upstream. The "Process and Output" section is being significantly restructured. The `.humanizer-sync` file should be updated to flag this section as a local modification that must be preserved during upstream merges.

- **Self-audit quality is prompt-dependent**: The self-audit's effectiveness depends entirely on how well the LLM responds to the adversarial question. There are no automated tests for SKILL.md behavior. Success criteria (SC-001 through SC-004) are measurable only through manual testing.

- **False-positive completeness**: The inline false-positive guidance distills categories from two existing sections (humanizer's "What NOT to flag" with 13 categories, content-generator's "Preserve Human Writing Signals" with 6 categories). If any category is missed, the self-audit could strip intentional human signals.

- **Draft visibility change**: The humanizer currently delivers the draft rewrite alongside the final. This feature changes that (FR-003: deliver final only). Users accustomed to seeing the draft will notice the difference.

## Open Questions

No open questions identified. All ambiguities were resolved during the clarification phase (5 questions asked and answered, recorded in spec.md under "## Clarifications").

## Review Checklist

- [ ] Key decisions are justified
- [ ] Breaking changes are documented with migration guidance
- [ ] Scope matches the stated boundaries
- [ ] Success criteria are achievable
- [ ] No unstated assumptions
- [ ] Self-audit question wording is identical in both skills
- [ ] False-positive guidance covers all categories from both existing sections
- [ ] Output format (findings after content) is consistent between both skills
- [ ] FR-010 single correction pass bound is clearly specified
- [ ] FR-009 skip-when-no-tells logic is present in both skills

---

<!-- Code phase sections are appended below this line by the phase-manager command -->
