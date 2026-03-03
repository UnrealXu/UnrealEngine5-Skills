---
name: ue5-performance-packaging
description: UE5.6/UE5.7 performance and packaging readiness workflow. Use when requests involve PIE performance checks, runtime stat review, pre-package validation, build configuration sanity, and release readiness checklists.
---

# Quick Start
- Confirm target platform and build configuration.
- Collect current performance symptoms and packaging goal.
- Output a pre-package checklist plus measurement plan.

# UE5.7 API Anchors
- Runtime quality and frame-budget anchors:
  - `UGameUserSettings::SetOverallScalabilityLevel(...)`
  - `UGameUserSettings::SetFrameRateLimit(...)`
  - `UGameUserSettings::ApplySettings(...)`
- Packaging settings anchors:
  - `UProjectPackagingSettings`
  - `BuildConfiguration`, `MapsToCook`, `DirectoriesToAlwaysCook`
  - `UsePakFile`, `bUseIoStore`, `bGenerateChunks`
- Asset dependency validation anchors:
  - `FAssetRegistryModule`, `IAssetRegistry`
  - `GetAssetsByPath(...)`
  - `GetDependencies(...)`, `GetReferencers(...)`
- Profiling instrumentation anchors:
  - `TRACE_CPUPROFILER_EVENT_SCOPE(...)`
  - `DECLARE_CYCLE_STAT(...)`
- Practical runtime stat commands:
  - `stat unit`, `stat gpu`, `stat scenerendering`, `memreport -full`

# Performance and Packaging Contract
- Every performance/packaging task must define:
  - target platform + build config + test map
  - reproducible capture scenario (camera path, duration, net mode)
  - baseline metrics and acceptance thresholds
  - packaging configuration set and dependency scan scope
  - go/no-go output with explicit blockers
- If any item is missing, readiness evaluation is incomplete.

# Workflow
## 1) Reproducible Baseline Capture
- Freeze test map, camera path, scalability, and net mode.
- Capture `stat unit` and `stat gpu` under same scenario repeatedly.
- Use median or percentile metrics, not single-frame spikes.

## 2) Hotspot Isolation
- Identify top-cost gameplay/render systems in the capture window.
- Correlate high-cost actors/assets with scene context.
- Add scoped CPU markers for custom systems when attribution is unclear.

## 3) Asset and Dependency Validation
- Scan target paths for missing or broken asset references.
- Query dependencies and referencers for problematic assets.
- Validate required map/game mode assets are included in package scope.

## 4) Packaging Configuration Validation
- Check `UProjectPackagingSettings` fields for target release policy.
- Validate maps-to-cook, always-cook directories, and build configuration.
- Validate Pak/IoStore/chunk strategy against distribution requirements.

## 5) Package Readiness Trial
- Run pre-package checklist and dry-run style verification.
- Isolate first blocking packaging error and dependency chain.
- Record unresolved blockers with owner and risk.

## 6) Go/No-Go Decision
- Approve only when metrics and packaging checks meet thresholds.
- Report remaining risks and recommended mitigation actions.
- Lock scenario and settings used for sign-off evidence.

# Constraints
- Do not claim optimization wins without measurable before/after data.
- Keep profiling scenario reproducible (map, camera path, net mode).
- Distinguish editor overhead from packaged runtime behavior.
- Avoid changing quality scalability settings without reporting it.
- Keep packaging checks deterministic; avoid ad-hoc config toggles during sign-off.
- Always report metric units (ms, fps, memory) and capture duration.

# Failure Handling
- Symptom: performance data is noisy across runs.
  - Locate: non-deterministic scenario setup and background variance.
  - Fix: lock scenario, warm up run, and compare median/percentile values.
- Symptom: optimization claims do not reproduce.
  - Locate: mismatched quality settings, map, or runtime mode.
  - Fix: publish exact capture config and rerun before/after under same conditions.
- Symptom: package build fails with long error cascade.
  - Locate: first blocking error and its direct dependency chain.
  - Fix: resolve earliest blocker first; rerun to reveal next blockers.
- Symptom: packaged build launches with missing assets.
  - Locate: cook list coverage and dependency graph gaps.
  - Fix: include missing maps/directories and resolve broken references.
- Symptom: packaged build perf is worse than PIE baseline.
  - Locate: packaged-only config differences and runtime content path.
  - Fix: compare packaged config to baseline and align scalability/device settings.
- Symptom: memory usage regresses near content-heavy scenes.
  - Locate: high-memory assets and streaming policy behavior.
  - Fix: reduce resident asset pressure and adjust streaming/cook strategy.

# Packaging Ops
- Prefer explicit map/cook lists over implicit discovery for release builds.
- Use AssetRegistry queries to validate dependencies before packaging.
- Keep one source of truth for release packaging settings per target profile.
- Re-run readiness checks after any packaging setting change.

# UE5.6 / UE5.7 Compatibility Notes
- `UGameUserSettings`, `UProjectPackagingSettings`, and AssetRegistry APIs above are stable in UE5.6/UE5.7.
- `ProjectPackagingSettings.h` lives under `Developer/DeveloperToolSettings` in both versions.

# Escalation
- Escalate when performance bottleneck requires engine-level profiling or renderer changes.
- Escalate when packaging issues stem from third-party plugin build failures.
