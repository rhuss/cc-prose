# Implementation Plan: Inline Voice-Matching

**Branch**: `003-inline-voice-matching` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/003-inline-voice-matching/spec.md`

## Summary

Add inline voice-matching capability to the content-generator skill (the humanizer already has it from upstream v2.8.0) and document voice source priority order across both skills. This enables users to provide a writing sample alongside any rewrite or generation request for ad-hoc voice matching without creating persistent profiles.

## Technical Context

**Language/Version**: Markdown (SKILL.md files are LLM instruction documents, not code)
**Primary Dependencies**: cc-prose plugin skills (humanizer, content-generator)
**Storage**: N/A (ephemeral, no persistence)
**Testing**: Manual validation via skill invocation
**Target Platform**: Claude Code plugin system
**Project Type**: Plugin (LLM skill definitions)
**Performance Goals**: N/A
**Constraints**: Must not break existing voice profile workflow; must preserve upstream humanizer structure
**Scale/Scope**: 2 SKILL.md files modified

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution is an unfilled template. No gates to check. Proceeding.

## Project Structure

### Documentation (this feature)

```text
specs/003-inline-voice-matching/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
prose/skills/
├── humanizer/
│   └── SKILL.md         # Modified: add priority order + cross-reference
├── content-generator/
│   └── SKILL.md         # Modified: add Voice Calibration section + priority logic
├── pre-validator/
│   └── SKILL.md         # Not modified
├── voice-architect/
│   └── SKILL.md         # Not modified
└── voice-extractor/
    └── SKILL.md         # Not modified
```

**Structure Decision**: No new files or directories. This feature modifies two existing SKILL.md files in-place.

## Implementation Approach

### Change 1: Humanizer SKILL.md (minimal changes)

The humanizer already has a complete "Voice Calibration (Optional)" section from the upstream v2.8.0 sync (lines 38-56). Changes needed:

1. **Add priority order documentation** after the "How to provide a sample" subsection. Insert a "Voice source priority" subsection explaining: inline sample > configured voice profile > default behavior.

2. **Add cross-reference to voice-extractor** at the end of the Voice Calibration section. A single line: "For reusable voice profiles across sessions, use the voice-extractor (`/prose:voice extract`)."

3. **Add file validation guidance** in the "How to provide a sample" subsection. When a referenced file doesn't exist or is binary, warn and fall back.

### Change 2: Content-Generator SKILL.md (new section + modified phase)

The content-generator currently has no inline voice matching. It loads voice profiles from YAML files (Phase 2) and applies them (Step 2). Changes needed:

1. **Add "Voice Calibration (Optional)" section** after the "Your Mission" section (before "Configuration Loading"). This mirrors the humanizer's section, adapted for content generation:
   - Same six analysis dimensions (sentence length, word choice, paragraph openings, punctuation, recurring phrases, transitions)
   - Same two input methods (inline text, file reference)
   - Same file validation (warn + fall back for missing/binary files)
   - Cross-reference to voice-extractor for persistent profiles

2. **Modify "Step 2: Apply Voice Profile"** to incorporate the priority order:
   - Check for inline sample first (from the user's request)
   - If present, use inline sample voice (skip YAML profile)
   - If not present, use configured voice profile (existing behavior)
   - If neither, use voice auto-detection (existing behavior)
   - Add a note that project-level style rules override sample voice for prohibited patterns

3. **Add priority order documentation** explicitly stating: inline sample > voice profile > auto-detection > default.

### Integration Points

- The humanizer's existing Voice Calibration section structure is preserved. New content is appended, not restructured.
- The content-generator's existing Phase 2 (Load Voice Profile) and Step 2 (Apply Voice Profile) remain intact. Inline voice matching is layered on top as a higher-priority option.
- Both skills' self-validation steps are unaffected. Inline voice matching applies to generation/rewriting, not validation.

## Complexity Tracking

No constitution violations to justify. This is a straightforward SKILL.md edit with no architectural complexity.
