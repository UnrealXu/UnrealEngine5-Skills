# Module Layout (UE5.6/UE5.7)

## Baseline
- `Source/ProjectName/` for runtime gameplay and shared systems.
- `Source/ProjectNameEditor/` for editor-only extensions.
- `Public/` exposes minimal API headers.
- `Private/` contains implementation and non-exported types.

## Suggested Layering
- Data contracts: enums/structs/data assets.
- Runtime systems: components, actors, subsystems.
- UI systems: UMG/Slate wrappers and widgets.
- Editor tooling: asset actions, customization, validation utilities.

## Rule
- Upper layer may depend on lower layer.
- Lower layer must not depend on upper layer.
- Editor modules never referenced from runtime modules.
