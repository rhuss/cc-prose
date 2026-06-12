# Implementation Plan: False-Positive Guidance and Human Signal Preservation

**Branch**: `002-false-positive-guidance` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/002-false-positive-guidance/spec.md`

## Summary

Add false-positive awareness, cluster detection, and human writing signal recognition to the pre-validator and content-generator skills. The humanizer already has this guidance from the upstream v2.8.0 sync. Changes are confined to two SKILL.md files: adding new sections for detection guidance, modifying severity classification rules, updating the report format, and adjusting self-validation logic.

## Technical Context

**Language/Version**: Markdown (SKILL.md files are prose instructions for Claude, not executable code)
**Primary Dependencies**: Upstream humanizer v2.8.0 (already synced, provides canonical false-positive and human signal lists)
**Storage**: N/A
**Testing**: Manual validation by running `/prose:check` and `/prose:write` on test content
**Target Platform**: Claude Code plugin (cc-prose)
**Project Type**: Plugin (skill file authoring)
**Performance Goals**: N/A (no runtime performance, these are LLM instruction files)
**Constraints**: Skill files must be self-contained (no cross-file references during execution); stoplist rules always override false-positive guidance
**Scale/Scope**: 2 files modified: `prose/skills/pre-validator/SKILL.md` and `prose/skills/content-generator/SKILL.md`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution contains only template placeholders (no project-specific principles defined). No violations possible. GATE PASSES.

## Project Structure

### Documentation (this feature)

```text
specs/002-false-positive-guidance/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
prose/
└── skills/
    ├── pre-validator/
    │   └── SKILL.md         # PRIMARY TARGET: scoring changes, cluster detection, human signals
    ├── content-generator/
    │   └── SKILL.md         # SECONDARY TARGET: self-validation false-positive awareness
    └── humanizer/
        └── SKILL.md         # REFERENCE ONLY: contains canonical detection guidance (already synced)
```

**Structure Decision**: No new files or directories. All changes are edits to two existing SKILL.md files.

## Implementation Approach

### Pre-validator Changes (prose/skills/pre-validator/SKILL.md)

**1. Add Detection Guidance Section**

Insert a new "Detection Guidance" section after Phase 1 (AI Pattern Scan) and before Phase 2 (Stoplist Word Check). This section contains:
- The false-positive list (12 items from the spec)
- The human writing signals list (6 items from the spec)
- The cluster detection principle

**2. Modify Severity Classification in Phase 1**

Update the AI Pattern Scan phase to apply isolation-aware severity:
- When a tell appears with no other tells in the same paragraph, downgrade to LOW severity
- When 3+ different tell types co-occur in the same paragraph, restore each to its original default severity
- Stoplist words remain CRITICAL regardless (FR-005)

The existing severity tiers (CRITICAL/HIGH/MEDIUM/LOW) and their point deductions remain unchanged. The change is to the classification logic that assigns tells to tiers.

**3. Add Human Writing Signals to Report Format**

Insert a "Human Writing Signals" subsection in the report template, between the severity issue lists (after LOW Priority Issues) and the Readability Metrics section. Format:

```markdown
## Human Writing Signals Detected

| Signal Type | Example Found | Location |
|-------------|---------------|----------|
| Specific detail | "123 Main Street, Peoria" | Line 45 |
| Self-correction | "I keep wanting to say..." | Line 78 |
```

**4. Update Category Count**

Replace all instances of "24" (in the context of humanizer categories) with "33".

### Content-generator Changes (prose/skills/content-generator/SKILL.md)

**1. Add False-Positive Awareness to Self-Validation (Step 6)**

Update the Humanizer Pattern Validation subsection in Step 6 to:
- Not reject output for a single isolated tell (no other tells in the entire output)
- Only flag tells when 2+ different tell types co-occur in the output

**2. Add Human Signal Preservation Guidance**

Add a subsection after Step 5 (Inject Personality) or within Step 6 (Self-Validation):
- List human writing signals that should be preserved
- Instruct self-validation to recognize and keep these patterns
- Prevent the generator from stripping its own personality markers

**3. Update Category Count**

Replace all instances of "24" (in the context of humanizer categories) with "33".

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Isolated tell downgrade lets AI content pass | Medium | Cluster detection compensates: 3+ co-occurring tells restore default severity |
| Human signal detection is subjective | Low | List is concrete and enumerated; detection is informational, not score-affecting |
| Skill file size increase | Low | Additions are ~40-60 lines per file; well within acceptable skill size |
| Stoplist/false-positive conflict | Low | Stoplist supremacy is explicitly maintained (FR-005) |
