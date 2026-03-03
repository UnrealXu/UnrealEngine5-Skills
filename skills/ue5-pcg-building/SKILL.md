---
name: ue5-pcg-building
description: UE5.6/UE5.7 PCG building generation workflow for modular buildings, blockouts, facade rules, and runtime generation. Use when requests involve Procedural Content Generation (PCG), Shape Grammar, lot-based building spawn, deterministic random seeds, density/filter pipelines, or converting designer constraints into reusable PCG graphs.
---

# Quick Start
- Define generation target: blockout towers, modular facades, or lot-based building sets.
- Define deterministic inputs: lot splines/points, district tags, style preset, and seed.
- Define runtime mode: static bake, on-demand, or runtime scheduled generation.
- Define output mode: Static Mesh instances first, Spawn Actor only for interactive/stateful parts.

# UE5.7 API Anchors
- Runtime trigger and radii live on `UPCGComponent`:
  - `EPCGComponentGenerationTrigger::GenerateAtRuntime`
  - `bOverrideGenerationRadii`, `GenerationRadii`, `SchedulingPolicyClass`, `SchedulingPolicy`
  - `GenerateLocal(...)`, `Cleanup(...)`
- Runtime scheduler refresh lives on `UPCGSubsystem`:
  - `RefreshRuntimeGenComponent(...)`
  - `RefreshAllRuntimeGenComponents(...)`
  - `CleanupLocalComponentsImmediate(...)`
- Output selection anchor classes:
  - `UPCGStaticMeshSpawnerSettings` for high-count rendering
  - `UPCGSpawnActorSettings` for interactive/stateful outputs
- Shape Grammar anchor classes:
  - `UPCGSubdivisionBaseSettings::GrammarSelection`
  - Do not rely on deprecated grammar fields (`bGrammarAsAttribute_DEPRECATED`, `Grammar_DEPRECATED`)

# Graph Stage Contract
- Every stage must explicitly declare:
  - Input data type (`EPCGDataType` or asset source)
  - Core node/classes (minimum two)
  - Required parameters (seed, tags, ranges, radii, or style keys)
  - Output data type
  - Debug method (node-level checks, debug node, or log/assert path)
- If a stage cannot satisfy these five items, treat the graph design as incomplete.

# Workflow
## 1) Input
- Input data type: actor/spline/point sources.
- Core node/classes: `UPCGDataFromActorSettings`, `UPCGGetActorPropertySettings`, `UPCGCreatePointsSettings`.
- Required parameters: lot tag filters, district/style tags, seed source, source bounds.
- Output: normalized lot point or spline data with stable ordering.
- Debug method: run `UPCGDebugSettings` after input stage and verify point count and bounds.

## 2) Filter
- Input data type: point/spline data from Input stage.
- Core node/classes: `UPCGAttributeFilteringSettings`, `UPCGDensityFilterSettings`, `UPCGFilterByTagSettings`.
- Required parameters: slope range, exclusion tags, min lot area/width, occupancy constraints.
- Output: only buildable lots/candidates.
- Debug method: compare candidate count before/after filter and inspect rejected tag distribution.

## 3) Transform
- Input data type: filtered buildable candidates.
- Core node/classes: `UPCGCopyPointsSettings`, `UPCGCreateSplineSettings`, `UPCGApplyScaleToBoundsSettings`.
- Required parameters: floor height, pivot convention, facade orientation basis, local axes.
- Output: footprint transforms and per-floor transforms.
- Debug method: inspect transform axes and floor index attributes on output points.

## 4) Grammar
- Input data type: segment/spline/point data from Transform stage.
- Core node/classes: `UPCGSubdivideSplineSettings`, `UPCGSubdivideSegmentSettings`, `UPCGSelectGrammarSettings`.
- Required parameters: `GrammarSelection`, module size limits, style-based grammar key mapping.
- Output: grammar-resolved module placements/attributes.
- Debug method: use `UPCGPrintGrammarSettings` for grammar parse and token validation.
- Rule: use `GrammarSelection` only; avoid deprecated grammar fields.

## 5) Output
- Input data type: grammar-resolved placements.
- Core node/classes: `UPCGStaticMeshSpawnerSettings`, `UPCGSpawnActorSettings`, `UPCGCreateTargetActor`.
- Required parameters:
  - Static path: mesh selector, instance packer, ISM/HISM policy.
  - Actor path: actor class, spawn attributes, state/interaction requirements.
- Output: rendered buildings and optional interactive building elements.
- Debug method: split output by layer/tag and validate per-layer counts.
- Default policy: prefer Static Mesh Spawner; use Spawn Actor only when stateful behavior is required.

## 6) Validate
- Input data type: final spawned result and runtime generation state.
- Core node/classes: `UPCGDebugSettings`, `UPCGComponent`, `UPCGSubsystem`.
- Required parameters: expected cell bounds, max per-update spawn budget, nav/collision expectations.
- Output: pass/fail signals and fix actions.
- Debug method: run staged checks for overlap, navigation impact, per-cell generation time, and deterministic replay.

# Constraints
- Keep the main pipeline compatible with both UE5.6 and UE5.7 unless a version-specific note is required.
- Runtime generation must explicitly set:
  - `GenerationTrigger = GenerateAtRuntime`
  - explicit `GenerationRadii` (do not rely on implicit defaults)
  - explicit `SchedulingPolicyClass` for predictable scheduler behavior
- Prefer ISM/HISM style output for large counts; avoid spawning heavyweight actors for each small part.
- Keep runtime generation bounds explicit to avoid uncontrolled world-wide regeneration.
- Avoid hidden dependency on editor-only data when runtime generation is expected.
- Treat World Partition boundaries as hard constraints for runtime scopes.

# Failure Handling
- Symptom: no buildings spawn.
  - Locate: Input stage output count, source bounds, lot tags.
  - Fix: verify source actor/spline ingestion and lot filter tags; confirm non-empty candidate set.
- Symptom: output exists in editor preview but not runtime.
  - Locate: `GenerationTrigger` and runtime radii/scheduling settings.
  - Fix: set `GenerateAtRuntime`, radii override, and valid scheduling policy.
- Symptom: runtime update regenerates too wide an area.
  - Locate: runtime radii and generation source movement.
  - Fix: reduce generation/cleanup radii and tighten source bounds.
- Symptom: stale generated pieces remain after rules shrink.
  - Locate: cleanup path and local component lifecycle.
  - Fix: trigger cleanup with remove-components behavior and force local cleanup when needed.
- Symptom: heavy hitching during runtime generation.
  - Locate: points-per-cell, actor spawn count, per-update workload.
  - Fix: reduce per-cell complexity, cap actor spawns, move non-interactive parts to static mesh instances.
- Symptom: deterministic replay mismatch with same seed.
  - Locate: unstable upstream point ordering or non-seeded random branch.
  - Fix: normalize ordering before random selection and bind every stochastic path to explicit seed inputs.
- Symptom: facade grammar fails or produces empty modules.
  - Locate: grammar parse logs and module token mapping.
  - Fix: validate grammar string, module dictionary, and segment size constraints.
- Symptom: overlap and collision issues.
  - Locate: filter thresholds and final placement constraints.
  - Fix: add clearance/slope filters and occupancy rejection before output stage.
- Symptom: navmesh degradation around generated buildings.
  - Locate: collision profile and nav-affecting flags on spawned outputs.
  - Fix: split nav-affecting vs non-nav-affecting outputs and rebuild nav only where required.
- Symptom: runtime changes do not apply after parameter edits.
  - Locate: scheduler refresh flow.
  - Fix: request runtime scheduler refresh for the modified component or all runtime components.

# Runtime Scheduler Ops
- Use component refresh when one runtime component changed style/radii/scheduling inputs.
- Use global refresh when style/global rules changed for many runtime components.
- Use immediate local cleanup when bounds shrink or partition ownership changed.
- After cleanup, trigger local regeneration only for affected runtime scope.

# UE5.6 / UE5.7 Compatibility Notes
- Core runtime trigger and grammar APIs above are stable in UE5.6 and UE5.7.
- Header path difference for subsystem:
  - UE5.6 commonly uses `Public/PCGSubsystem.h`
  - UE5.7 commonly uses `Public/Subsystems/PCGSubsystem.h`

# Escalation
- Escalate when architecture requires custom C++ PCG elements or engine plugin extension.
- Escalate when city-scale generation must be integrated with World Partition streaming policy.
- Escalate when generated layout must be synchronized with save/load or multiplayer authority rules.
