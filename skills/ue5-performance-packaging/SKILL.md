---
name: ue5-performance-packaging
description: UE5.6/UE5.7 performance and packaging readiness workflow. Use when requests involve PIE performance checks, runtime stat review, pre-package validation, build configuration sanity, and release readiness checklists.
---

# Quick Start
- Confirm target platform and build configuration.
- Collect current performance symptoms and packaging goal.
- Output a pre-package checklist plus measurement plan.

# Workflow
- Run runtime performance checks (frame time, game/render/GPU timing).
- Identify heavyweight actors/assets and suspect systems.
- Validate asset references and required map/game mode settings.
- Verify build configuration and packaging options.
- Produce go/no-go checklist with unresolved blockers.

# Constraints
- Do not claim optimization wins without measurable before/after data.
- Keep profiling scenario reproducible (map, camera path, net mode).
- Distinguish editor overhead from packaged runtime behavior.
- Avoid changing quality scalability settings without reporting it.

# Failure Handling
- If metrics are noisy, run repeated captures and use median.
- If package fails, isolate first blocking error and dependency chain.
- If asset references break, list exact missing packages and owning assets.

# Escalation
- Escalate when performance bottleneck requires engine-level profiling or renderer changes.
- Escalate when packaging issues stem from third-party plugin build failures.
