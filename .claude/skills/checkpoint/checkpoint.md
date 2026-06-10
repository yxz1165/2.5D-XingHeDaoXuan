---
name: checkpoint
description: 创建开发存档点——保存会话状态、提交代码、推送到 GitHub。关掉前或完成重要里程碑时使用。
model: haiku
---

# 检查点 / Checkpoint

创建开发存档点。调用时机：
- 关掉 Claude Code 之前
- 完成一个重要里程碑后
- 想确保当前进度已保存时

## 执行

```bash
bash .claude/skills/checkpoint/checkpoint.sh
```

执行后：
1. 更新 `production/session-state/active.md` 时间戳
2. `git add -A && git commit` 当前所有变更
3. `git push` 到 GitHub
4. 输出存档确认

下次打开项目时，`session-start.sh` 会自动检测 `active.md` 并提供恢复指引。
用户只需说 **"继续之前的开发"** 即可无缝恢复。
