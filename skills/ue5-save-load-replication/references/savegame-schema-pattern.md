# SaveGame Schema Pattern

## Structure
- `F...SaveData` for per-system snapshots.
- Stable keys (`FName`, GUID, or explicit slot IDs) for map-based lookup.
- Version field for migration.

## Flow
- Runtime -> `BuildSaveData()`
- Save container -> `USaveGame` map/array
- Load -> schema validation -> `RestoreFromSaveData()`

## Safety
- Validate counts, IDs, and bounds before applying loaded data.
- Return operation result object with reason text for failures.
