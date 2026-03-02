# Pickup Actor Pattern

## Components
- Root scene component
- Collision sphere/capsule for interaction
- Visual component (static mesh/skeletal mesh/VFX)

## Interaction Flow
- Detect candidate interactor.
- Validate authority and eligibility.
- Attempt inventory/state mutation.
- Broadcast success/failure events.
- Apply lifecycle policy (destroy or persist).

## Optional UX
- Outline/custom depth on hover.
- Floating text or toast feedback.
