# Tooltip Patterns

## Placement
- Anchor near cursor or target widget.
- Apply fixed offset.
- Flip horizontally/vertically when near viewport edges.
- Clamp final position to viewport bounds.

## Content
- First line: item display name and quantity.
- Second line: short description or fallback text.

## Lifecycle
- Show on hover enter.
- Update position while active.
- Hide immediately on hover leave or invalid target.
