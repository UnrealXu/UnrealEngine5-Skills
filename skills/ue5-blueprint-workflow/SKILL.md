---
name: ue5-blueprint-workflow
description: UE5.6/UE5.7 Blueprint graph workflow for feature implementation, input events, node wiring, and graph validation. Use when requests involve adding Blueprint logic, keyboard input behavior, function chains, event graph edits, or pin-level connection guidance.
---

# Quick Start
- Identify target Blueprint asset and graph (`EventGraph` or function graph).
- Confirm requested behavior as event -> logic -> output chain.
- Produce graph-level steps first, then exact node/pin wiring details.

# Workflow
- Add or reuse input events using hotkey fast path first.
- For keyboard input, create/reuse key node with `add_input_key_event` before generic node guesses.
- Build logic with minimal nodes, then connect exec/data pins explicitly.
- Validate graph by checking node pins and compile status.
- Summarize final node chain in deterministic order.

# Constraints
- Mandatory hotkey rule: use `add_input_key_event` first for keyboard features.
- Keep `reuse_existing=true` for key events to avoid duplicates.
- Avoid trial-and-error node class guessing when a dedicated operation exists.
- Separate graph steps from pin-level detail in final output.

# Failure Handling
- If build fails, report blockers and suggest exact next action per blocker.
- If pin names differ by node variant, inspect node pins before wiring.
- If graph has multiple candidate entry events, pick the one matching user input context and state assumption.

# Escalation
- Escalate when behavior requires C++ extension, custom latent nodes, or engine plugin changes.
- Escalate when Blueprint is locked, corrupted, or cannot compile due to unrelated project errors.
