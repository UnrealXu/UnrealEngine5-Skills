---
name: ue5-debug-validation
description: UE5.6/UE5.7 debugging and validation workflow for logs, asset checks, and regression triage. Use when requests involve troubleshooting why gameplay does not work, validating expected output, narrowing minimal repro, and producing concrete fix steps.
---

# Quick Start
- Reproduce issue with minimal steps.
- Collect output log lines and relevant actor/asset state.
- Classify fault domain: data, Blueprint, C++, networking, or editor config.

# Workflow
- Read and filter recent output logs by error/warning categories.
- Validate existence and configuration of critical assets/classes.
- Compare expected behavior vs observed behavior at each pipeline stage.
- Isolate smallest failing scenario and identify first bad transition.
- Provide fix list ordered by impact and confidence.

# Constraints
- Avoid broad refactors during diagnosis.
- Keep repro deterministic and documented.
- Prefer observable checks over assumptions.
- Separate root cause from secondary noise.

# Failure Handling
- If no repro is found, provide instrumentation additions and a new capture plan.
- If multiple candidates exist, rank by probability and verification cost.
- If issue spans systems, split into independent hypotheses and tests.

# Escalation
- Escalate when failure is inside engine/plugin internals not owned by project code.
- Escalate when diagnosis needs platform-specific profiling tools unavailable in current environment.
