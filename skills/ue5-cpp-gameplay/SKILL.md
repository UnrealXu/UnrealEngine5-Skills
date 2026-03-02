---
name: ue5-cpp-gameplay
description: UE5.6/UE5.7 gameplay C++ implementation for Actors, Components, DataAssets, and gameplay logic. Use when requests ask to write .h/.cpp pairs, expose UPROPERTY/UFUNCTION to Blueprint, use GameplayTags, or build reusable component-based systems.
---

# Quick Start
- Confirm target class type (`AActor`, `UActorComponent`, `UObject`, `USaveGame`, etc.).
- Define required Blueprint-facing API before implementation.
- Output both header and source files together.

# Workflow
- Create type declarations with Unreal macros and UE5 pointer conventions (`TObjectPtr` in headers).
- Define Blueprint API (`BlueprintCallable`, `BlueprintPure`) and categories.
- Implement runtime logic in `.cpp` with explicit includes and safe guards.
- Add replication hooks/RPC stubs when multiplayer behavior is requested.
- Add `GameplayTag` usage only with explicit tag names and fallback checks.

# Constraints
- Always provide matching `.h` and `.cpp` when creating a class.
- Use non-deprecated APIs compatible with UE5.6/UE5.7.
- Keep includes minimal; use forward declarations in headers.
- Avoid hardcoded asset paths unless explicitly requested.

# Failure Handling
- If API usage differs by minor engine patch, use the stable UE5.6/UE5.7-compatible call and document fallback.
- If a Blueprint exposure request is ambiguous, expose minimal callable surface and mark extension points.
- If ownership or authority is unclear in networked logic, default to server-authoritative flow.

# Escalation
- Escalate when user asks for plugin/module-level refactor beyond a single gameplay class.
- Escalate when solution needs custom engine source modifications.
