#!/bin/bash
# 取得目前功能分支的路徑，不建立任何內容
# 供需要尋找現有功能檔案的指令使用

set -e

# 載入共用函式
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 取得所有路徑
eval $(get_feature_paths)

# 檢查是否在功能分支上
check_feature_branch "$CURRENT_BRANCH" || exit 1

# 輸出路徑（不建立任何內容）
echo "REPO_ROOT: $REPO_ROOT"
echo "BRANCH: $CURRENT_BRANCH"
echo "FEATURE_DIR: $FEATURE_DIR"
echo "FEATURE_SPEC: $FEATURE_SPEC"
echo "IMPL_PLAN: $IMPL_PLAN"
echo "TASKS: $TASKS"