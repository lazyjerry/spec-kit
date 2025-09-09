#!/bin/bash
# 根據新功能計畫逐步更新代理程式上下文檔案
# 支援：CLAUDE.md、GEMINI.md 和 .github/copilot-instructions.md
# O(1) 操作 - 僅讀取目前上下文檔案和新的 plan.md

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
FEATURE_DIR="$REPO_ROOT/specs/$CURRENT_BRANCH"
NEW_PLAN="$FEATURE_DIR/plan.md"

# 決定要更新哪些代理程式上下文檔案
CLAUDE_FILE="$REPO_ROOT/CLAUDE.md"
GEMINI_FILE="$REPO_ROOT/GEMINI.md"
COPILOT_FILE="$REPO_ROOT/.github/copilot-instructions.md"

# 允許透過參數覆寫
AGENT_TYPE="$1"

if [ ! -f "$NEW_PLAN" ]; then
    echo "錯誤：在 $NEW_PLAN 找不到 plan.md"
    exit 1
fi

echo "=== 為功能 $CURRENT_BRANCH 更新代理程式上下文檔案 ==="

# 從新計畫中提取技術資訊
NEW_LANG=$(grep "^**Language/Version**: " "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/^**Language\/Version**: //' | grep -v "NEEDS CLARIFICATION" || echo "")
NEW_FRAMEWORK=$(grep "^**Primary Dependencies**: " "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/^**Primary Dependencies**: //' | grep -v "NEEDS CLARIFICATION" || echo "")
NEW_TESTING=$(grep "^**Testing**: " "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/^**Testing**: //' | grep -v "NEEDS CLARIFICATION" || echo "")
NEW_DB=$(grep "^**Storage**: " "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/^**Storage**: //' | grep -v "N/A" | grep -v "NEEDS CLARIFICATION" || echo "")
NEW_PROJECT_TYPE=$(grep "^**Project Type**: " "$NEW_PLAN" 2>/dev/null | head -1 | sed 's/^**Project Type**: //' || echo "")

# 更新單一代理程式上下文檔案的函式
update_agent_file() {
    local target_file="$1"
    local agent_name="$2"
    
    echo "正在更新 $agent_name 上下文檔案：$target_file"
    
    # 為新上下文建立暫存檔案
    local temp_file=$(mktemp)
    
    # 如果檔案不存在，從範本建立
    if [ ! -f "$target_file" ]; then
        echo "正在建立新的 $agent_name 上下文檔案..."
        
        # 檢查這是否為 SDD 儲存庫本身
        if [ -f "$REPO_ROOT/templates/agent-file-template.md" ]; then
            cp "$REPO_ROOT/templates/agent-file-template.md" "$temp_file"
        else
            echo "錯誤：在 $REPO_ROOT/templates/agent-file-template.md 找不到範本"
            return 1
        fi
        
        # 替換佔位符
        sed -i.bak "s/\[PROJECT NAME\]/$(basename $REPO_ROOT)/" "$temp_file"
        sed -i.bak "s/\[DATE\]/$(date +%Y-%m-%d)/" "$temp_file"
        sed -i.bak "s/\[EXTRACTED FROM ALL PLAN.MD FILES\]/- $NEW_LANG + $NEW_FRAMEWORK ($CURRENT_BRANCH)/" "$temp_file"
        
        # 根據類型新增專案結構
        if [[ "$NEW_PROJECT_TYPE" == *"web"* ]]; then
            sed -i.bak "s|\[ACTUAL STRUCTURE FROM PLANS\]|backend/\nfrontend/\ntests/|" "$temp_file"
        else
            sed -i.bak "s|\[ACTUAL STRUCTURE FROM PLANS\]|src/\ntests/|" "$temp_file"
        fi
        
        # 新增最小指令集
        if [[ "$NEW_LANG" == *"Python"* ]]; then
            COMMANDS="cd src && pytest && ruff check ."
        elif [[ "$NEW_LANG" == *"Rust"* ]]; then
            COMMANDS="cargo test && cargo clippy"
        elif [[ "$NEW_LANG" == *"JavaScript"* ]] || [[ "$NEW_LANG" == *"TypeScript"* ]]; then
            COMMANDS="npm test && npm run lint"
        else
            COMMANDS="# Add commands for $NEW_LANG"
        fi
        sed -i.bak "s|\[ONLY COMMANDS FOR ACTIVE TECHNOLOGIES\]|$COMMANDS|" "$temp_file"
        
        # 新增程式碼風格
        sed -i.bak "s|\[LANGUAGE-SPECIFIC, ONLY FOR LANGUAGES IN USE\]|$NEW_LANG: Follow standard conventions|" "$temp_file"
        
        # 新增最近變更
        sed -i.bak "s|\[LAST 3 FEATURES AND WHAT THEY ADDED\]|- $CURRENT_BRANCH: Added $NEW_LANG + $NEW_FRAMEWORK|" "$temp_file"
        
        rm "$temp_file.bak"
    else
        echo "正在更新現有的 $agent_name 上下文檔案..."
        
        # 提取手動新增的內容
        local manual_start=$(grep -n "<!-- MANUAL ADDITIONS START -->" "$target_file" | cut -d: -f1)
        local manual_end=$(grep -n "<!-- MANUAL ADDITIONS END -->" "$target_file" | cut -d: -f1)
        
        if [ ! -z "$manual_start" ] && [ ! -z "$manual_end" ]; then
            sed -n "${manual_start},${manual_end}p" "$target_file" > /tmp/manual_additions.txt
        fi
        
        # 解析現有檔案並建立更新版本
        python3 - << EOF
import re
import sys
from datetime import datetime

# Read existing file
with open("$target_file", 'r') as f:
    content = f.read()

# Check if new tech already exists
tech_section = re.search(r'## Active Technologies\n(.*?)\n\n', content, re.DOTALL)
if tech_section:
    existing_tech = tech_section.group(1)
    
    # Add new tech if not already present
    new_additions = []
    if "$NEW_LANG" and "$NEW_LANG" not in existing_tech:
        new_additions.append(f"- $NEW_LANG + $NEW_FRAMEWORK ($CURRENT_BRANCH)")
    if "$NEW_DB" and "$NEW_DB" not in existing_tech and "$NEW_DB" != "N/A":
        new_additions.append(f"- $NEW_DB ($CURRENT_BRANCH)")
    
    if new_additions:
        updated_tech = existing_tech + "\n" + "\n".join(new_additions)
        content = content.replace(tech_section.group(0), f"## Active Technologies\n{updated_tech}\n\n")

# Update project structure if needed
if "$NEW_PROJECT_TYPE" == "web" and "frontend/" not in content:
    struct_section = re.search(r'## Project Structure\n\`\`\`\n(.*?)\n\`\`\`', content, re.DOTALL)
    if struct_section:
        updated_struct = struct_section.group(1) + "\nfrontend/src/      # Web UI"
        content = re.sub(r'(## Project Structure\n\`\`\`\n).*?(\n\`\`\`)', 
                        f'\\1{updated_struct}\\2', content, flags=re.DOTALL)

# Add new commands if language is new
if "$NEW_LANG" and f"# {NEW_LANG}" not in content:
    commands_section = re.search(r'## Commands\n\`\`\`bash\n(.*?)\n\`\`\`', content, re.DOTALL)
    if not commands_section:
        commands_section = re.search(r'## Commands\n(.*?)\n\n', content, re.DOTALL)
    
    if commands_section:
        new_commands = commands_section.group(1)
        if "Python" in "$NEW_LANG":
            new_commands += "\ncd src && pytest && ruff check ."
        elif "Rust" in "$NEW_LANG":
            new_commands += "\ncargo test && cargo clippy"
        elif "JavaScript" in "$NEW_LANG" or "TypeScript" in "$NEW_LANG":
            new_commands += "\nnpm test && npm run lint"
        
        if "```bash" in content:
            content = re.sub(r'(## Commands\n\`\`\`bash\n).*?(\n\`\`\`)', 
                            f'\\1{new_commands}\\2', content, flags=re.DOTALL)
        else:
            content = re.sub(r'(## Commands\n).*?(\n\n)', 
                            f'\\1{new_commands}\\2', content, flags=re.DOTALL)

# Update recent changes (keep only last 3)
changes_section = re.search(r'## Recent Changes\n(.*?)(\n\n|$)', content, re.DOTALL)
if changes_section:
    changes = changes_section.group(1).strip().split('\n')
    changes.insert(0, f"- $CURRENT_BRANCH: Added $NEW_LANG + $NEW_FRAMEWORK")
    # Keep only last 3
    changes = changes[:3]
    content = re.sub(r'(## Recent Changes\n).*?(\n\n|$)', 
                    f'\\1{chr(10).join(changes)}\\2', content, flags=re.DOTALL)

# Update date
content = re.sub(r'Last updated: \d{4}-\d{2}-\d{2}', 
                f'Last updated: {datetime.now().strftime("%Y-%m-%d")}', content)

# Write to temp file
with open("$temp_file", 'w') as f:
    f.write(content)
EOF

        # 如果手動新增的內容存在則還原
        if [ -f /tmp/manual_additions.txt ]; then
            # 從暫存檔案中移除舊的手動區段
            sed -i.bak '/<!-- MANUAL ADDITIONS START -->/,/<!-- MANUAL ADDITIONS END -->/d' "$temp_file"
            # 附加手動新增的內容
            cat /tmp/manual_additions.txt >> "$temp_file"
            rm /tmp/manual_additions.txt "$temp_file.bak"
        fi
    fi
    
    # 將暫存檔案移動到最終位置
    mv "$temp_file" "$target_file"
    echo "✅ $agent_name 上下文檔案更新成功"
}

# 根據參數更新檔案或偵測現有檔案
case "$AGENT_TYPE" in
    "claude")
        update_agent_file "$CLAUDE_FILE" "Claude Code"
        ;;
    "gemini") 
        update_agent_file "$GEMINI_FILE" "Gemini CLI"
        ;;
    "copilot")
        update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        ;;
    "")
        # 更新所有現有檔案
        [ -f "$CLAUDE_FILE" ] && update_agent_file "$CLAUDE_FILE" "Claude Code"
        [ -f "$GEMINI_FILE" ] && update_agent_file "$GEMINI_FILE" "Gemini CLI" 
        [ -f "$COPILOT_FILE" ] && update_agent_file "$COPILOT_FILE" "GitHub Copilot"
        
        # 如果沒有檔案存在，根據目前目錄建立或詢問使用者
        if [ ! -f "$CLAUDE_FILE" ] && [ ! -f "$GEMINI_FILE" ] && [ ! -f "$COPILOT_FILE" ]; then
            echo "找不到代理程式上下文檔案。預設建立 Claude Code 上下文檔案。"
            update_agent_file "$CLAUDE_FILE" "Claude Code"
        fi
        ;;
    *)
        echo "錯誤：未知的代理程式類型 '$AGENT_TYPE'。請使用：claude、gemini、copilot，或留空以更新全部。"
        exit 1
        ;;
esac
echo ""
echo "變更摘要："
if [ ! -z "$NEW_LANG" ]; then
    echo "- 新增語言：$NEW_LANG"
fi
if [ ! -z "$NEW_FRAMEWORK" ]; then
    echo "- 新增框架：$NEW_FRAMEWORK"
fi
if [ ! -z "$NEW_DB" ] && [ "$NEW_DB" != "N/A" ]; then
    echo "- 新增資料庫：$NEW_DB"
fi

echo ""
echo "用法：$0 [claude|gemini|copilot]"
echo "  - 無參數：更新所有現有的代理程式上下文檔案"
echo "  - claude：僅更新 CLAUDE.md"
echo "  - gemini：僅更新 GEMINI.md" 
echo "  - copilot：僅更新 .github/copilot-instructions.md"