# UE5 Skills README

[English](#english) | [中文](#中文)

## English

This folder contains Codex skills for Unreal Engine 5.6/5.7 projects.

### Skills Overview Screenshot

![UE5 Skills Overview](./assets/ue5-skills-overview.png)

> Screenshot of the Codex Skills panel showing the installed UE5 skill set and enabled status (captured on March 3, 2026).

### What Is Included

- Routing skills:
  - `ue5-auto-assistant`
  - `ue5-module-router`
- Domain skills:
  - `ue5-architecture`
  - `ue5-blueprint-workflow`
  - `ue5-cpp-gameplay`
  - `ue5-debug-validation`
  - `ue5-performance-packaging`
  - `ue5-save-load-replication`
  - `ue5-ui-umg-slate`
  - `ue5-world-interaction`
  - `ue5-pcg-building`

### UE5.7 Actionable Upgrade Status

Skills already upgraded to the UE5.7 actionable format:

- `ue5-pcg-building`
- `ue5-blueprint-workflow`
- `ue5-cpp-gameplay`
- `ue5-save-load-replication`
- `ue5-world-interaction`
- `ue5-ui-umg-slate`
- `ue5-performance-packaging`
- `ue5-debug-validation`

Each upgraded skill now contains:

- `UE5.7 API Anchors` (engine class/function/node anchors)
- stage contract section (decision-complete workflow contract)
- executable failure handling (`symptom -> locate -> fix`)
- explicit UE5.6/UE5.7 compatibility notes

### Key Routing Data

- `skills/ue5-architecture/references/ue5-engine-module-index-v2.csv`
- `skills/ue5-architecture/references/ue5-module-routing-table-final.csv`

### Quick Usage

Recommended flow:

1. Use `ue5-auto-assistant`
2. If module names are present, use `ue5-module-router`
3. Execute the routed target skill

Examples:

- `Use ue5-auto-assistant to design an inventory feature`
- `Use ue5-module-router for AssetRegistry troubleshooting`
- `Use ue5-cpp-gameplay to implement a replicated component`

### Validate Skill Pack

```powershell
python .\skills\scripts\validate_skills.py
```

Expected output: `Validation OK`

### Rebuild Routing Index (Architecture Skill)

Auto-detect engine source:

```powershell
python .\skills\ue5-architecture\scripts\generate_module_index_v2.py
```

Explicit engine source:

```powershell
python .\skills\ue5-architecture\scripts\generate_module_index_v2.py --engine-source "E:\UEVersion\UE_5.7\Engine\Source"
```

### Sync To Global Codex Skills

```powershell
robocopy .\skills "$env:USERPROFILE\.codex\skills" /MIR
```

### Publish Checklist

1. Regenerate routing index files if architecture references changed.
2. Run `validate_skills.py`.
3. Confirm `SKILL.md` frontmatter and references are valid.
4. Commit only intended `skills/` changes.
5. Push and verify skill rendering in your Codex/IDE environment.

### Risk Notice

This skill pack is still in active iteration.

- Back up project data before applying generated changes.
- Validate in a test branch/sandbox first.
- Review generated Blueprint/C++ outputs before merging.

## 中文

本目录提供面向 Unreal Engine 5.6/5.7 的 Codex 技能包。

### Skills 总览截图

![UE5 Skills 总览](./assets/ue5-skills-overview.png)

> 该图为 Codex Skills 面板截图，展示当前已安装的 UE5 技能集合及启用状态（截图时间：2026年3月3日）。

### 已包含技能

- 路由类技能：
  - `ue5-auto-assistant`
  - `ue5-module-router`
- 领域类技能：
  - `ue5-architecture`
  - `ue5-blueprint-workflow`
  - `ue5-cpp-gameplay`
  - `ue5-debug-validation`
  - `ue5-performance-packaging`
  - `ue5-save-load-replication`
  - `ue5-ui-umg-slate`
  - `ue5-world-interaction`
  - `ue5-pcg-building`

### UE5.7 可落地化升级状态

已完成升级的技能：

- `ue5-pcg-building`
- `ue5-blueprint-workflow`
- `ue5-cpp-gameplay`
- `ue5-save-load-replication`
- `ue5-world-interaction`
- `ue5-ui-umg-slate`
- `ue5-performance-packaging`
- `ue5-debug-validation`

以上技能统一补齐了：

- `UE5.7 API Anchors`（具体引擎类/函数/节点锚点）
- 阶段契约（保证实现可执行、可交付）
- 可执行故障处理（症状 -> 定位 -> 修复）
- UE5.6/UE5.7 兼容说明

### 推荐使用流程

1. 先用 `ue5-auto-assistant`
2. 识别到模块名时，使用 `ue5-module-router`
3. 执行目标技能

### 校验

```powershell
python .\skills\scripts\validate_skills.py
```

期望输出：`Validation OK`

### 风险提示

当前技能包仍在持续迭代中：

- 应用前先备份项目
- 先在测试分支或沙盒验证
- Blueprint/C++ 自动生成结果请人工复核后再合并
