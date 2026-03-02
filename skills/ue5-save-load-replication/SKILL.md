---
name: ue5-save-load-replication
description: UE5.6/UE5.7 save/load and multiplayer replication workflow for gameplay systems. Use when requests involve SaveGame schema design, serialization, restore pipelines, RepNotify handling, RPC entry points, and server-authoritative validation.
---

# Quick Start
- Define what must persist and what must replicate.
- Separate local save state from network runtime state.
- Output data schema, save flow, load flow, and net flow.

# Workflow
- Define save structs and identifiers for stable serialization.
- Build save data from runtime component state.
- Restore runtime state with validation and conflict handling.
- Add replication fields with RepNotify for client updates.
- Add RPC entry points for client requests and server authority checks.

# Constraints
- Server is source of truth for replicated gameplay state.
- Validate all client-requested actions before applying state changes.
- Keep SaveGame schema versionable; avoid fragile implicit ordering.
- Do not assume single-player behavior in multiplayer code paths.

# Failure Handling
- If save schema changes, provide backward-compat migration or version gate.
- If restore fails partially, return structured operation result and keep state consistent.
- If RepNotify storms occur, batch or debounce state updates.

# Escalation
- Escalate when changes break existing save compatibility policy.
- Escalate when replication design impacts anti-cheat or authoritative architecture decisions.
