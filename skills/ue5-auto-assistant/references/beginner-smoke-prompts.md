# Beginner Smoke Prompts (UE5.6/UE5.7 MCP + Skill)

Use these prompts to validate natural-language routing and MCP tool priority.

## How To Use
- Start a new Codex session.
- Paste one case at a time.
- Do not include skill names in prompts.
- Verify expected routing and recommended tools.

## Case 1: Save/Load
Prompt: `Inventory is empty after load. Where should I debug first?`
Expected:
- primary skill: `ue5-save-load-replication`
- recommended tools include `get_output_log`, `blueprint_query`

## Case 2: Module-Specific
Prompt: `How do I debug material compile stalls in RenderCore?`
Expected:
- routed by `ue5-module-router`
- high confidence when exact module match exists

## Case 3: Blueprint Hotkey
Prompt: `In Blueprint, press key 2 to jump and print a log. How do I wire this?`
Expected:
- primary skill: `ue5-blueprint-workflow`
- fast-path for keyboard input (`add_input_key_event` first)

## Case 4: World Interaction
Prompt: `I want pickup items that auto-collect when player enters range.`
Expected:
- primary skill: `ue5-world-interaction`
- tools include `spawn_actor`, `get_level_actors`, `set_property`

## Case 5: UI
Prompt: `My tooltip is clipped at viewport edges. How should I clamp it?`
Expected:
- primary skill: `ue5-ui-umg-slate`
- tools include `blueprint_query`, `blueprint_modify`, `capture_viewport`

## Case 6: Performance/Packaging
Prompt: `Give me a pre-package checklist and profiling order.`
Expected:
- primary skill: `ue5-performance-packaging`
- tools include `run_console_command`, `get_output_log`

## Pass Criteria
- correct routing for each prompt
- dedicated MCP tools prioritized over `execute_script`
- one clarification only when confidence is low