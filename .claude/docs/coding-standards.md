# Coding Standards

## 中文注释强制规则

**所有代码文件（.cs / .gd / .cpp / .py 等）必须使用中文注释。**
- 每个文件的头部必须有中文说明（文件功能概述）
- 每个 class / struct / enum 必须有中文注释
- 每个 public 方法必须有中文注释（参数说明、返回值说明）
- 复杂逻辑必须有行内中文注释
- 注释以 `///`（XML文档注释）或 `//`（行注释）形式
- 此规则对已有代码和新代码均生效，不得遗漏
- 所有回答、讨论、commit message 使用简体中文

## General Rules

- All game code must include doc comments on public APIs
- Every system must have a corresponding architecture decision record in `docs/architecture/`
- Gameplay values must be data-driven (external config), never hardcoded
- All public methods must be unit-testable (dependency injection over singletons)
- Commits must reference the relevant design document or task ID
- **Verification-driven development**: Write tests first when adding gameplay systems.
  For UI changes, verify with screenshots. Compare expected output to actual output
  before marking work complete. Every implementation should have a way to prove it works.

# Design Document Standards

## Obsidian 格式强制规则（所有 .md 设计文档）

**所有游戏设计文档必须使用 Obsidian 格式。** 此规则优先级等同于代码注释规则，违反即为不合格。

### Frontmatter（YAML 头·必填）

每个 .md 文件必须以 `---` 包裹的 YAML frontmatter 开头：

```yaml
---
category: <分类>        # 必填·从标签库选取
status: <状态>          # 必填·🟢已完成/📝编写中/📝待补充/📋参考/📦归档/📦废弃
phase: <阶段>           # 必填·Phase1/Phase2/Phase3/Phase4/全阶段
tags:                   # 必填·从标签库选取·至少2个
  - <标签1>
  - <标签2>
updated: YYYY-MM-DD     # 必填·最后修改日期
---
```

### Wikilink 互联（必填）

- 跨文档引用**必须**用 `[[文档名]]` 格式，禁止裸路径
- 同文件夹用短名 `[[战斗系统GDD]]`
- 跨文件夹用相对路径 `[[卦码系统/03-卦码实现规格书]]`
- 每个 GDD 底部必须有 `> **关联文档：**` 段落列出所有引用

### 标签规范（必填）

- 只使用标签库中已定义的标签
- **禁止**：纯数字（`#1`）、色值（`#C04040`）、未定义的自创标签
- 格式：`分类/子类`（如 `系统/战斗`、`GDD/关卡`）

### 数据权威（强制）

- 任何跨文档共享的数值**必须**在 `_shared_data.json` 中有唯一定义
- 修改数值→先改 `_shared_data.json`→再同步 .md 文档
- 修改后运行 `python _audit.py`，必须零问题

### 命名规范（必填）

- 文件名：中文 + 连字符（`-`），不用空格/下划线/特殊符号
- 例：`战斗系统GDD.md` ✅ / `战斗系统_GDD.md` ❌ / `Combat GDD.md` ❌

## GDD 内容标准

- All design docs use Markdown
- Each mechanic has a dedicated document in `design/gdd/`
- Documents must include these 8 required sections:
  1. **Overview** -- one-paragraph summary
  2. **Player Fantasy** -- intended feeling and experience
  3. **Detailed Rules** -- unambiguous mechanics
  4. **Formulas** -- all math defined with variables
  5. **Edge Cases** -- unusual situations handled
  6. **Dependencies** -- other systems listed
  7. **Tuning Knobs** -- configurable values identified
  8. **Acceptance Criteria** -- testable success conditions
- Balance values must link to their source formula or rationale

# Testing Standards

## Test Evidence by Story Type

All stories must have appropriate test evidence before they can be marked Done:

| Story Type | Required Evidence | Location | Gate Level |
|---|---|---|---|
| **Logic** (formulas, AI, state machines) | Automated unit test — must pass | `tests/unit/[system]/` | BLOCKING |
| **Integration** (multi-system) | Integration test OR documented playtest | `tests/integration/[system]/` | BLOCKING |
| **Visual/Feel** (animation, VFX, feel) | Screenshot + lead sign-off | `production/qa/evidence/` | ADVISORY |
| **UI** (menus, HUD, screens) | Manual walkthrough doc OR interaction test | `production/qa/evidence/` | ADVISORY |
| **Config/Data** (balance tuning) | Smoke check pass | `production/qa/smoke-[date].md` | ADVISORY |

## Automated Test Rules

- **Naming**: `[system]_[feature]_test.[ext]` for files; `test_[scenario]_[expected]` for functions
- **Determinism**: Tests must produce the same result every run — no random seeds, no time-dependent assertions
- **Isolation**: Each test sets up and tears down its own state; tests must not depend on execution order
- **No hardcoded data**: Test fixtures use constant files or factory functions, not inline magic numbers
  (exception: boundary value tests where the exact number IS the point)
- **Independence**: Unit tests do not call external APIs, databases, or file I/O — use dependency injection

## What NOT to Automate

- Visual fidelity (shader output, VFX appearance, animation curves)
- "Feel" qualities (input responsiveness, perceived weight, timing)
- Platform-specific rendering (test on target hardware, not headlessly)
- Full gameplay sessions (covered by playtesting, not automation)

## CI/CD Rules

- Automated test suite runs on every push to main and every PR
- No merge if tests fail — tests are a blocking gate in CI
- Never disable or skip failing tests to make CI pass — fix the underlying issue
- Engine-specific CI commands:
  - **Godot**: `godot --headless --script tests/gdunit4_runner.gd`
  - **Unity**: `game-ci/unity-test-runner@v4` (GitHub Actions)
  - **Unreal**: headless runner with `-nullrhi` flag
