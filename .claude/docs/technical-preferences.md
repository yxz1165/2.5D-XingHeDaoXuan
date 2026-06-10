# Technical Preferences

<!-- Populated by /setup-engine. Updated as the user makes decisions throughout development. -->
<!-- All agents reference this file for project-specific standards and conventions. -->

## Engine & Language

- **Engine**: 团结引擎 1.9.0 (Tuanjie Engine)
- **Language**: C# (.NET 9)
- **Rendering**: URP (Universal Render Pipeline) — 2.5D 风格渲染
- **Physics**: Unity Physics (默认 3D 物理，2.5D 场景用 3D 碰撞体约束 Z 轴)

## Input & Platform

<!-- Written by /setup-engine. Read by /ux-design, /ux-review, /test-setup, /team-ui, and /dev-story -->
<!-- to scope interaction specs, test helpers, and implementation to the correct input methods. -->

- **Target Platforms**: PC (Windows 优先), 后续考虑移动端
- **Input Methods**: Keyboard/Mouse + Gamepad
- **Primary Input**: Keyboard/Mouse
- **Gamepad Support**: Full (Xbox 布局)
- **Touch Support**: None (首发 PC)
- **Platform Notes**: 团结引擎天然支持微信小游戏/抖音小游戏/鸿蒙，如后续扩展移动端可快速导出

## Naming Conventions

- **Classes**: PascalCase — `PlayerController`, `DaoPalaceManager`
- **Variables**: camelCase — `moveSpeed`, `currentHealth`
- **Events**: PascalCase + 过去式 — `OnDamageTaken`, `OnDoorOpened`
- **Files**: 与主类名一致 — `PlayerController.cs`
- **Scenes/Prefabs**: PascalCase + 中文注释 — `DaoPalace_01_StarJi.unity`
- **Constants**: UPPER_SNAKE_CASE — `MAX_SAVE_SLOTS`, `DEFAULT_PLAYER_HEALTH`

## Performance Budgets

- **Target Framerate**: [TO BE CONFIGURED]
- **Frame Budget**: [TO BE CONFIGURED]
- **Draw Calls**: [TO BE CONFIGURED]
- **Memory Ceiling**: [TO BE CONFIGURED]

## Testing

- **Framework**: [TO BE CONFIGURED]
- **Minimum Coverage**: [TO BE CONFIGURED]
- **Required Tests**: Balance formulas, gameplay systems, networking (if applicable)

## Forbidden Patterns

<!-- Add patterns that should never appear in this project's codebase -->
- [None configured yet — add as architectural decisions are made]

## Allowed Libraries / Addons

<!-- Add approved third-party dependencies here -->
- [None configured yet — add as dependencies are approved]

## Architecture Decisions Log

<!-- Quick reference linking to full ADRs in docs/architecture/ -->
- [No ADRs yet — use /architecture-decision to create one]

## Engine Specialists

<!-- Written by /setup-engine when engine is configured. -->
<!-- Read by /code-review, /architecture-decision, /architecture-review, and team skills -->
<!-- to know which specialist to spawn for engine-specific validation. -->

- **Primary**: unity-specialist — 团结引擎/Unity 通用架构
- **Language/Code Specialist**: unity-specialist — C# 代码规范与 Unity API
- **Shader Specialist**: unity-shader-specialist — Shader Graph + HLSL
- **UI Specialist**: unity-ui-specialist — UI Toolkit (推荐) + UGUI
- **Additional Specialists**: unity-addressables-specialist (资产加载), unity-dots-specialist (如后续需要 DOTS)
- **Routing Notes**: 团结引擎与 Unity API 高度兼容，unity-* 系列 agent 可直接使用

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
|-----------------------|---------------------|
| `.cs` (C# 游戏代码) | unity-specialist |
| Shader / material files | unity-shader-specialist |
| UI / screen files (.uxml, .uss, .prefab) | unity-ui-specialist |
| Scene / prefab / level files (.unity) | unity-specialist |
| Addressables 配置 | unity-addressables-specialist |
| General architecture review | lead-programmer |
