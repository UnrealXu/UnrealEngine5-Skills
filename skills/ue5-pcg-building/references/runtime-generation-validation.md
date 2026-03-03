# Runtime Generation Validation

## Functional Checks
- Verify generation source moves correctly and updates target bounds.
- Verify graph regenerates only required cells or regions.
- Verify seed and style settings produce reproducible output.

## Performance Checks
- Measure generation spikes in PIE and standalone.
- Confirm high-count outputs use instance-based rendering.
- Limit per-update spawned element count to avoid frame hitches.

## World Integration Checks
- Validate navigation behavior for generated collision.
- Validate streaming boundaries with World Partition.
- Validate interaction actors are spawned only where needed.

## Safety Checks
- Ensure runtime path does not call editor-only logic.
- Ensure cleanup path removes stale generated instances.
- Ensure save/load or network authority rules are explicit.

## Minimal Runnable Runtime Template
- Component setup:
  - `GenerationTrigger = GenerateAtRuntime`
  - `bOverrideGenerationRadii = true`
  - explicit `GenerationRadii` set for generate/cleanup behavior
  - explicit `SchedulingPolicyClass` selection
- Runtime control flow:
  - update source bounds -> refresh runtime component scheduling -> generate affected cells only
  - when bounds or rules shrink -> cleanup stale local components -> regenerate affected region
- API anchors for C++/tooling integration:
  - `UPCGComponent::GenerateLocal(...)`
  - `UPCGComponent::Cleanup(...)`
  - `UPCGSubsystem::RefreshRuntimeGenComponent(...)`
  - `UPCGSubsystem::RefreshAllRuntimeGenComponents(...)`
  - `UPCGSubsystem::CleanupLocalComponentsImmediate(...)`

## Performance Threshold Suggestions
- Treat these as baseline targets for regression checks:
  - Runtime refresh-to-visible-output latency: p95 <= 150 ms
  - Runtime generation frame hitch: no single frame > 8 ms caused by PCG update
  - Partition/cell regeneration scope: changed cells only (no full-map re-run)
  - Per-update interactive actor spawns: <= 50
  - Per-update static mesh instance creations: <= 2000
- If thresholds are exceeded:
  - reduce active generation radii;
  - simplify per-cell graph branch depth;
  - split expensive grammar/output branches into deferred passes.

## Validation Scenarios
- Scenario 1: fixed-seed replay.
  - Action: run generation twice with same inputs/seed.
  - Pass: output transforms/modules match.
- Scenario 2: source movement locality.
  - Action: move generation source by one cell.
  - Pass: only overlapping cells regenerate.
- Scenario 3: radius shrink cleanup.
  - Action: reduce generation/cleanup radii.
  - Pass: out-of-scope generated results are removed.
- Scenario 4: output strategy swap.
  - Action: switch a subgraph from Spawn Actor to Static Mesh Spawner.
  - Pass: hitch decreases and functional state remains correct for non-interactive parts.
- Scenario 5: grammar swap.
  - Action: change `GrammarKey` or grammar string for one district.
  - Pass: only target district modules change; other districts remain stable.
