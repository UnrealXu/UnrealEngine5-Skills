---
name: ue5-debug-validation
description: UE5.6/UE5.7 debugging and validation workflow for logs, asset checks, and regression triage. Use when requests involve troubleshooting why gameplay does not work, validating expected output, narrowing minimal repro, and producing concrete fix steps.
---

# Quick Start
- Reproduce issue with minimal steps.
- Collect output log lines and relevant actor/asset state.
- Classify fault domain: data, Blueprint, C++, networking, or editor config.

# UE5.7 API Anchors
- Core diagnostics anchors:
  - `UE_LOG(...)`
  - `ensure(...)`, `ensureMsgf(...)`
  - `check(...)`, `checkf(...)`
- Runtime debug output anchors:
  - `UEngine::AddOnScreenDebugMessage(...)`
  - `UKismetSystemLibrary::PrintString(...)`
- Structured log review anchors:
  - `FMessageLog::Info(...)`
  - `FMessageLog::Warning(...)`
  - `FMessageLog::Error(...)`
- Asset/config verification anchors:
  - `FAssetRegistryModule`, `IAssetRegistry`
  - `GetAssetsByPath(...)`
  - `GetDependencies(...)`, `GetReferencers(...)`

# Debug Stage Contract
- Every debug task must define:
  - reproducible scenario and expected vs observed behavior
  - data capture set (logs, runtime state, asset/config snapshot)
  - first bad transition candidate in the execution pipeline
  - hypothesis list ranked by probability and verification cost
  - fix validation and regression scope
- If any item is missing, diagnosis output is incomplete.

# Workflow
## 1) Reproduce and Freeze Context
- Build a minimal deterministic repro with exact steps and preconditions.
- Capture map, actor setup, input sequence, and runtime mode.
- Define expected result and observed deviation.

## 2) Capture Signals
- Filter logs by relevant categories and timestamps around failure window.
- Add targeted debug markers (`UE_LOG`, on-screen debug, or Blueprint print) if needed.
- Capture relevant state snapshots at stage boundaries.

## 3) Validate Data and Assets
- Verify key assets/classes/config entries exist and resolve correctly.
- Check dependencies/referencers for missing or mismatched assets.
- Confirm runtime-loaded data matches expected environment.

## 4) Locate First Bad Transition
- Walk pipeline step-by-step and identify earliest divergence point.
- Separate root cause from downstream noise symptoms.
- Prioritize smallest fixable cause with highest confidence.

## 5) Hypothesis and Verification
- Rank hypotheses by probability and verification cost.
- Run one focused test per hypothesis to avoid cross-contamination.
- Keep rejected hypotheses documented with evidence.

## 6) Fix and Regression Validation
- Apply minimal fix and rerun the same repro scenario.
- Validate no regression on adjacent systems/paths.
- Output fix summary with confidence and residual risk.

# Constraints
- Avoid broad refactors during diagnosis.
- Keep repro deterministic and documented.
- Prefer observable checks over assumptions.
- Separate root cause from secondary noise.
- Do not mix instrumentation changes with functional fixes in one step.
- Preserve failing evidence before introducing mitigation changes.

# Failure Handling
- Symptom: cannot reproduce issue consistently.
  - Locate: missing preconditions, race windows, or nondeterministic setup.
  - Fix: tighten repro setup and add targeted instrumentation checkpoints.
- Symptom: logs contain too much unrelated noise.
  - Locate: broad log categories and missing temporal scoping.
  - Fix: narrow category filters and focus around failure timestamps.
- Symptom: multiple plausible causes remain.
  - Locate: shared downstream symptom without first-failure isolation.
  - Fix: split into independent hypotheses and run low-cost discriminating tests.
- Symptom: issue disappears after adding debug output.
  - Locate: timing-sensitive/race-sensitive behavior.
  - Fix: use low-overhead markers and repeat with controlled timing.
- Symptom: fix resolves one path but breaks another.
  - Locate: hidden coupling between systems or config layers.
  - Fix: keep fix minimal and extend regression matrix around impacted paths.
- Symptom: runtime mismatch only happens on packaged builds.
  - Locate: build config/cook differences versus editor run.
  - Fix: compare packaged and editor config/assets and validate load order.

# Validation Ops
- Always keep a minimal repro artifact (steps, map, config) with the diagnosis.
- Always include first-failure evidence, not only final symptom logs.
- Always provide a verification checklist for the proposed fix.
- Always state residual risk when confidence is below high.

# UE5.6 / UE5.7 Compatibility Notes
- Logging/assertion/message/asset-registry APIs listed above are stable across UE5.6/UE5.7.
- Prefer runtime-safe diagnostics for validation paths that must run outside editor.

# Escalation
- Escalate when failure is inside engine/plugin internals not owned by project code.
- Escalate when diagnosis needs platform-specific profiling tools unavailable in current environment.
