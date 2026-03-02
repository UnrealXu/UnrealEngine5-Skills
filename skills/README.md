# UE5 Skills README

A Codex skill set for Unreal Engine projects targeting UE5.6 and UE5.7.
It routes user requests to focused workflows for Blueprint, C++, UI, networking, save/load, debugging, performance, and architecture.

## Scope

- Engine versions: UE5.6 and UE5.7
- Runtime: Codex CLI + Unreal project workspace
- Goal: deterministic routing and reusable task workflows

## Skills

- `ue5-auto-assistant`: natural-language entry and auto-routing
- `ue5-module-router`: module-name and alias based routing
- `ue5-architecture`: module boundaries, Build.cs, ownership
- `ue5-blueprint-workflow`: Blueprint graph implementation workflow
- `ue5-cpp-gameplay`: gameplay C++ implementation workflow
- `ue5-debug-validation`: issue triage and validation workflow
- `ue5-performance-packaging`: performance and packaging checks
- `ue5-save-load-replication`: save/load and multiplayer sync
- `ue5-ui-umg-slate`: UMG/Slate UI workflow
- `ue5-world-interaction`: pickups, spawners, traces, overlap logic

## Key Routing Data

- `skills/ue5-architecture/references/ue5-engine-module-index-v2.csv`
- `skills/ue5-architecture/references/ue5-module-routing-table-final.csv`

## Quick Usage

Use normal language or call a skill directly:

- `Use ue5-auto-assistant to design an inventory feature`
- `Use ue5-module-router for AssetRegistry troubleshooting`
- `Use ue5-architecture to split Runtime and Editor modules`

Recommended flow:

1. `ue5-auto-assistant`
2. `ue5-module-router` (when module names are present)
3. target skill (for example `ue5-cpp-gameplay`)

## Rebuild Routing Index

Auto-detect engine source:

- Priority 1: `UE_ENGINE_SOURCE` / `UE_ENGINE_ROOT` environment variables
- Priority 2: common install paths (prefers UE_5.7, fallback UE_5.6)

```powershell
python .\skills\ue5-architecture\scripts\generate_module_index_v2.py
```

Explicit engine source:

```powershell
python .\skills\ue5-architecture\scripts\generate_module_index_v2.py --engine-source "E:\UEVersion\UE_5.7\Engine\Source"
```

Prefer a specific version:

```powershell
python .\skills\ue5-architecture\scripts\generate_module_index_v2.py --engine-version 5.6
```

Outputs:

- `ue5-engine-module-index-v2.csv`
- `ue5-engine-module-index-v2.md`
- `ue5-module-routing-table-final.csv`

## Sync To Global Codex Skills

```powershell
robocopy .\skills "$env:USERPROFILE\.codex\skills" /MIR
```

## Release Validation

Run the pack validator before publishing:

```powershell
python .\skills\scripts\validate_skills.py
```

Expected output:

- `Validation OK`
- no `ue56-` / `ue57x-` legacy tokens
- all `SKILL.md` files have valid frontmatter and no BOM

## Publish Checklist

1. Regenerate routing index CSV/MD.
2. Run `validate_skills.py`.
3. Verify one active source of truth:
   - project-local `.codex/skills`, or
   - user-global `%USERPROFILE%\.codex\skills`.
4. Restart Codex/IDE settings page and confirm only `ue5-*` skills are loaded.
5. Commit `skills/` with updated references and docs.

## Distribution Tips

- For GitHub release: publish the `skills/` folder directly.
- Avoid committing machine-specific paths or local user IDs in docs/scripts.
- Keep `agents/openai.yaml` aligned with each `SKILL.md`.
```

## Troubleshooting

- `missing YAML frontmatter delimited by ---`
  - Ensure `SKILL.md` starts with `---`
  - Remove UTF-8 BOM from `SKILL.md`
- unstable routing results
  - regenerate routing index
  - confirm `ue5-module-routing-table-final.csv` is up to date
  - include explicit module names when possible

## Maintenance

- regenerate index after engine updates
- keep `ue5-auto-assistant` and `ue5-module-router` routing docs aligned
- update this README when adding/removing skills
