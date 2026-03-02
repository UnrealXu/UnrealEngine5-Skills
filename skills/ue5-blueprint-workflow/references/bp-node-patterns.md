# Blueprint Node Patterns

## Feature Chain Pattern
- Entry event
- Guard branch (optional)
- Core action node(s)
- Output feedback (`PrintString` or UI update)

## Pin Wiring Pattern
- Connect exec flow first.
- Then connect data pins.
- Set defaults only when data source is absent.

## Validation Pattern
- Inspect node pins for dynamic nodes before final wiring.
- Compile after each logical chunk to isolate faults.
