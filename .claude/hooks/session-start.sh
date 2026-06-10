#!/bin/bash
# Claude Code SessionStart Hook: 恢复项目上下文
# 显示分支、最近提交、会话状态恢复指引

echo "=== Claude Code Game Studios — Session Context ==="

# 当前分支与仓库
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ -n "$BRANCH" ]; then
    REMOTE=$(git config --get "branch.$BRANCH.remote" 2>/dev/null)
    REPO_URL=$(git remote get-url "$REMOTE" 2>/dev/null)
    echo "Branch: $BRANCH"
    if [ -n "$REPO_URL" ]; then
        echo "Remote: $REPO_URL"
    fi

    echo ""
    echo "Recent commits:"
    git log --oneline -5 2>/dev/null | while read -r line; do
        echo "  $line"
    done
fi

# === 会话状态恢复 ===
STATE_FILE="production/session-state/active.md"
if [ -f "$STATE_FILE" ]; then
    echo ""
    echo "╔══════════════════════════════════════════╗"
    echo "║  📋 检测到上次会话状态                    ║"
    echo "╚══════════════════════════════════════════╝"
    echo ""

    # 提取 STATUS 注释块
    sed -n '/<!-- STATUS -->/,/<!-- \/STATUS -->/p' "$STATE_FILE" 2>/dev/null | grep -v "^<!--"

    # 提取任务进度
    echo ""
    echo "━━━ 任务进度 ━━━"
    grep -E "^\- \[.x\]|^\- \[ \]" "$STATE_FILE" 2>/dev/null | head -10

    # 提取下一步
    echo ""
    echo "━━━ 下一步 ━━━"
    NEXT=$(grep -A1 "^## 下一步" "$STATE_FILE" 2>/dev/null | tail -1)
    if [ -n "$NEXT" ]; then
        echo "  $NEXT"
    else
        echo "  读取 $STATE_FILE 了解完整上下文"
    fi

    echo ""
    echo "💡 直接说：\"继续之前的开发\" 即可无缝恢复。"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

# 代码健康速检
if [ -d "src" ]; then
    SRC_FILES=$(find src/ -name "*.cs" 2>/dev/null | wc -l)
    if [ "$SRC_FILES" -gt 0 ]; then
        TODO_COUNT=$(grep -r "TODO" src/ 2>/dev/null | wc -l)
        echo ""
        echo "Code: ${SRC_FILES} C# files, ${TODO_COUNT} TODOs"
    fi
fi

echo "==================================="
exit 0
