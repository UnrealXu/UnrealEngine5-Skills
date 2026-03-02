# Routing Policy (UE5.6/UE5.7)

## Priority Order
1. Exact module name match in routing table.
2. Exact Build.cs path segment match.
3. Alias/keyword match from routing table.
4. Domain fallback from module index v2.

## Confidence Levels
- High: `route_reason=module_override` or exact module hit with stable mapping.
- Medium: `route_reason=domain_mapping` with non-`General` domain.
- Low: fallback on `General` domain + weak alias evidence.

## Output Contract
- `primary_skill`
- `secondary_skill` (if present)
- `recommended_mcp_tools[]`
- `matched_modules[]`
- `route_reason`
- `route_confidence`

## Tool Priority Matrix
- Blueprint requests:
  - Prefer: `blueprint_feature_build`, `blueprint_modify`, `blueprint_query`
  - Then: `enhanced_input`, `get_output_log`
  - Last resort: `execute_script`
- World interaction requests:
  - Prefer: `spawn_actor`, `get_level_actors`, `set_property`, `move_actor`, `delete_actors`, `open_level`
  - Then: `capture_viewport`, `get_output_log`
  - Last resort: `execute_script`
- Save/load/network requests:
  - Prefer: `character_data`, `blueprint_query`, `blueprint_modify`, `asset`, `asset_search`
  - Then: `get_output_log`, `task_*`
  - Last resort: `execute_script`
- Performance/packaging requests:
  - Prefer: `run_console_command`, `get_output_log`, `capture_viewport`, `open_level`, `asset_dependencies`, `asset_referencers`
  - Then: `task_*`
  - Last resort: `execute_script`
- Debug/validation requests:
  - Prefer: `get_output_log`, `asset_search`, `blueprint_query`, `get_level_actors`, `task_list`, `task_status`, `task_result`
  - Then: `capture_viewport`
  - Last resort: `execute_script`

## execute_script Fallback Conditions
Use `execute_script` only when all conditions are met:
1. No dedicated tool supports the required operation.
2. The request cannot be decomposed into existing MCP tool calls.
3. The reason is explicitly stated in the response.
4. Script scope is minimal and reversible where possible.
