# Verification: Multi-harness support

Date: 2026-11-06
Spec: [spec.md](spec.md)
Result: PASS

## Fresh checks

- `make test-multi-harness`: 11 Python tests and 5 Node tests pass, zero failures.
- `make validate`: marketplace and plugin validation pass; existing missing-listing-icon advisory remains.
- `git diff --check` and `git diff --cached --check`: pass.
- `bash -n scripts/check-upstream-changes.sh`: pass.
- Runbook structure check: RUNBOOK_CHECK_PASS; runbook remains drafted, not executed.
- Closeout script: CLOSEOUT_SKIP; manual check of review-findings.md confirms zero unresolved Critical/Important findings.

## Code hygiene

Reviewed every changed implementation and invocation file. Removed the initializer's unused project-mode plugin_root argument and unused typing import; removed a redundant validated-template lookup/conditional and unnecessary intermediate voice ordering. Config discovery does not mutate data, V1 path registration deduplicates deliberately, and V2 rejects individual payloads without aborting the batch. No orphaned resource references, new secret handling, or unbounded background work was introduced.

## Functional compliance

| Requirement | Status | Evidence |
|---|---|---|
| FR-001 | IMPLEMENTED | prose/.codex-plugin/plugin.json and .agents/plugins/marketplace.json; native isolated install plus app-server discovery |
| FR-002 | IMPLEMENTED | package.json, index.js, .opencode/plugins/prose.js:setup; native OpenCode 2.1.4 discovery |
| FR-003 | IMPLEMENTED | adapters read the original shared files; invocation skills reference commands; packaging tests |
| FR-004 | IMPLEMENTED | six action skills in prose/skills/ and README native invocation matrix; native names confirmed |
| FR-005 | IMPLEMENTED | original writing policy and audit prompt bodies retained; tool substitutions reference common guide |
| FR-006 | IMPLEMENTED | resolve_style_config.py:resolve_paths and shared guide; configuration precedence/duplicate-name fixtures |
| FR-007 | IMPLEMENTED | init_style_config.py:get_plugin_root/init_project_config/init_global_config; repeated/closed-stdin/missing-template/symlink tests |
| FR-008 | IMPLEMENTED | prose/docs/harnesses.md:Consumer detection and session-visible native capability names |
| FR-009 | IMPLEMENTED | common guide loaded by all eleven skills; native tools, permitted delegation and disclosed inline fallback |
| FR-010 | IMPLEMENTED | prose/commands/update-humanizer.md:checkout prerequisite, initial-baseline dry-run guard, source-only maintenance; tracking metadata |
| FR-011 | IMPLEMENTED | Claude commands retained, shared global/legacy roots retained, original upstream check script retained; Claude validation and regression fixtures |
| FR-012 | IMPLEMENTED | README installation/invocation matrix, help/tutorial mappings, quickstart limitations |

```text
SPEC_COMPLIANCE_RESULT:
  total: 12
  implemented: 12
  missing: 0
  percentage: 100%
  gate: PASS
```

## Drift and success criteria

No drift from the agreed scope: Codex then OpenCode, shared source and global directory, existing profile schemas, no migration or new writing algorithm. The source-discovery helper supports the declared precedence contract.

| Criterion | Status | Evidence |
|---|---|---|
| SC-001 | Met | Native Codex/OpenCode discovery of original five skills and six action equivalents; Claude manifest validation and common invocation matrix |
| SC-002 | Met | Shared resolver fixtures cover empty roots, global/project layers, legacy fallback, named voice collisions, and project voice precedence; all harness instructions use the same source map |
| SC-003 | Met | Shared original files, six wrapper-to-command mapping checks, and V2 registration payload checks |
| SC-004 | Met | Closed-stdin reruns preserve custom bytes and fill missing files; eight templates copied |
| SC-005 | Met | Fresh local checks pass; actual native results and unrun manual checks recorded in quickstart.md |

All seven specified error/edge classes are handled by the guide, resolver, initializer or preserved upstream workflow. All ten implementation tasks are checked.

## Limits of evidence

Native installation/discovery was exercised during implementation; this verification reran the complete local test and manifest suite after hygiene changes. No generated prose, live voice extraction, actual upstream merge, or OpenCode V1 host was exercised. The runbook has five pending steps. Code review was inline; CodeRabbit failed authentication, and independent subagents were not authorized. These limits do not claim end-to-end model behavior was tested.
