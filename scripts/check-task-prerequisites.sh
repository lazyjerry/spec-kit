#!/bin/bash
# 檢查實作計畫是否存在並尋找選用的設計文件
# 用法：./check-task-prerequisites.sh [--json]

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

# 檢查功能目錄是否存在
if [[ ! -d "$FEATURE_DIR" ]]; then
    echo "錯誤：找不到功能目錄：$FEATURE_DIR"
    echo "請先執行 /specify 來建立功能結構。"
    exit 1
fi

# 檢查實作計畫（必需）
if [[ ! -f "$IMPL_PLAN" ]]; then
    echo "錯誤：在 $FEATURE_DIR 中找不到 plan.md"
    echo "請先執行 /plan 來建立計畫。"
    exit 1
fi

if $JSON_MODE; then
    # 建立實際存在的可用文件的 JSON 陣列
    docs=()
    [[ -f "$RESEARCH" ]] && docs+=("research.md")
    [[ -f "$DATA_MODEL" ]] && docs+=("data-model.md")
    ([[ -d "$CONTRACTS_DIR" ]] && [[ -n "$(ls -A "$CONTRACTS_DIR" 2>/dev/null)" ]]) && docs+=("contracts/")
    [[ -f "$QUICKSTART" ]] && docs+=("quickstart.md")
    # 將陣列合併為 JSON 格式
    json_docs=$(printf '"%s",' "${docs[@]}")
    json_docs="[${json_docs%,}]"
    printf '{"FEATURE_DIR":"%s","AVAILABLE_DOCS":%s}\n' "$FEATURE_DIR" "$json_docs"
else
    # 列出可用的設計文件（選用）
    echo "FEATURE_DIR:$FEATURE_DIR"
    echo "AVAILABLE_DOCS:"

    # 使用共用檢查函式
    check_file "$RESEARCH" "research.md"
    check_file "$DATA_MODEL" "data-model.md"
    check_dir "$CONTRACTS_DIR" "contracts/"
    check_file "$QUICKSTART" "quickstart.md"
fi

# 總是成功 - 任務產生應該能使用任何可用的文件