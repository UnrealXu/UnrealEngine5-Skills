---
name: ue5-ui-umg-slate
description: UE5.6/UE5.7 UI development workflow using UMG and Slate integration. Use when requests involve Widget Blueprint setup, Slate host widgets, lifecycle binding, input and focus handling, tooltip behavior, or viewport clamping logic.
---

# Quick Start
- Identify whether feature belongs to UMG, Slate, or hybrid bridge.
- Define data source component/subsystem and UI binding point.
- Output widget tree intent and runtime binding sequence.

# Workflow
- Create or update UMG widget and required exposed variables.
- Build Slate widget when custom grid/input rendering is required.
- Bridge UMG and Slate through a host `UWidget` wrapper.
- Bind runtime data on construct/init and subscribe to change events.
- Handle focus, visibility, and tooltip screen-edge clamp behavior.

# Constraints
- Keep UI rendering and gameplay state mutation separated.
- Avoid direct gameplay writes from passive display widgets.
- Clamp tooltip and popup placement to viewport bounds.
- Prefer deterministic input ownership and focus transitions.

# Failure Handling
- If widget does not refresh, verify binding lifecycle and event subscription timing.
- If input is swallowed, inspect focus path and input mode conflicts.
- If tooltip flickers, debounce hover source and clamp updates per frame.

# Escalation
- Escalate when behavior requires engine-level Slate customization beyond project scope.
- Escalate when UI architecture conflicts with existing CommonUI framework decisions.
