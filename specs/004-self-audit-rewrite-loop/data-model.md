# Data Model: Self-Audit Rewrite Loop

**Feature**: 004-self-audit-rewrite-loop | **Date**: 2026-06-12

## Overview

This feature operates entirely within SKILL.md files (prose instructions for an LLM). There are no code data structures, database schemas, or API contracts. The entities below are conceptual models that guide the language and structure of the skill instructions.

## Entities

### Self-Audit Finding

A brief bullet describing a higher-order AI tell identified during the self-audit step.

| Field | Type | Description |
|-------|------|-------------|
| tell_description | string | What the AI tell is (e.g., "rhythm too uniform across paragraphs") |
| affected_area | string | Which part of the text exhibits the tell |

**Notes**: Findings are expressed as brief bullet points in the skill output. They are not structured data.

### Draft Rewrite

Internal working state produced by the humanizer's pattern-based rewrite.

| Field | Type | Description |
|-------|------|-------------|
| content | string | The rewritten text after pattern rules applied |
| pattern_violations_fixed | list | Which patterns were addressed |

**Notes**: Not shown to the user (FR-003). Serves as input to the self-audit step.

### Final Rewrite

The output produced after addressing self-audit findings.

| Field | Type | Description |
|-------|------|-------------|
| content | string | The final text delivered to the user |
| audit_findings | list[Self-Audit Finding] | What the self-audit caught (may be empty) |
| rewrite_performed | boolean | Whether a rewrite pass was triggered |
| correction_performed | boolean | Whether FR-010 correction pass ran |

**Notes**: This is what the user sees. Findings appear after the content in a labeled section.

## State Transitions

### Humanizer Processing Flow

```
Input Text
  → [Pattern Rewrite] → Draft Rewrite
  → [Self-Audit Question] → Audit Findings (0..N)
  → {findings?}
     ├─ Yes → [Final Rewrite] → Rewritten Text
     │         → [Re-validate patterns]
     │         → {new violations?}
     │            ├─ Yes → [Single Correction Pass] → Corrected Text → Deliver
     │            └─ No → Deliver
     └─ No → Deliver (skip rewrite, report "no additional tells")
```

### Content-Generator Processing Flow

```
Content Request
  → [Generate] → Raw Content
  → [Self-Validate (rules)] → Validated Content
  → [Self-Audit Question] → Audit Findings (0..N)
  → {findings?}
     ├─ Yes → [Rewrite Pass] → Final Content → Deliver
     └─ No → Deliver (report "no additional tells")
```

## Relationships

- **Self-Audit Finding → Draft Rewrite**: Findings reference specific parts of the draft
- **Final Rewrite → Self-Audit Finding**: Final rewrite addresses findings
- **Voice Profile → Self-Audit**: Voice-consistent traits must not be flagged as AI tells
- **Pattern Rules → Final Rewrite**: FR-010 re-validation ensures pattern compliance after self-audit rewrite
