# Deep Review Findings

**Date:** 2026-11-06
**Branch:** 006-multi-harness-support
**Rounds:** 2 (inline review and fixes)
**Gate Outcome:** PASS
**Invocation:** ship / review-code

## Review method

Correctness, architecture, security, production readiness, test quality, and goal alignment were reviewed inline against spec.md and the implementation. No independent subagents were dispatched: repository guidance permits Codex subagents only for explicitly requested parallel work. This is not an independent multi-agent review. Goal alignment used the agreed brainstorm and spec; no PR was created.

CodeRabbit was attempted with `coderabbit review --agent --uncommitted --dir prose` (this installed CLI does not support the skill's older --files flag). It failed authentication before producing findings: “Your CodeRabbit session or Git provider access could not be authenticated.” No login or credential changes were attempted. Configured external Codex reviewer delegation was omitted under the repository's subagent restriction; Copilot is disabled in config.

## Summary

| Severity | Found | Fixed | Remaining |
|---|---:|---:|---:|
| Critical | 0 | 0 | 0 |
| Important | 2 | 2 | 0 |
| Minor | 2 | 2 | 0 |

## Findings and resolutions

### FINDING-1 — Missing bundled templates were silently ignored

**Severity:** Important. **Category:** correctness/readiness. **Source:** inline review.

Global initialization succeeded even when a damaged install had no bundled voice templates. It could create global configuration without its expected template library. The initializer now checks template resources before creating global files, reports the missing path with a reinstall remedy, and returns failure. `test_missing_templates_reports_reinstall_without_writes` checks the result and absence of writes; the symlink test confirms valid real-path lookup.

### FINDING-2 — Dry-run did not cover first-time tracking state

**Severity:** Important. **Category:** correctness. **Source:** inline review.

The original command's initial-baseline branch wrote tracking state before reaching the later dry-run guard. The command now parses dry-run before state changes and makes baseline creation a read-only proposal in that mode. Maintenance checkout validation permits a missing tracking marker on first use. Existing merge rules, local additions, and upstream failure handling remain intact. This is an instruction-level workflow; no live upstream merge was executed.

### FINDING-3 — Marketplace version mismatch

**Severity:** Minor. **Category:** packaging. **Source:** Claude native validation.

The existing Claude marketplace advertised 1.0.0 while its authoritative plugin manifest was 1.1.0. The entry now matches the plugin and Codex/OpenCode metadata. Native marketplace validation passes without that warning.

### FINDING-4 — Portability instructions needed sync tracking

**Severity:** Minor. **Category:** maintenance. **Source:** inline review.

The new humanizer guide preamble needed an explicit preserved section. It now has a named Harness portability section listed in local_additions, including the frontmatter shell-tool requirement. A remaining bare Agent-tool dispatch instruction was also mapped to the guide's permitted-worker/inline action.

## Spec compliance after fixes

| Requirement | Implementation / evidence | Status |
|---|---|---|
| FR-001 Codex install/discovery | prose/.codex-plugin/plugin.json; .agents/plugins/marketplace.json; isolated native install and app-server skills/list | Compliant |
| FR-002 OpenCode install/discovery | package.json; index.js; .opencode/plugins/prose.js; OpenCode 2.1.4 native API lists all eleven shared files | Compliant |
| FR-003 shared source | Five original skill files; six wrappers reference existing commands; adapter reads source files rather than copying policy | Compliant |
| FR-004 six workflow equivalents | prose/skills/{write,rewrite,voice,check,init,update-humanizer}; README invocation matrix; native skill ids verified | Compliant |
| FR-005 writing rules retained | Shared rule/prompt bodies preserved; tool instructions adapted; all hosts read the same files | Compliant; generated output not exercised |
| FR-006 shared config/fallbacks | prose/scripts/resolve_style_config.py; prose/docs/harnesses.md; fixture precedence and legacy-only-profile tests | Compliant |
| FR-007 idempotent initialization/resources | init_style_config.py real path, no overwrite prompt, missing-resource check; preservation/rerun/symlink tests | Compliant |
| FR-008 capability discovery | harnesses.md and README capability mapping; Codex/OpenCode native names match | Compliant |
| FR-009 tools | Common guide loaded by every skill; native interaction/worker mapping and disclosed inline fallback | Compliant |
| FR-010 source maintenance | commands/update-humanizer.md; .humanizer-sync; no mandatory canonical Claude copy; dry-run guard | Compliant at instruction level |
| FR-011 Claude compatibility | Existing commands/config homes retained; Claude plugin/marketplace validation and initializer regression tests | Compliant |
| FR-012 documented installs/limits | README, help/tutorial adaptation, quickstart validation record | Compliant |

Functional requirements: 12/12. All seven listed edge/error classes have handling in the common guide, source mapper, initializer or existing upstream workflow. No spec-declared Constants section exists. No extra writing algorithms, migration, external consumer changes, or other-harness integrations were added. Shared discovery is a supporting mechanism for the declared configuration contract.

## Perspective checks

- Correctness: precedence, fallback, idempotence, native skill payloads, dry-run and missing-resource handling checked; findings fixed above.
- Architecture: one source tree, one configuration helper and one guide; adapters register or reference sources without policy copies.
- Security: no credential reads or permission overrides introduced; source discovery is read-only; integration probes use temporary user homes and local servers; no unsafe argument evaluation added.
- Readiness: actionable registration/resource errors; per-skill rejection contained within deferred V2 callback; startup async behavior documented.
- Test quality: tests exercise byte preservation, stdin closure, missing resources, real-path resolution, conflicting voice names, delayed callback rejection and native install/discovery. No model output is claimed as tested.
- Goal alignment: Codex completed before OpenCode; both expose original five capabilities plus command equivalents; shared data root follows the user's explicit decision.

## Validation and limitations

`make test-multi-harness`: 11 Python tests and 5 Node tests pass after fixes. Native Codex isolated install and skills/list pass; native OpenCode 2.1.4 discovery passes. npm dry-run packaging includes native entry points and required prose resources. Claude marketplace and plugin validation pass; missing listing icon is an existing advisory warning.

OpenCode V1 has hook contract tests, not live host validation. Remote Git package installation awaits publication. Generated prose, voice extraction, and live upstream sync were not exercised. Independent review was unavailable under the user restriction; CodeRabbit additionally failed authentication. These limitations are recorded, not treated as runtime proof.

Submit verification additionally removed an unused initializer argument/import, a redundant template directory check, and unnecessary intermediate voice sorting. The complete 16-test suite and Claude manifest checks passed afterward; see VERIFICATION.md.

## Finish follow-up

A subsequent GitHub CodeRabbit review posted eight comments (one Major, seven Minor) after submission. The Major runbook issue and its related failed-cd comment were verified and corrected: workspace creation and writes now have nonempty-variable guards and directory-change dependencies. Fault probes confirmed failed mktemp, missing workspace variables, and failed cd all stop execution. The make prerequisite and distinction between local and authenticated walkthrough coverage were also clarified. Other Minor review suggestions remain for review; no source implementation was changed during this finish pass. The actual local runbook then passed all five steps.
