---
name: ue5-world-interaction
description: UE5.6/UE5.7 world interaction systems for pickups, spawners, overlap/trace checks, and visual feedback. Use when requests involve interactive world actors, spawn logic, pickup behavior, interaction radius checks, success/failure feedback, and actor lifecycle control.
---

# Quick Start
- Define interaction model: overlap-driven, trace-driven, or explicit use key.
- Define actor set: pickup actor, optional spawner, optional visual mapping data asset.
- Output runtime state transitions from spawn to interaction resolution.

# Workflow
- Build actor components (root, collision, visual mesh/effect) and defaults.
- Implement interaction eligibility checks (distance, authority, target validity).
- Apply gameplay effect on success and failure with explicit result object.
- Add visual/audio feedback and optional UI toast hooks.
- Finalize lifecycle policy: destroy, disable, or keep actor after interaction.

# Constraints
- Keep interaction validation server-authoritative in multiplayer.
- Ensure collision channels and trace responses are explicit.
- Keep spawner randomization deterministic when reproducibility is needed.
- Avoid hidden side effects in `Tick` without clear need.

# Failure Handling
- If pickup fails due to capacity/conditions, keep actor state stable and report reason.
- If overlap triggers multiple times, guard with active/in-progress state.
- If spawned actors leak, track and clean managed instances on respawn.

# Escalation
- Escalate when design requires persistent world state synchronization across sessions.
- Escalate when system must integrate with GAS ability targeting rules.
