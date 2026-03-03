# PCG Building Graph Patterns

## Pattern 1: Lot To Building Footprint
- Input lot points or splines.
- Filter invalid areas by slope, bounds, and exclusion tags.
- Derive footprint transforms for each accepted lot.

## Pattern 2: Vertical Stack
- Convert each footprint into floor-level points.
- Apply floor count rules by district tag or density tier.
- Offset transforms per floor height and pivot convention.

## Pattern 3: Facade Dressing
- Use side/corner classification from footprint edges.
- Sample facade modules by rule set and weighted randomness.
- Add conditional meshes (balcony, signage, trim) via tags.

## Pattern 4: Rooftop Pass
- Add rooftop modules only for top floor points.
- Validate clearance before large rooftop props.
- Keep rooftop spawn optional by style preset.

## Pattern 5: Output Selection
- Prefer Static Mesh Spawner with ISM/HISM for high counts.
- Use Spawn Actor only for interactive or stateful building parts.
- Keep output split by layer for easier debug and culling.

## Minimal Runnable Template Graph (UE5.7)
- Goal: build a deterministic lot-to-building graph that runs in editor and runtime.
- Stage chain:
  - Input: `UPCGDataFromActorSettings` -> `UPCGGetActorPropertySettings`
  - Filter: `UPCGFilterByTagSettings` -> `UPCGAttributeFilteringSettings`
  - Transform: `UPCGCopyPointsSettings` -> `UPCGApplyScaleToBoundsSettings`
  - Grammar: `UPCGSubdivideSplineSettings` -> `UPCGSelectGrammarSettings`
  - Output: `UPCGStaticMeshSpawnerSettings` (default), optional `UPCGSpawnActorSettings`
  - Validate: `UPCGDebugSettings`
- Minimal required attributes:
  - `LotId` (stable lot identity)
  - `DistrictTag` (style routing)
  - `Seed` (deterministic random)
  - `FloorCount` (vertical expansion)
  - `GrammarKey` (rule selection)
- Determinism rules:
  - Normalize point ordering before any random branch.
  - Use explicit seed attributes for all weighted or stochastic decisions.
  - Keep style and grammar keys immutable inside one generation pass.

## Performance Threshold Suggestions
- Treat these as starting budgets, not hard engine limits.
- Runtime update budget targets:
  - PCG generation time per update (game thread visible cost): p95 <= 4 ms
  - Actor spawns per update (interactive/stateful only): <= 50
  - Static mesh instance creations per update: <= 2000
  - Candidate points per active cell before output: <= 10000
- Escalate optimization if any target is exceeded for more than 5 consecutive updates.
- When over budget:
  - reduce candidate points before output stage;
  - move non-interactive outputs from actor spawn to static mesh instancing;
  - split heavy grammar branches into lower-frequency passes.

## UE5.6 / UE5.7 Note
- Patterns above are valid in both versions.
- Runtime scheduler include paths differ between versions; keep include usage version-aware in C++ helpers.
