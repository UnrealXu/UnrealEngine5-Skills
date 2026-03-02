#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = SKILL_DIR / "references"


@dataclass(frozen=True)
class DomainRule:
    name: str
    any_tokens: set[str]


DOMAIN_RULES: list[DomainRule] = [
    DomainRule("CoreEngine", {"core", "coreuobject", "engine", "projects", "applicationcore"}),
    DomainRule("Rendering", {"render", "renderer", "rhi", "shader", "material", "nanite", "lumen", "raytracing"}),
    DomainRule("Animation", {"animation", "anim", "skeletal", "rig", "controlrig", "pose"}),
    DomainRule("Audio", {"audio", "sound", "metasound", "voice", "synth"}),
    DomainRule("Physics", {"physics", "chaos", "collision", "cloth", "destruction"}),
    DomainRule("AI_Mass", {"ai", "navigation", "nav", "behavior", "perception", "mass"}),
    DomainRule("NetworkingOnline", {"network", "net", "replication", "online", "socket", "http", "websocket"}),
    DomainRule("UI", {"ui", "umg", "slate", "widget", "commonui", "appframework"}),
    DomainRule("GameplayFramework", {"gameplay", "ability", "gamefeatures", "modular", "input", "enhancedinput"}),
    DomainRule("AssetsBuildPipeline", {"asset", "cook", "package", "registry", "serialization", "save", "uht", "ubt"}),
    DomainRule("Media", {"media", "movie", "video", "electra", "imgmedia"}),
    DomainRule("XR", {"xr", "vr", "ar", "openxr", "headmounted", "hmd", "steamvr"}),
    DomainRule("VFX", {"niagara", "vfx", "fx"}),
]


DOMAIN_SEED_KEYWORDS: dict[str, list[str]] = {
    "CoreEngine": ["core", "engine", "uobject"],
    "Rendering": ["render", "shader", "rhi"],
    "Animation": ["animation", "skeletal", "rig"],
    "Audio": ["audio", "sound", "metasound"],
    "Physics": ["physics", "chaos", "collision"],
    "AI_Mass": ["ai", "nav", "mass"],
    "NetworkingOnline": ["network", "online", "replication"],
    "UI": ["ui", "umg", "slate"],
    "GameplayFramework": ["gameplay", "ability", "input"],
    "AssetsBuildPipeline": ["asset", "cook", "package"],
    "Media": ["media", "movie", "video"],
    "XR": ["xr", "vr", "ar"],
    "VFX": ["niagara", "vfx", "fx"],
    "General": ["unreal", "module"],
}


SKILL_ROUTING_BY_DOMAIN: dict[str, str] = {
    "CoreEngine": "ue5-architecture",
    "Rendering": "ue5-performance-packaging",
    "Animation": "ue5-cpp-gameplay",
    "Audio": "ue5-cpp-gameplay",
    "Physics": "ue5-world-interaction",
    "AI_Mass": "ue5-cpp-gameplay",
    "NetworkingOnline": "ue5-save-load-replication",
    "UI": "ue5-ui-umg-slate",
    "GameplayFramework": "ue5-cpp-gameplay",
    "AssetsBuildPipeline": "ue5-performance-packaging",
    "Media": "ue5-cpp-gameplay",
    "XR": "ue5-cpp-gameplay",
    "VFX": "ue5-world-interaction",
    "General": "ue5-architecture",
}

MODULE_DOMAIN_OVERRIDES: dict[str, str] = {
    "Core": "CoreEngine",
    "CoreUObject": "CoreEngine",
    "Engine": "CoreEngine",
    "RenderCore": "Rendering",
    "Renderer": "Rendering",
    "RHI": "Rendering",
    "Slate": "UI",
    "UMG": "UI",
    "AIModule": "AI_Mass",
    "NavigationSystem": "AI_Mass",
    "GameplayAbilities": "GameplayFramework",
    "GameplayTags": "GameplayFramework",
    "GameplayTasks": "GameplayFramework",
    "OnlineSubsystem": "NetworkingOnline",
    "OnlineSubsystemUtils": "NetworkingOnline",
    "AssetRegistry": "AssetsBuildPipeline",
    "Niagara": "VFX",
    "Chaos": "Physics",
    "CommonUI": "UI",
    "EnhancedInput": "GameplayFramework",
    "InputCore": "GameplayFramework",
    "RenderCore": "Rendering",
    "RendererCore": "Rendering",
    "Landscape": "Rendering",
    "MovieScene": "Media",
    "MediaAssets": "Media",
    "MediaUtils": "Media",
    "WebSockets": "NetworkingOnline",
    "HTTP": "NetworkingOnline",
    "PacketHandler": "NetworkingOnline",
    "ReplicationGraph": "NetworkingOnline",
    "NetCore": "NetworkingOnline",
    "UMGEditor": "UI",
    "SlateCore": "UI",
    "AnimGraphRuntime": "Animation",
    "AnimationCore": "Animation",
    "ControlRig": "Animation",
    "PhysicsCore": "Physics",
}

MODULE_SKILL_OVERRIDES: dict[str, str] = {
    "Core": "ue5-architecture",
    "CoreUObject": "ue5-architecture",
    "Engine": "ue5-architecture",
    "Projects": "ue5-architecture",
    "RenderCore": "ue5-performance-packaging",
    "Renderer": "ue5-performance-packaging",
    "RHI": "ue5-performance-packaging",
    "ShaderCore": "ue5-performance-packaging",
    "MaterialShaderQualitySettings": "ue5-performance-packaging",
    "AssetRegistry": "ue5-performance-packaging",
    "AssetTools": "ue5-performance-packaging",
    "PakFile": "ue5-performance-packaging",
    "CookOnTheFly": "ue5-performance-packaging",
    "CookOnTheFlyNetServer": "ue5-performance-packaging",
    "Niagara": "ue5-world-interaction",
    "Chaos": "ue5-world-interaction",
    "PhysicsCore": "ue5-world-interaction",
    "AIModule": "ue5-cpp-gameplay",
    "NavigationSystem": "ue5-cpp-gameplay",
    "GameplayAbilities": "ue5-cpp-gameplay",
    "GameplayTags": "ue5-cpp-gameplay",
    "GameplayTasks": "ue5-cpp-gameplay",
    "EnhancedInput": "ue5-cpp-gameplay",
    "AnimGraphRuntime": "ue5-cpp-gameplay",
    "ControlRig": "ue5-cpp-gameplay",
    "Slate": "ue5-ui-umg-slate",
    "SlateCore": "ue5-ui-umg-slate",
    "UMG": "ue5-ui-umg-slate",
    "CommonUI": "ue5-ui-umg-slate",
    "OnlineSubsystem": "ue5-save-load-replication",
    "OnlineSubsystemUtils": "ue5-save-load-replication",
    "NetCore": "ue5-save-load-replication",
    "ReplicationGraph": "ue5-save-load-replication",
    "PacketHandler": "ue5-save-load-replication",
    "HTTP": "ue5-save-load-replication",
    "WebSockets": "ue5-save-load-replication",
}


EXCLUDE_TOKENS = {
    "build",
    "runtime",
    "developer",
    "editor",
    "thirdparty",
    "programs",
    "module",
    "source",
    "engine",
    "cs",
}


def split_tokens(value: str) -> list[str]:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    parts = re.split(r"[^A-Za-z0-9]+", value)
    return [p.lower() for p in parts if p]


def classify_domain(module_name: str, rel_path: str, layer: str) -> str:
    if module_name in MODULE_DOMAIN_OVERRIDES:
        return MODULE_DOMAIN_OVERRIDES[module_name]

    tokens = set(split_tokens(module_name))
    tokens.update(split_tokens(rel_path))

    if layer == "ThirdParty":
        lower_blob = f"{module_name} {rel_path}".lower()
        render_tokens = {
            "directx", "dx11", "dx12", "dx9", "d3d12", "vulkan", "opengl", "opengles", "glslang",
            "spirv", "shaderconductor", "nvapi", "amd", "ags", "cuda", "directml", "embree",
        }
        audio_tokens = {"audio", "ogg", "opus", "vorbis", "xaudio2", "directsound", "wasapi", "wwise", "fmod"}
        net_tokens = {"asio", "openssl", "curl", "websocket", "websockets", "eossdk", "steam", "http"}
        media_tokens = {"ffmpeg", "video", "media", "webm", "dnxhr", "dnxmxf", "dnxuncompressed", "bink"}
        xr_tokens = {"openxr", "openvr", "oculus", "arcore", "vr", "xr", "hmd"}
        ui_tokens = {"cef3", "cef", "freetype", "harfbuzz", "icu"}
        build_tokens = {
            "zlib", "zstd", "lz4", "oodle", "ispc", "protobuf", "protobuf3", "fbx", "alembic",
            "openexr", "dr", "dr_libs", "blake3", "zip", "expat", "boost", "eigen", "astcenc", "etc2comp",
        }

        if tokens.intersection(render_tokens) or any(k in lower_blob for k in ("directx", "directml", "d3d12", "dx11", "dx12", "vulkan", "opengl")):
            return "Rendering"
        if tokens.intersection(audio_tokens) or any(k in lower_blob for k in ("directsound", "xaudio", "wasapi", "ogg", "opus", "vorbis")):
            return "Audio"
        if tokens.intersection(net_tokens) or any(k in lower_blob for k in ("websocket", "openssl", "curl", "eossdk", "steam")):
            return "NetworkingOnline"
        if tokens.intersection(media_tokens) or any(k in lower_blob for k in ("dnxhr", "dnxmxf", "dnxuncompressed", "bink", "webm", "video")):
            return "Media"
        if tokens.intersection(xr_tokens) or any(k in lower_blob for k in ("openxr", "openvr", "oculus", "arcore", "googlearcore")):
            return "XR"
        if tokens.intersection(ui_tokens) or any(k in lower_blob for k in ("cef3", "freetype", "harfbuzz", "icu")):
            return "UI"
        if tokens.intersection(build_tokens) or any(k in lower_blob for k in ("alembic", "fbx", "openexr", "zlib", "zstd", "lz4", "oodle", "protobuf", "dr_libs")):
            return "AssetsBuildPipeline"
        return "General"

    if layer == "Programs":
        return "AssetsBuildPipeline"

    for rule in DOMAIN_RULES:
        if tokens.intersection(rule.any_tokens):
            return rule.name
    return "General"


def top_keywords(module_name: str, rel_path: str, domain: str) -> str:
    freq: Counter[str] = Counter()
    for tok in split_tokens(module_name) + split_tokens(rel_path):
        if len(tok) < 3 or tok in EXCLUDE_TOKENS:
            continue
        freq[tok] += 1

    seed = DOMAIN_SEED_KEYWORDS.get(domain, DOMAIN_SEED_KEYWORDS["General"])
    ordered = list(seed)
    ordered.extend([k for k, _ in freq.most_common(12) if k not in ordered])
    return "|".join(ordered[:8])

def pick_target_skill(module_name: str, domain: str) -> tuple[str, str]:
    if module_name in MODULE_SKILL_OVERRIDES:
        return MODULE_SKILL_OVERRIDES[module_name], "module_override"
    return SKILL_ROUTING_BY_DOMAIN.get(domain, "ue5-architecture"), "domain_mapping"

def secondary_skill_for(primary_skill: str, domain: str) -> str:
    if primary_skill == "ue5-cpp-gameplay":
        if domain in {"UI"}:
            return "ue5-ui-umg-slate"
        if domain in {"NetworkingOnline"}:
            return "ue5-save-load-replication"
        return "ue5-architecture"
    if primary_skill == "ue5-ui-umg-slate":
        return "ue5-cpp-gameplay"
    if primary_skill == "ue5-save-load-replication":
        return "ue5-cpp-gameplay"
    if primary_skill == "ue5-world-interaction":
        return "ue5-cpp-gameplay"
    if primary_skill == "ue5-performance-packaging":
        return "ue5-architecture"
    return "ue5-cpp-gameplay"

def route_confidence(route_reason: str, layer: str, domain: str) -> str:
    if route_reason == "module_override":
        return "high"
    if domain != "General":
        return "medium"
    if layer in {"Runtime", "Editor", "Developer"}:
        return "medium"
    return "low"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate UE module index and skill routing table.")
    parser.add_argument(
        "--engine-source",
        type=Path,
        default=None,
        help="Path to Engine/Source. If omitted, auto-detect UE_5.7 then UE_5.6.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=OUT_DIR,
        help="Output directory for CSV/MD artifacts.",
    )
    parser.add_argument(
        "--engine-version",
        type=str,
        default=None,
        help="Optional preferred engine version (for example: 5.7 or 5.6).",
    )
    return parser.parse_args(argv)


def normalize_engine_source(path_like: Path) -> Path:
    # Accept either the engine root (e.g. UE_5.7) or Engine/Source directly.
    p = path_like.expanduser()
    if p.name.lower() == "source" and p.parent.name.lower() == "engine":
        return p
    return p / "Engine" / "Source"


def default_engine_candidates(preferred_version: str | None) -> list[Path]:
    env_candidates: list[Path] = []
    env_engine = os.getenv("UE_ENGINE_SOURCE")
    env_root = os.getenv("UE_ENGINE_ROOT")
    if env_engine:
        env_candidates.append(Path(env_engine))
    if env_root:
        env_candidates.append(normalize_engine_source(Path(env_root)))

    root_candidates = [
        Path(r"E:\UEVersion"),
        Path(r"D:\UEVersion"),
        Path(r"C:\UEVersion"),
        Path(r"C:\Program Files\Epic Games"),
    ]
    version_tokens = ["5.7", "5.6"]
    if preferred_version in {"5.6", "5.7"}:
        version_tokens = [preferred_version] + [v for v in version_tokens if v != preferred_version]

    engine_candidates: list[Path] = []
    for root in root_candidates:
        for version in version_tokens:
            engine_candidates.append(root / f"UE_{version}" / "Engine" / "Source")
            engine_candidates.append(root / f"UnrealEngine-{version}" / "Engine" / "Source")
    return env_candidates + engine_candidates


def resolve_engine_source(override: Path | None, preferred_version: str | None) -> Path:
    if override is not None:
        return normalize_engine_source(override)
    for candidate in default_engine_candidates(preferred_version):
        if candidate.exists():
            return candidate
    searched = ", ".join(str(p) for p in default_engine_candidates(preferred_version))
    raise SystemExit(f"Engine source not found. Checked: {searched}")


def detect_engine_version(engine_source: Path) -> str:
    joined = str(engine_source)
    m = re.search(r"UE_(\d+\.\d+)", joined, flags=re.IGNORECASE)
    if m:
        return m.group(1)
    m = re.search(r"UnrealEngine-(\d+\.\d+)", joined, flags=re.IGNORECASE)
    if m:
        return m.group(1)
    return "Unknown"


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    engine_source = resolve_engine_source(args.engine_source, args.engine_version)
    out_dir = args.out_dir
    engine_version = detect_engine_version(engine_source)

    if not engine_source.exists():
        raise SystemExit(f"Engine source not found: {engine_source}")
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for f in engine_source.rglob("*.Build.cs"):
        rel = str(f.relative_to(engine_source)).replace("/", "\\")
        module_name = re.sub(r"\.build\.cs$", "", f.name, flags=re.IGNORECASE)
        layer = rel.split("\\", 1)[0]
        domain = classify_domain(module_name, rel, layer)
        keywords = top_keywords(module_name, rel, domain)
        target_skill, route_reason = pick_target_skill(module_name, domain)
        secondary_skill = secondary_skill_for(target_skill, domain)
        confidence = route_confidence(route_reason, layer, domain)
        rows.append(
            {
                "ModuleName": module_name,
                "Layer": layer,
                "DomainGuessV2": domain,
                "RelativeBuildCsPath": rel,
                "TriggerKeywords": keywords,
                "TargetSkill": target_skill,
                "SecondarySkill": secondary_skill,
                "RouteConfidence": confidence,
                "RouteReason": route_reason,
            }
        )

    rows.sort(key=lambda r: (r["Layer"], r["ModuleName"].lower()))

    csv_index = out_dir / "ue5-engine-module-index-v2.csv"
    with csv_index.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "ModuleName",
                "Layer",
                "DomainGuessV2",
                "RelativeBuildCsPath",
                "TriggerKeywords",
                "TargetSkill",
                "SecondarySkill",
                "RouteConfidence",
                "RouteReason",
            ],
        )
        w.writeheader()
        w.writerows(rows)

    csv_route = out_dir / "ue5-module-routing-table-final.csv"
    with csv_route.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "ModuleName",
                "Layer",
                "TargetSkill",
                "SecondarySkill",
                "RouteConfidence",
                "RouteReason",
                "PrimaryAliases",
                "ExcludeTerms",
                "RelativeBuildCsPath",
            ],
        )
        w.writeheader()
        for r in rows:
            aliases = [r["ModuleName"].lower()]
            aliases.extend([k for k in r["TriggerKeywords"].split("|")[:3] if k])
            w.writerow(
                {
                    "ModuleName": r["ModuleName"],
                    "Layer": r["Layer"],
                    "TargetSkill": r["TargetSkill"],
                    "SecondarySkill": r["SecondarySkill"],
                    "RouteConfidence": r["RouteConfidence"],
                    "RouteReason": r["RouteReason"],
                    "PrimaryAliases": "|".join(dict.fromkeys(aliases)),
                    "ExcludeTerms": "email|translation|copywriting",
                    "RelativeBuildCsPath": r["RelativeBuildCsPath"],
                }
            )

    layer_stats = Counter(r["Layer"] for r in rows)
    domain_stats = Counter(r["DomainGuessV2"] for r in rows)
    skill_stats = Counter(r["TargetSkill"] for r in rows)
    confidence_stats = Counter(r["RouteConfidence"] for r in rows)

    md_index = out_dir / "ue5-engine-module-index-v2.md"
    lines: list[str] = []
    lines.append("# UE5.6/UE5.7 Engine Module Index V2.3 (Draft)")
    lines.append("")
    lines.append(f"- Engine Source: `{engine_source}`")
    lines.append(f"- Detected Engine Version: `{engine_version}`")
    lines.append(f"- Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Total Modules (.Build.cs): **{len(rows)}**")
    lines.append("- Full CSV: `skills/ue5-architecture/references/ue5-engine-module-index-v2.csv`")
    lines.append("- Final Routing CSV: `skills/ue5-architecture/references/ue5-module-routing-table-final.csv`")
    lines.append("")
    lines.append("## Layer Distribution")
    for k, v in sorted(layer_stats.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Domain V2 Distribution")
    for k, v in sorted(domain_stats.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Target Skill Distribution")
    for k, v in sorted(skill_stats.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Routing Confidence Distribution")
    for k, v in sorted(confidence_stats.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Sample (First 100)")
    lines.append("| Module | Layer | DomainV2 | TargetSkill | Confidence | Build.cs |")
    lines.append("|---|---|---|---|---|---|")
    for r in rows[:100]:
        lines.append(
            f"| {r['ModuleName']} | {r['Layer']} | {r['DomainGuessV2']} | {r['TargetSkill']} | {r['RouteConfidence']} | `{r['RelativeBuildCsPath']}` |"
        )
    md_index.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Generated: {csv_index}")
    print(f"Generated: {md_index}")
    print(f"Generated: {csv_route}")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
