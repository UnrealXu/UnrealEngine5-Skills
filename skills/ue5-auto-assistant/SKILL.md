---
name: ue5-auto-assistant
description: UE5.6/UE5.7 automatic assistant entry for beginners. Use when users ask Unreal questions without naming a specific skill. Auto-route to the most precise UE5 skill and recommend dedicated MCP tools.
---

# Quick Start
- Treat this as the default entry for UE5.6/UE5.7 requests.
- Parse user intent first without requiring module names.
- Route to `ue5-module-router` when module-level precision is needed.

# Workflow
- Detect request type: Blueprint, C++, UI, save/load, networking, world interaction, debugging, performance, packaging.
- If module names appear, delegate routing to `ue5-module-router`.
- If module names do not appear, route by intent:
  - Blueprint -> `ue5-blueprint-workflow`
  - C++ gameplay -> `ue5-cpp-gameplay`
  - UI/UMG/Slate -> `ue5-ui-umg-slate`
  - save/load/replication -> `ue5-save-load-replication`
  - pickup/spawner/world interaction -> `ue5-world-interaction`
  - perf/packaging -> `ue5-performance-packaging`
  - debugging/validation -> `ue5-debug-validation`
  - architecture/refactor -> `ue5-architecture`
- Return one primary skill and optional secondary skill for cross-domain requests.
- Return routing payload fields:
  - `primary_skill`
  - `secondary_skill`
  - `recommended_mcp_tools[]`
  - `route_confidence`
  - `route_reason`

# Natural Language To Skill And Tools
- Blueprint requests:
  - target skill: `ue5-blueprint-workflow`
  - recommended tools: `blueprint_feature_build`, `blueprint_modify`, `blueprint_query`
- C++ gameplay/system requests:
  - target skill: `ue5-cpp-gameplay`
  - recommended tools: `blueprint_query`, `asset_search`, `get_output_log`
- UI/UMG/Slate requests:
  - target skill: `ue5-ui-umg-slate`
  - recommended tools: `blueprint_query`, `blueprint_modify`, `capture_viewport`
- Save/load/replication requests:
  - target skill: `ue5-save-load-replication`
  - recommended tools: `character_data`, `blueprint_query`, `get_output_log`
- World interaction/pickup/spawner requests:
  - target skill: `ue5-world-interaction`
  - recommended tools: `spawn_actor`, `get_level_actors`, `set_property`, `move_actor`
- Performance/packaging requests:
  - target skill: `ue5-performance-packaging`
  - recommended tools: `run_console_command`, `get_output_log`, `capture_viewport`, `open_level`
- Debug/validation requests:
  - target skill: `ue5-debug-validation`
  - recommended tools: `get_output_log`, `asset_search`, `blueprint_query`, `task_list`
- Architecture/module-boundary requests:
  - target skill: `ue5-architecture`
  - recommended tools: `asset_search`, `asset_dependencies`, `asset_referencers`

# Constraints
- Do not require users to know skill names.
- Prefer deterministic routing with explicit reason.
- Keep fallback behavior explicit when confidence is low.
- Prefer dedicated MCP tools before `execute_script`.

# Failure Handling
- If intent is ambiguous, return top 2 route candidates and ask one short clarification.
- If request spans many systems, split into staged route steps.
- Clarification template:
  - `Quick check: do you want A(<candidate_1>) or B(<candidate_2>)?`
  - ask once, then continue.

# Escalation
- Escalate when query depends on plugin/engine source outside indexed scope.
- Escalate when org-level coding standards are required but not available in repo.