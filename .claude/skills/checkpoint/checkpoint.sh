#!/bin/bash
# /checkpoint — 手动存档点
# 更新会话状态 → 保存内存 → 提交并推送
# 用法: bash .claude/skills/checkpoint/checkpoint.sh "存档描述"

MSG="${1:-手动存档} $(date '+%m-%d %H:%M')"

STATE_FILE="production/session-state/active.md"
MEMORY_DIR="$HOME/.claude/projects/I--Software-AI-Claude-Code-Game-Studios-2-5D--/memory"

echo "📦 创建存档点..."

# 1. 更新时间戳
if [ -f "$STATE_FILE" ]; then
    sed -i "s/\*\*最后更新\*\*：.*/\*\*最后更新\*\*：$(date '+%Y-%m-%d %H:%M')/" "$STATE_FILE" 2>/dev/null
    echo "  ✅ 会话状态已更新"
fi

# 2. Git 提交推送
CHANGES=$(git status --porcelain 2>/dev/null)
if [ -n "$CHANGES" ]; then
    git add -A 2>/dev/null
    git commit -m "checkpoint: $MSG" 2>/dev/null
    echo "  ✅ 已提交: $MSG"

    # 后台推送
    git push origin HEAD 2>/dev/null &
    echo "  ✅ 正在推送至 GitHub..."
else
    echo "  ℹ️  无变更，跳过提交"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  存档完成。下次打开项目时自动恢复。"
echo "  恢复指令：\"继续之前的开发\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
