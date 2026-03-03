---
name: ue5-save-load-replication
description: UE5.6/UE5.7 save/load and multiplayer replication workflow for gameplay systems. Use when requests involve SaveGame schema design, serialization, restore pipelines, RepNotify handling, RPC entry points, and server-authoritative validation.
---

# Quick Start
- Define what must persist and what must replicate.
- Separate local save state from network runtime state.
- Output data schema, save flow, load flow, and net flow.

# UE5.7 API Anchors
- Save pipeline anchors:
  - `USaveGame`
  - `UGameplayStatics::CreateSaveGameObject(...)`
  - `UGameplayStatics::SaveGameToSlot(...)`, `LoadGameFromSlot(...)`
  - `UGameplayStatics::AsyncSaveGameToSlot(...)`, `AsyncLoadGameFromSlot(...)`
- Replication anchors:
  - `GetLifetimeReplicatedProps(...)`
  - `DOREPLIFETIME(...)`
  - `ReplicatedUsing=OnRep_*`
  - `UFUNCTION(Server/Client/NetMulticast, ...)`
- Authority anchors:
  - server-authoritative mutation path
  - client requests routed through validated server RPC entry points

# State Contract
- Every state field must be classified as one of:
  - Persistent-only (SaveGame, not replicated)
  - Replicated-only (runtime sync, not persisted)
  - Persistent + replicated (authoritative state with save restore)
- Every persisted schema must include:
  - explicit version integer
  - stable identifiers/keys (avoid index-based implicit ordering)
  - migration behavior for older versions
- Every replicated field must define:
  - replication condition or scope
  - `OnRep_*` behavior on clients
  - server write ownership

# Workflow
## 1) Partition State
- Identify gameplay state by ownership: local player, world/shared, match/session.
- Split ephemeral runtime values from persistent values.
- Mark authoritative write path for each field.

## 2) Save Schema
- Define save structs/objects with explicit schema version.
- Use stable keys/IDs for actors, components, and inventory-like entries.
- Include optional migration metadata for backward compatibility.

## 3) Save Pipeline
- Gather runtime state into save schema in deterministic order.
- Write through sync or async slot APIs based on latency sensitivity.
- Return structured save result (success, failure reason, version used).

## 4) Load and Restore Pipeline
- Load save object, validate version, run migration if needed.
- Apply restore in dependency-safe order (owners before dependents).
- Resolve missing assets/entities with explicit fallback policy.

## 5) Replication Pipeline
- Replicate only client-visible runtime state.
- Register replicated properties with `DOREPLIFETIME(...)`.
- Use `OnRep_*` for client-side reconstruction/UI refresh, not authority writes.

## 6) RPC Authority Pipeline
- Use client->server RPC for requested actions.
- Validate payloads on server before mutating replicated state.
- Broadcast resulting state via replication/NetMulticast only when needed.

# Constraints
- Server is source of truth for replicated gameplay state.
- Validate all client-requested actions before applying state changes.
- Keep SaveGame schema versionable; avoid fragile implicit ordering.
- Do not assume single-player behavior in multiplayer code paths.
- Keep restore process idempotent where possible (safe to retry after partial failure).
- Avoid persisting transient network-only caches.

# Failure Handling
- Symptom: load succeeds but gameplay state is inconsistent.
  - Locate: restore ordering and missing dependency handling.
  - Fix: apply owners/components/dependents in staged restore order with fallback defaults.
- Symptom: old save files break after update.
  - Locate: schema version checks and migration path.
  - Fix: add explicit migration per version or gate unsupported versions cleanly.
- Symptom: replicated value differs from saved value after reconnect.
  - Locate: authority write path and restore timing vs replication timing.
  - Fix: restore on authority first, then let replication propagate to clients.
- Symptom: `OnRep_*` spam causes frame spikes.
  - Locate: frequent property churn and large payload replication.
  - Fix: batch updates, replicate coarse state, derive fine state client-side.
- Symptom: client can trigger unauthorized state changes.
  - Locate: RPC validation and authority checks.
  - Fix: enforce server validation and reject invalid client payloads.
- Symptom: async save/load callbacks race with gameplay transitions.
  - Locate: callback lifecycle and stale object references.
  - Fix: guard callbacks with state tokens and world validity checks.
- Symptom: partial restore leaves orphaned actors/components.
  - Locate: failure rollback path.
  - Fix: stage restore transactions and cleanup created artifacts on failure.

# Replication Ops
- Use `ReplicatedUsing` when client-side side effects are required.
- Use RPC only for intent transfer, not as persistent state storage.
- Use replication for authoritative state fan-out; use SaveGame for disk persistence.
- Never trust client-local save data as authoritative multiplayer input.

# UE5.6 / UE5.7 Compatibility Notes
- SaveGame and replication APIs listed above are stable across UE5.6 and UE5.7.
- Prefer stable Engine runtime APIs over project-specific serialization shortcuts.

# Escalation
- Escalate when changes break existing save compatibility policy.
- Escalate when replication design impacts anti-cheat or authoritative architecture decisions.
