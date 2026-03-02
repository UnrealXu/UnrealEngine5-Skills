# UMG + Slate Bridge Pattern

## When to Use
- Use UMG for layout, animation, and designer iteration.
- Use Slate for custom drawing, dense grid logic, or low-level input handling.

## Bridge Shape
- `UWidget` host class owns `TSharedPtr<SWidget>`.
- `RebuildWidget()` creates Slate instance.
- Blueprint API on host widget forwards data/config to Slate widget.

## Data Updates
- Prefer event-driven refresh from gameplay component delegates.
- Avoid per-frame polling when data change events are available.
