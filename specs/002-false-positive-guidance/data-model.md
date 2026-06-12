# Data Model: False-Positive Guidance and Human Signal Preservation

**Date**: 2026-06-12

## Entities

### AI Tell

A textual pattern that may indicate AI-generated content.

| Attribute | Description |
|-----------|-------------|
| Pattern | The specific text or structural pattern (e.g., "delve", em dash, rule-of-three) |
| Category | The humanizer category it belongs to (e.g., "AI Vocabulary", "Style Issues") |
| Default Severity | The severity level before isolation adjustment (CRITICAL, HIGH, MEDIUM, LOW) |
| Effective Severity | The severity after isolation/cluster adjustment |
| Location | Line number and paragraph context where the tell appears |

### Cluster

Three or more different AI tell types co-occurring within the same paragraph.

| Attribute | Description |
|-----------|-------------|
| Paragraph | The paragraph containing the co-occurring tells |
| Tell Types | List of distinct tell categories present (minimum 3) |
| Tell Count | Number of different tell types in the cluster |
| Effect | Restores each tell to its default severity (removes isolation downgrade) |

### False Positive

A textual pattern that resembles an AI tell but is common in human writing.

| Attribute | Description |
|-----------|-------------|
| Pattern | The pattern description (e.g., "em dashes alone", "formal vocabulary") |
| Scope | When this applies: "in isolation" (no co-occurring tells in the same paragraph) |
| Override | Stoplist entries are never treated as false positives |

### Human Writing Signal

A textual pattern that positively indicates human authorship.

| Attribute | Description |
|-----------|-------------|
| Signal Type | Category of signal (specific detail, mixed feelings, self-correction, etc.) |
| Example | The actual text found in the content |
| Location | Line number where the signal appears |
| Effect | Reported in output; does not modify numeric score |

## Relationships

```
AI Tell ─── belongs to ──→ Category (1:1)
AI Tell ─── may be in ──→ Cluster (N:1, only when 3+ different types co-occur)
AI Tell ─── may match ──→ False Positive list (checked only when isolated)
Cluster ─── contains ──→ AI Tell (1:N, minimum 3 different types)
Human Writing Signal ─── independent of ──→ AI Tell (no direct relationship)
Stoplist Word ─── overrides ──→ False Positive (stoplist always wins)
```

## State Transitions

### AI Tell Severity Resolution

```
Tell detected
  ├─ Is it a stoplist word? → CRITICAL (always, no override)
  ├─ Is it in a cluster (3+ different types in paragraph)?
  │   └─ Yes → Use default severity (original tier)
  └─ No cluster (isolated)
      └─ Downgrade to LOW severity
```

## Notes

- No persistent data storage. All entities exist transiently during a single validation or generation run.
- The false-positive list and human signals list are static content embedded in the SKILL.md files, not configurable data.
- Cluster detection scope differs: paragraph-level for pre-validator, whole-output for content-generator.
