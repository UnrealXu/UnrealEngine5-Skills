---
name: ue5-world-interaction
description: UE5.6/UE5.7 world interaction systems for pickups, spawners, overlap/trace checks, and visual feedback. Use when requests involve interactive world actors, spawn logic, pickup behavior, interaction radius checks, success/failure feedback, and actor lifecycle control.
---

# Quick Start
- Define interaction model: overlap-driven, trace-driven, or explicit use key.
- Define actor set: pickup actor, optional spawner, optional visual mapping data asset.
- Output runtime state transitions from spawn to interaction resolution.

# UE5.7 API Anchors
- Detection anchors:
  - `USphereComponent`, `UBoxComponent`
  - `UPrimitiveComponent::OnComponentBeginOverlap`
  - `UPrimitiveComponent::OnComponentEndOverlap`
  - `FHitResult`
- Trace anchors:
  - `UWorld::LineTraceSingleByChannel(...)`
  - `UWorld::SweepSingleByChannel(...)`
  - `UKismetSystemLibrary::SphereTraceSingle(...)`
- Lifecycle anchors:
  - `AActor::SetActorHiddenInGame(...)`
  - `AActor::SetActorEnableCollision(...)`
  - `AActor::Destroy(...)`
  - `AActor::SetActorTickEnabled(...)`
- Networking anchors:
  - server authority validation for interaction success
  - replicated result state for client feedback

# Interaction Stage Contract
- Every interaction feature must define:
  - Detection source (overlap/trace/use-key)
  - Eligibility checks (distance, tags, inventory/capacity, authority)
  - Success and failure result payloads
  - Feedback path (VFX/SFX/UI)
  - Post-interaction lifecycle policy (destroy/disable/cooldown/respawn)
- If any item is missing, interaction behavior is underspecified.

# Workflow
## 1) Actor and Component Setup
- Build root + collision + visual components with explicit collision channels.
- Define default states (`active`, `cooldown`, `consumed`) and replication needs.
- Keep collision shape and bounds aligned with intended interaction distance.

## 2) Detection Path
- Overlap model: bind begin/end overlap delegates on collision component.
- Trace model: run line/sphere traces on input request and validate hit actor/component.
- Keep detection deterministic by explicit channels/profiles.

## 3) Eligibility and Authority
- Validate target state, range, actor validity, and gameplay conditions.
- In multiplayer, validate success on server before mutating shared state.
- Return structured failure reason on rejection.

## 4) Resolve Interaction
- On success: apply effect (grant item, trigger state change, start cooldown).
- On failure: keep state stable and emit reason-specific feedback.
- Prevent re-entrant execution during in-progress resolution.

## 5) Feedback Path
- Emit VFX/SFX/UI feedback for both success and failure paths.
- Separate cosmetic-only effects from authoritative gameplay mutations.
- Keep feedback idempotent for repeated client updates.

## 6) Lifecycle and Cleanup
- Choose lifecycle explicitly: destroy, hide+disable collision, or reuse via respawn timer.
- If spawner exists, track spawned instances and cleanup on reset/despawn.
- Disable tick for dormant interaction actors when not needed.

# Constraints
- Keep interaction validation server-authoritative in multiplayer.
- Ensure collision channels and trace responses are explicit.
- Keep spawner randomization deterministic when reproducibility is needed.
- Avoid hidden side effects in `Tick` without clear need.
- Do not destroy actors before broadcasting required success/failure feedback.
- Keep overlap and trace paths functionally equivalent when both are enabled.

# Failure Handling
- Symptom: overlap never triggers.
  - Locate: collision enabled state, overlap flags, collision channel responses.
  - Fix: enable overlap generation, set proper channel responses, verify component bounds.
- Symptom: trace path misses obvious targets.
  - Locate: trace channel/profile and ignore actor list.
  - Fix: align trace channel/profile and reduce self/owner ignore misuse.
- Symptom: interaction triggers multiple times.
  - Locate: missing in-progress guard and duplicated delegate bindings.
  - Fix: add state guard and ensure single bind per component.
- Symptom: client sees success but server rejects.
  - Locate: authority checks and RPC validation path.
  - Fix: move final validation to server and replicate authoritative result.
- Symptom: consumed pickup remains interactable.
  - Locate: lifecycle state and collision disable logic.
  - Fix: disable collision/interaction immediately after confirmed success.
- Symptom: spawned interactables leak over time.
  - Locate: spawner bookkeeping and reset cleanup path.
  - Fix: track spawned instances and destroy/disable stale instances on respawn cycle.
- Symptom: frame spikes near dense interaction areas.
  - Locate: per-frame trace/overlap workload and unnecessary ticking.
  - Fix: reduce polling frequency, gate traces by input/distance, disable idle tick.

# Interaction Authority Ops
- Use server-validated interaction resolution for shared gameplay effects.
- Use client-side prediction only for cosmetic feedback when acceptable.
- Replicate result state, not raw input spam.
- Keep cooldown/timer ownership on authority side for deterministic multiplayer behavior.

# UE5.6 / UE5.7 Compatibility Notes
- Overlap, trace, and actor lifecycle APIs listed above are stable across UE5.6 and UE5.7.
- Prefer explicit collision profile/channel configuration in both versions.

# Escalation
- Escalate when design requires persistent world state synchronization across sessions.
- Escalate when system must integrate with GAS ability targeting rules.
