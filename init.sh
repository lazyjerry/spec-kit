#!/bin/bash

# Spec-kit 初始化腳本
# 此腳本會：
# 1. 提示輸入專案名稱
# 2. 使用 uvx 指令來初始化專案
# 3. 驗證專案建立成功

set -e  # 如果任何命令失敗就退出

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函數：印出帶顏色的訊息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查是否在 macOS 上
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_warning "此腳本是為 macOS 設計的，在其他系統上可能需要調整"
fi

# 獲取當前用戶名稱
CURRENT_USER=$(whoami)
print_info "當前用戶: $CURRENT_USER"

# 步驟 1: 輸入專案名稱
echo ""
echo "=== Spec-kit 專案初始化 ==="
echo ""
read -p "請輸入專案名稱: " PROJECT_NAME

# 驗證專案名稱
if [[ -z "$PROJECT_NAME" ]]; then
    print_error "專案名稱不能為空"
    exit 1
fi

# 檢查專案名稱是否包含無效字符
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    print_error "專案名稱只能包含英文字母、數字、底線和連字符"
    exit 1
fi

# 檢查目錄是否已存在
if [[ -d "$PROJECT_NAME" ]]; then
    print_error "目錄 '$PROJECT_NAME' 已存在，請選擇其他名稱或刪除現有目錄"
    exit 1
fi

print_info "專案名稱: $PROJECT_NAME"
print_info "將在當前目錄創建專案: $(pwd)/$PROJECT_NAME"

# 確認是否繼續
echo ""
read -p "確定要繼續嗎？(y/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Yy]$ ]]; then
    print_info "操作已取消"
    exit 0
fi

echo ""
print_info "開始初始化專案..."

# 步驟 2: 使用本地腳本初始化專案
print_info "正在執行 spec-kit 初始化指令（使用本地版本）..."

# 檢查本地腳本是否存在
LOCAL_SCRIPT="/Users/lazyjerry/Dropbox/個人project/個人用專案/spec-kit/src/specify_cli/__init__.py"
if [[ ! -f "$LOCAL_SCRIPT" ]]; then
    print_error "本地 spec-kit 腳本不存在：$LOCAL_SCRIPT"
    exit 1
fi

# 創建本地範本複製功能
echo ""
print_info "使用本地範本創建專案..."

# 創建專案目錄
mkdir -p "$PROJECT_NAME"

# 複製範本文件
TEMPLATE_DIR="/Users/lazyjerry/Dropbox/個人project/個人用專案/spec-kit/templates"
if [[ -d "$TEMPLATE_DIR" ]]; then
    cp -r "$TEMPLATE_DIR"/* "$PROJECT_NAME"/
    print_success "範本文件複製完成"
else
    print_error "找不到範本目錄：$TEMPLATE_DIR"
    exit 1
fi

# 步驟 3: 檢查專案目錄是否創建成功
if [[ ! -d "$PROJECT_NAME" ]]; then
    print_error "專案目錄 '$PROJECT_NAME' 未找到，初始化可能失敗"
    exit 1
fi

# 驗證權限設定
OWNER=$(stat -f "%Su" "$PROJECT_NAME")
if [[ "$OWNER" == "$CURRENT_USER" ]]; then
    print_success "權限驗證通過，目錄擁有者: $OWNER"
else
    print_info "目錄擁有者: $OWNER"
fi

echo ""
print_success "=== 專案初始化完成！ ==="
print_info "專案位置: $(pwd)/$PROJECT_NAME"
print_info "你現在可以進入專案目錄開始工作："
echo "  cd $PROJECT_NAME"

echo ""
print_info "如需查看專案內容："
echo "  ls -la $PROJECT_NAME"
