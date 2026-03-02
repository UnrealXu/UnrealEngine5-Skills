# Prepackage Checklist (UE5.6/UE5.7)

## Project Settings
- Default map and game mode are correct.
- Target platforms and RHI options are intentional.
- Required plugins are enabled and compatible.

## Content Health
- No missing or invalid asset references.
- Redirectors fixed in content folders.
- Large assets reviewed for cook/package impact.

## Build Health
- Clean Development build succeeds.
- Shipping build config validates.
- Packaging log has no unresolved errors.

## Runtime Smoke Test
- Launch packaged build.
- Verify core gameplay loop, save/load, and UI navigation.
