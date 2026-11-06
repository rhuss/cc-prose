# Feature Specification: Multi-harness support

**Feature Branch**: `006-multi-harness-support`
**Created**: 2026-11-06
**Status**: Draft
**Input**: Brainstorm 07, including the 2026-11-06 revisit: Codex first, then OpenCode; shared skills and behavior parity.

## Overview

Make cc-prose available to writing users and consumers such as cc-guide on Codex and OpenCode. Users need the same voice profiles, content generation, rewriting, and AI-pattern validation they receive on Claude Code. Deliver Codex support before OpenCode, preserving the existing Claude Code installation and writing workflows.

## Clarifications

### Session 2026-11-06 (Smart mode)

- Q: Does parity require identical generated prose? → A: No; it requires identical source rules, profile selection, and workflow steps (FR-005).
- Q: Must native invocation strings remain literal `prose:*`? → A: No; publish a capability mapping to native syntax (FR-004, FR-008).
- Q: Should existing user data move automatically? → A: No automatic relocation or deletion; retain legacy reads (FR-006 and User Story 2).
- Q: What if a review tool is unavailable? → A: Follow the same review inline using supported harness tools (FR-009).

### User decision 2026-11-06

- Q: Where should global styles and voices live? → A: Keep `~/.claude/style/` shared by Claude Code, Codex, and OpenCode, retaining existing legacy fallbacks and copyedit compatibility.

## User Scenarios & Testing

### User Story 1 - Write and validate in Codex (Priority: P1)

A user installs cc-prose in Codex, selects an existing voice, generates or rewrites content, and checks it for AI patterns. A consuming workflow discovers the installed capabilities from the active session.

**Why this priority**: Codex is the primary missing integration for cc-guide.
**Independent Test**: Install in an isolated Codex setup, invoke all five writing skills and the six command-equivalent workflows, and generate and check a document using a named voice.

**Acceptance Scenarios**:
1. **Given** a supported Codex installation, **When** the user follows the documented install steps, **Then** all five shared writing skills are discoverable and usable.
2. **Given** cc-prose is installed, **When** a consumer looks at session capabilities, **Then** it can identify content generation, humanization, and validation without reading an installation registry.
3. **Given** a named voice and sample document, **When** write, rewrite, voice, check, init, or update-humanizer is requested, **Then** the corresponding workflow is available with documented invocation syntax.

### User Story 2 - Reuse writing configuration across harnesses (Priority: P1)

A writer switches harnesses and retains their global voice library and project style rules.

**Why this priority**: Losing profiles while switching harnesses defeats the purpose of portability.
**Independent Test**: Initialize configuration using an isolated home, create a voice, and resolve the same profile and rules from each supported harness's documented workflow.

**Acceptance Scenarios**:
1. **Given** project and global configuration, **When** any supported harness resolves settings, **Then** it uses the same precedence: built-in defaults, global configuration, then project configuration; additive wordlists, stoplists, and styleguides retain their existing behavior.
2. **Given** existing Claude style and voice configuration, **When** a new harness uses cc-prose, **Then** existing data remains readable without automatic relocation or deletion.
3. **Given** existing configuration files, **When** initialization runs twice, **Then** existing files are preserved.

### User Story 3 - Use the same workflows in OpenCode (Priority: P2)

An OpenCode user installs cc-prose and uses the shared writing workflows after Codex support is implemented.

**Why this priority**: OpenCode is the agreed secondary harness.
**Independent Test**: Follow installation instructions in an isolated OpenCode setup and exercise the same workflow and configuration matrix as Codex.

**Acceptance Scenarios**:
1. **Given** a supported OpenCode setup, **When** installed as documented, **Then** the same five skills and six command-equivalent workflows are available.
2. **Given** the same content and configuration, **When** a workflow runs on OpenCode, **Then** it follows the same voice-selection and validation rules as Claude Code and Codex.

### Edge Cases and Error Handling

- Missing optional configuration: use built-in defaults; retain existing project and legacy fallbacks.
- Duplicate profile names: apply a documented, deterministic precedence shared by all harnesses.
- Initialization of existing files: skip existing files and identify them in output.
- Missing question or subagent tools: use the harness's supported interaction mechanism; when delegation is unavailable, perform the same review inline.
- Missing capability: consumers report it as unavailable rather than assuming installation based on a registry or path.
- Missing plugin resources: report the missing resource and installation remedy rather than guessing a Claude cache path.
- Upstream network or tracking errors: report the error and preserve local skills and tracking state, following the existing update workflow.

## Requirements

### Functional Requirements

- **FR-001**: Users MUST be able to install cc-prose using documented Codex integration conventions and discover all five writing skills.
- **FR-002**: Users MUST be able to install cc-prose using documented OpenCode integration conventions and discover the same five skills after Codex support is implemented.
- **FR-003**: All harnesses MUST use one authoritative source for each writing workflow; adapters MUST NOT duplicate writing policy.
- **FR-004**: Each harness MUST expose equivalents for write, rewrite, voice, check, init, and update-humanizer with documented native invocation syntax. Literal command spelling MAY differ by harness.
- **FR-005**: Voice selection, measurement interpretation, humanizer patterns, and validation scoring MUST retain the existing writing rules on every supported harness. Parity means shared rules and workflows, not identical generated text.
- **FR-006**: All supported harnesses MUST use `~/.claude/style/` as the shared global directory and resolve the same project style configuration and voice library with documented deterministic precedence, preserving existing legacy fallbacks and copyedit configuration compatibility.
- **FR-007**: Initialization MUST support project and global use, preserve existing files, and resolve bundled resources independently of a Claude installation path.
- **FR-008**: Consumers MUST be able to discover generation, humanization, and validation capabilities from the active session. Documentation MUST map native names to these capabilities and describe absence handling.
- **FR-009**: All skills and command-equivalent workflows MUST handle harness tool differences without requiring unavailable Claude tools or Claude environment variables.
- **FR-010**: The humanizer update workflow MUST operate on the authoritative cc-prose skill and tracking state without requiring a separate Claude user skill copy. Existing local additions and dry-run behavior MUST be preserved.
- **FR-011**: Claude Code installation, commands, existing style configuration, and upstream humanizer maintenance MUST continue to work.
- **FR-012**: Installation and usage documentation MUST distinguish the three supported harnesses and state prerequisites and any unverified runtime limitations.

### Key Entities

- **Harness entry point**: native metadata or adapter exposing shared workflows in one supported harness.
- **Voice profile**: existing reusable writing parameters and optional extracted measurements, identified by name and source location.
- **Style configuration**: global or project settings, rules, vocabulary, and active voice with explicit precedence.
- **Capability mapping**: mapping from generation, humanization, and validation to actual session-visible names.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Each supported harness exposes all five writing skills and all six command-equivalent workflows in an installation and invocation matrix.
- **SC-002**: A shared fixture matrix resolves identical configuration precedence and profile selection across all three harnesses, including project overrides and legacy fallback cases.
- **SC-003**: Every writing policy remains in one authoritative source, and adapter checks detect duplicated or missing workflow mappings.
- **SC-004**: Initialization is idempotent and preserves every existing file in the configuration fixtures.
- **SC-005**: All available local checks for packaging, configuration, and existing Claude integration pass; manual session checks are recorded separately with their actual results.

## Assumptions and Constraints

- macOS and Linux with Python 3 and standard shell tooling are the initial supported environments, consistent with the current tooling.
- Existing profile schemas and writing algorithms remain unchanged.
- The current constitution is an unfilled template and supplies no additional ratified constraints.
- Harness-native invocation syntax takes precedence over assuming `prose:*` names are universal.
- Other harnesses, changes to cc-guide itself, automatic data migration, and new writing behavior are outside this pass.
- Runtime availability and authenticated harness sessions may limit end-to-end validation; static validation must not be reported as runtime proof.
