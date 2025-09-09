#!/bin/bash
# 為目前分支設定實作計畫結構
# 回傳實作計畫產生所需的路徑
# 用法：./setup-plan.sh [--json]

set -e

JSON_MODE=false
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "用法：$0 [--json]"; exit 0 ;;
    esac
done

# 載入共用函式
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 取得所有路徑
eval $(get_feature_paths)

# 檢查是否在功能分支上
check_feature_branch "$CURRENT_BRANCH" || exit 1

# 如果 specs 目錄不存在則建立
mkdir -p "$FEATURE_DIR"

# 如果計畫範本存在則複製
TEMPLATE="$REPO_ROOT/templates/plan-template.md"
if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$IMPL_PLAN"
fi

if $JSON_MODE; then
    printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s"}\n' \
        "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH"
else
    # 輸出所有路徑供 LLM 使用
    echo "FEATURE_SPEC: $FEATURE_SPEC"
    echo "IMPL_PLAN: $IMPL_PLAN"
    echo "SPECS_DIR: $FEATURE_DIR"
    echo "BRANCH: $CURRENT_BRANCH"
fi