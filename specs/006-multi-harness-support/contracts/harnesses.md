# Harness contract

| Capability | Source skill | Claude | Codex | OpenCode |
|---|---|---|---|---|
| Generate | content-generator | prose:content-generator | prose:content-generator | content-generator |
| Humanize | humanizer | prose:humanizer | prose:humanizer | humanizer |
| Validate | pre-validator | prose:pre-validator | prose:pre-validator | pre-validator |
| Manage voices | voice-architect | prose:voice-architect | prose:voice-architect | voice-architect |
| Extract voices | voice-extractor | prose:voice-extractor | prose:voice-extractor | voice-extractor |

Consumers inspect session-visible skills for the mapped capabilities; presence of a package or registry entry is insufficient. If one capability is missing, report it and use only the consumer's documented fallback. Command equivalents use the six thin skills on Codex/OpenCode and existing `/prose:<action>` commands on Claude. Native invocation names must be confirmed with installation discovery, not inferred from registry data.

Configuration: `resolve_paths(project_dir, home)` returns source paths only. Apply numeric thresholds global then project; combine vocabulary and rule files as before. Named-profile selection uses project active voice first, then unified global name, then legacy global name. Missing optional paths are omitted/null. Every returned path must exist. No config or profile writes occur during discovery.
