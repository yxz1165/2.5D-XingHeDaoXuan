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
