# Claude Code Game Studios -- Game Studio Agent Architecture

Indie game development managed through 48 coordinated Claude Code subagents.
Each agent owns a specific domain, enforcing separation of concerns and quality.

## Technology Stack

- **Engine**: 团结引擎 1.9.0 (Tuanjie Engine, Unity 中国版)
- **Language**: C#
- **Version Control**: Git with trunk-based development
- **Build System**: 团结 Hub + Unity Build Automation
- **Asset Pipeline**: Addressables + AssetBundles

> **Note**: Engine-specialist agents exist for Godot, Unity, and Unreal with
> dedicated sub-specialists. Use the set matching your engine.

## Project Structure

@.claude/docs/directory-structure.md

## 游戏设计文档（星河倒悬）

所有游戏设计文档位于 `星河倒悬（女巫女巫别哭了）/` 目录，包含：

- **战斗系统** (14文档) — 核心战斗GDD、卦象战场引擎、64卦数据规格书、数值框架
- **术数系统** (22文档) — 12种术数战斗思维体系、选装Build、卦象交互
- **卦码系统** (6文档) — Build分享编码、实现规格书
- **道宫关卡** (12文档) — 世界地图、12道宫副本、敌人AI
- **装备道具** (8文档) — 法器锻造、装备、背包、成长
- **营地经济** (3文档) — 落星村重建、经济系统
- **界面视觉** (6文档) — 摄像机、UI/HUD、存档
- **narrative** (31文档) — 14章剧情大纲+正文、世界观时间线
- **经济系统分析** (18文档) — 参考游戏分析+完整设计
- **决策分析** (8文档) — 道士独挑决策全记录

项目总目录入口：`星河倒悬（女巫女巫别哭了）/00-总目录.md`
共享数据权威源：`星河倒悬（女巫女巫别哭了）/_shared_data.json`
Phase 1 开发计划：`星河倒悬（女巫女巫别哭了）/Phase1-开发计划.md`

## Engine Version Reference

@docs/engine-reference/unity/VERSION.md

## Technical Preferences

@.claude/docs/technical-preferences.md

## Coordination Rules

@.claude/docs/coordination-rules.md

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question -> Options -> Decision -> Draft -> Approval**

- Agents MUST ask "May I write this to [filepath]?" before using Write/Edit tools
- Agents MUST show drafts or summaries before requesting approval
- Multi-file changes require explicit approval for the full changeset
- No commits without user instruction

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for full protocol and examples.

> **First session?** If the project has no engine configured and no game concept,
> run `/start` to begin the guided onboarding flow.

## Coding Standards

@.claude/docs/coding-standards.md

### 中文注释强制规则

**所有代码文件（.cs / .gd / .cpp / .py 等）必须使用中文注释。**

- 每个文件的头部必须有中文说明（功能概述）
- 每个 class / struct / enum 必须有中文注释
- 每个 public 方法必须有中文注释（参数说明、返回值说明）
- 复杂逻辑必须有行内中文注释
- 注释以 `///`（XML文档注释）或 `//`（行注释）形式
- 此规则对已有代码和新代码均生效，不得遗漏

## Context Management

@.claude/docs/context-management.md
