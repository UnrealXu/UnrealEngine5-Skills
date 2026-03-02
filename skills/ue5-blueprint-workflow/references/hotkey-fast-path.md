# Hotkey Fast Path

## Mandatory Sequence
1. `blueprint_modify(operation=add_input_key_event, key_name=..., reuse_existing=true)`
2. Query or inspect pins only if needed.
3. Connect exec and data pins.
4. Validate graph compile result.

## Key Names
- Use UE key names like `One`, `SpaceBar`, `A`, `LeftMouseButton`.
- Digits like `"1"` are acceptable if tooling normalizes them.

## Anti-Pattern
- Do not try multiple generic `NodeClass/Event` guesses before the fast path.
