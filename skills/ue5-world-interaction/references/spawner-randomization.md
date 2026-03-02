# Spawner Randomization

## Inputs
- Candidate item IDs
- Optional weight per item
- Spawn count, radius, and minimum spacing

## Algorithm
- Seed RNG explicitly when deterministic test runs are required.
- Pick item by weighted random.
- Sample spawn location and reject if blocked or too close to existing spawn.
- Spawn actor and assign payload data.

## Respawn Policy
- Full clear + regenerate.
- Incremental refill to target count.
- Manual hotkey-triggered rebuild in PIE.
