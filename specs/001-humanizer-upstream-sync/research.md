# Research: Humanizer Upstream Sync

## R1: cc-spex Sync Pattern Analysis

**Decision**: Adapt the cc-spex superpowers sync pattern for single-file humanizer tracking.

**Rationale**: The cc-spex pattern is proven in production, handles delta detection via git commit SHAs, preserves local additions through metadata-driven merge instructions, and generates audit reports. The humanizer case is simpler (single file vs. multiple skills), making it a straightforward adaptation.

**Key components from cc-spex**:
- `.superpowers-sync` JSON tracking file with `upstream_repo`, `last_sync_commit`, `last_sync_date`, `modified_skills`
- `scripts/check-upstream-changes.sh` (104 lines) for non-destructive upstream checking
- `.claude/commands/update-superpowers.md` (373 lines) for AI-assisted merge
- `docs/sync-reports/sync-YYYY-MM-DD.md` for audit trail

**Simplifications for cc-prose**:
- Single file tracking (only SKILL.md) vs. cc-spex's 4 modified skills
- No `sync_mode` variants needed (cc-spex has `reference-only` and `merge` modes)
- No `feeds_into` indirection (cc-spex's writing-plans feeds into plan skill)
- Simpler modified_skills metadata (just section headings to preserve)

**Alternatives considered**:
- Git submodule: Rejected. Fragile UX, overkill for one file.
- Manual cp with version comments: Rejected. No merge intelligence, no audit trail.

## R2: Upstream Check Strategy

**Decision**: Use `gh api` as primary, `git clone --depth 1` as fallback.

**Rationale**: `gh api repos/blader/humanizer/commits/main` returns the latest commit SHA in milliseconds without cloning. For diff details, `gh api repos/blader/humanizer/compare/{base}...main` provides the full comparison. When `gh` is unavailable, a shallow clone achieves the same result at higher cost.

**Implementation notes**:
- `gh api` path: no temp directory, no cleanup, fastest
- `git clone --depth 1` path: temp directory required, must clean up on exit (trap)
- Both paths produce the same output: commit count, commit messages, SKILL.md diff summary

## R3: Local Addition Preservation Strategy

**Decision**: Use `modified_skills` metadata in `.humanizer-sync` to list section headings containing local additions.

**Rationale**: The merge command reads this metadata to know which sections are cc-prose-specific. During merge, the AI agent is instructed to preserve these sections verbatim while integrating upstream changes around them. If a local section overlaps with an upstream change, the conflict is flagged in the sync report.

**Current local additions to track**:
- Rule-of-three density detection (within category 10 "Rule of Three Overuse")
- Custom filler phrase entries (within category 22 "Filler Phrases", entries like "Here's the twist/kicker/...")

**Metadata format**:
```json
{
  "modified_skills": [
    {
      "upstream_file": "SKILL.md",
      "local_file": "prose/skills/humanizer/SKILL.md",
      "local_additions": [
        {
          "section": "10. Rule of Three Overuse",
          "description": "Density detection counting triples across whole text"
        },
        {
          "section": "22. Filler Phrases",
          "description": "Added 'Here's the twist/kicker/...' entries"
        }
      ]
    }
  ]
}
```

## R4: Sync Report Structure

**Decision**: Follow cc-spex pattern with sections for upstream range, changes, integration decisions, and preserved additions.

**Template**:
```markdown
# Sync Report: YYYY-MM-DD

**Upstream**: blader/humanizer
**Previous sync**: <commit-sha> (<date>)
**Current sync**: <commit-sha> (<date>)
**Commits synced**: N

## Upstream Changes

[Per-commit summary of what changed in SKILL.md]

## Changes Integrated

[What was merged into the local copy]

## Local Additions Preserved

[Confirmation that local sections remained intact]

## Conflicts

[Any conflicts between upstream changes and local additions, or "None"]

## Action Items

[Follow-up tasks if any, or "None"]
```
