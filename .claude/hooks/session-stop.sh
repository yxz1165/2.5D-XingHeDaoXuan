#!/bin/bash
# Claude Code Stop Hook: 会话结束时自动保存并推送
# - 更新会话状态文件
# - 自动 git add / commit / push
# - 记录会话日志

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SESSION_LOG_DIR="production/session-logs"
STATE_FILE="production/session-state/active.md"
mkdir -p "$SESSION_LOG_DIR" 2>/dev/null

# === 1. 归档会话状态到日志 ===
if [ -f "$STATE_FILE" ]; then
    {
        echo "## 会话结束: $TIMESTAMP"
        cat "$STATE_FILE"
        echo "---"
        echo ""
    } >> "$SESSION_LOG_DIR/session-log.md" 2>/dev/null
fi

# === 2. 检查是否有未提交的更改 ===
CHANGES=$(git status --porcelain 2>/dev/null)
if [ -n "$CHANGES" ]; then
    echo "[Session Stop] 检测到未提交更改，自动保存..."

    # 生成提交信息（优先从 active.md 中提取任务描述）
    TASK_DESC=""
    if [ -f "$STATE_FILE" ]; then
        TASK_DESC=$(grep "^Task:" "$STATE_FILE" 2>/dev/null | head -1 | sed 's/^Task: //' | cut -c1-80)
    fi
    if [ -z "$TASK_DESC" ]; then
        TASK_DESC="会话自动存档"
    fi

    COMMIT_MSG="checkpoint: $TASK_DESC [$TIMESTAMP]"

    git add -A 2>/dev/null
    git commit -m "$COMMIT_MSG" 2>/dev/null

    # === 3. 推送到 GitHub ===
    git push origin HEAD 2>/dev/null &
    # 后台推送，不阻塞 hook 超时
fi

exit 0
