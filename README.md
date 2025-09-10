<p align="center">
    <em>Jerry 客製化版本</em>
</p>

<div align="center">
    <img src="./media/logo_small.webp"/>
    <h1>🌱 Spec Kit</h1>
    <h3><em>更快速地建構高品質軟體。</em></h3>
</div>

<p align="center">
    <strong>透過規格驅動開發 (Spec-Driven Development) 的協助，讓組織能夠專注於產品情境，而非撰寫無差異化的程式碼。</strong>
</p>

[![Release](https://github.com/github/spec-kit/actions/workflows/release.yml/badge.svg)](https://github.com/github/spec-kit/actions/workflows/release.yml)

---

## 目錄

- [🤔 什麼是規格驅動開發？](#-什麼是規格驅動開發)
- [⚡ 開始使用](#-開始使用)
- [📚 核心理念](#-核心理念)
- [🌟 開發階段](#-開發階段)
- [🎯 實驗目標](#-實驗目標)
- [🔧 前置需求](#-前置需求)
- [📖 了解更多](#-了解更多)
- [詳細流程](#詳細流程)
- [疑難排解](#疑難排解)

## 🤔 什麼是規格驅動開發？

規格驅動開發 **顛覆了** 傳統軟體開發的模式。數十年來，程式碼一直是王道——規格只是我們建構的鷹架，一旦「真正的」編碼工作開始就會被丟棄。規格驅動開發改變了這一點：**規格變得可執行**，直接產生可運作的實作，而不僅僅是指導它們。

## ⚡ 開始使用

### 1. 安裝 Specify

根據你使用的編碼代理程式來初始化專案：

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

### 2. 建立規格

使用 `/specify` 指令來描述你想要建構的內容。專注於 **什麼** 和 **為什麼**，而不是技術堆疊。

```bash
/specify Build an application that can help me organize my photos in separate photo albums. Albums are grouped by date and can be re-organized by dragging and dropping on the main page. Albums never other nested albums. Within each album, photos are previewed in a tile-like interface.
```

### 3. 建立技術實作計畫

使用 `/plan` 指令來提供你的技術堆疊和架構選擇。

```bash
/plan The application uses Vite with minimal number of libraries. Use vanilla HTML, CSS, and JavaScript as much as possible. Images are not uploaded anywhere and metadata is stored in a local SQLite database.
```

### 4. 分解並實作

使用 `/tasks` 來建立可執行的任務清單，然後請你的代理程式實作功能。

詳細的逐步說明，請參閱我們的 [完整指南](./spec-driven.md)。

## 📚 核心理念

規格驅動開發是一個結構化的流程，強調：

- **意圖驅動開發**，規格在「_如何做_」之前先定義「_做什麼_」
- **豐富的規格建立**，使用護欄和組織原則
- **多步驟精煉**，而非從提示一次性產生程式碼
- **高度依賴** 先進 AI 模型的規格解釋能力

## 🌟 開發階段

| 階段                             | 重點         | 主要活動                                                                                            |
| -------------------------------- | ------------ | --------------------------------------------------------------------------------------------------- |
| **從零到一開發**（「綠地專案」） | 從頭開始產生 | <ul><li>從高階需求開始</li><li>產生規格</li><li>規劃實作步驟</li><li>建構可投產的應用程式</li></ul> |
| **創意探索**                     | 平行實作     | <ul><li>探索多樣化解決方案</li><li>支援多種技術堆疊與架構</li><li>實驗 UX 模式</li></ul>            |
| **迭代增強**（「棕地專案」）     | 棕地現代化   | <ul><li>迭代新增功能</li><li>現代化舊有系統</li><li>調整流程</li></ul>                              |

## 🎯 實驗目標

我們的研究和實驗專注於：

### 技術獨立性

- 使用多樣化的技術堆疊建立應用程式
- 驗證規格驅動開發是一個不受特定技術、程式語言或框架束縛的流程假設

### 企業限制

- 展示關鍵任務應用程式開發
- 納入組織限制（雲端供應商、技術堆疊、工程實務）
- 支援企業設計系統和合規需求

### 以使用者為中心的開發

- 為不同使用者群體和偏好建構應用程式
- 支援各種開發方法（從氛圍編碼到 AI 原生開發）

### 創意與迭代流程

- 驗證平行實作探索的概念
- 提供強健的迭代功能開發工作流程
- 擴展流程以處理升級和現代化任務

## 🔧 前置需求

- **Linux/macOS**（或 Windows 上的 WSL2）
- AI 編碼代理程式：[Claude Code](https://www.anthropic.com/claude-code)、[GitHub Copilot](https://code.visualstudio.com/) 或 [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [uv](https://docs.astral.sh/uv/) 用於套件管理
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 📖 了解更多

- **[完整規格驅動開發方法論](./spec-driven.md)** - 深入了解完整流程
- **[詳細演練](#詳細流程)** - 逐步實作指南

---

## 詳細流程

<details>
<summary>點擊展開詳細的逐步演練</summary>

你可以使用 Specify CLI 來啟動你的專案，這會在你的環境中引入所需的工件。執行：

```bash
specify init <project_name>
```

或在目前目錄中初始化：

```bash
specify init --here
```

![Specify CLI 在終端機中啟動新專案](./media/specify_cli.gif)

系統會提示你選擇正在使用的 AI 代理程式。你也可以直接在終端機中主動指定：

```bash
specify init <project_name> --ai claude
specify init <project_name> --ai gemini
specify init <project_name> --ai copilot
# 或在目前目錄中：
specify init --here --ai claude
```

CLI 會檢查你是否已安裝 Claude Code 或 Gemini CLI。如果沒有，或者你偏好在不檢查正確工具的情況下取得範本，請在指令中使用 `--ignore-agent-tools`：

```bash
specify init <project_name> --ai claude --ignore-agent-tools
```

### **步驟 1：** 啟動專案

前往專案資料夾並執行你的 AI 代理程式。在我們的範例中，我們使用 `claude`。

![啟動 Claude Code 環境](./media/bootstrap-claude-code.gif)

如果你看到 `/specify`、`/plan` 和 `/tasks` 指令可用，就表示設定正確。

第一步應該是建立新的專案鷹架。使用 `/specify` 指令，然後提供你想要開發的專案的具體需求。

> [!IMPORTANT]
> 盡可能明確地說明你想要建構 _什麼_ 以及 _為什麼_。**此時不要專注於技術堆疊**。

範例提示：

```text
開發 Taskify，一個團隊生產力平台。它應該允許使用者建立專案、新增團隊成員、
指派任務、留言，並以看板風格在看板之間移動任務。在這個功能的初始階段，
我們稱之為「建立 Taskify」，讓我們有多個使用者，但使用者將預先宣告、預先定義。
我想要五個使用者分為兩個不同類別，一個產品經理和四個工程師。讓我們建立三個
不同的範例專案。讓我們為每個任務的狀態設定標準看板欄位，例如「待辦」、
「進行中」、「審查中」和「完成」。這個應用程式不會有登入功能，因為這只是
確保我們基本功能設定的第一個測試。對於任務卡片 UI 中的每個任務，
你應該能夠在看板工作板的不同欄位之間變更任務的目前狀態。
你應該能夠為特定卡片留下無限數量的留言。你應該能夠從該任務
卡片指派其中一個有效使用者。當你第一次啟動 Taskify 時，它會給你一個五個使用者的清單供選擇。
不需要密碼。當你點擊使用者時，你會進入主檢視，顯示專案清單。
當你點擊專案時，你會開啟該專案的看板。你會看到欄位。
你將能夠在不同欄位之間拖放卡片。你會看到任何指派給你（目前登入使用者）的卡片
以不同顏色顯示，這樣你就能快速看到你的卡片。你可以編輯你留下的任何留言，
但不能編輯其他人留下的留言。你可以刪除你留下的任何留言，但不能刪除其他人留下的留言。
```

輸入此提示後，你應該會看到 Claude Code 啟動規劃和規格草擬流程。Claude Code 也會觸發一些內建腳本來設定儲存庫。

完成此步驟後，你應該會建立一個新分支（例如 `001-create-taskify`），以及在 `specs/001-create-taskify` 目錄中的新規格。

產生的規格應該包含一組使用者故事和功能需求，如範本中定義的。

在此階段，你的專案資料夾內容應該類似以下：

```text
├── memory
│	 ├── constitution.md
│	 └── constitution_update_checklist.md
├── scripts
│	 ├── check-task-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── get-feature-paths.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	     └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

### **步驟 2：** 功能規格澄清

建立基準規格後，你可以繼續澄清在第一次嘗試中未正確捕捉的任何需求。例如，你可以在同一個 Claude Code 會話中使用這樣的提示：

```text
對於你建立的每個範例專案或專案，應該有 5 到 15 個任務的變動數量，
每個專案的任務隨機分佈到不同的完成狀態。確保每個完成階段至少有一個任務。
```

你也應該要求 Claude Code 驗證 **審查與接受檢查清單**，勾選已驗證/通過需求的項目，未通過的項目保持未勾選。可以使用以下提示：

```text
閱讀審查與接受檢查清單，如果功能規格符合標準，請勾選檢查清單中的每個項目。如果不符合，請保持空白。
```

重要的是要利用與 Claude Code 的互動作為澄清和詢問規格相關問題的機會 - **不要將其第一次嘗試視為最終版本**。

### **步驟 3：** 產生計畫

現在你可以具體說明技術堆疊和其他技術需求。你可以使用專案範本內建的 `/plan` 指令，搭配這樣的提示：

```text
我們將使用 .NET Aspire 來產生這個，使用 Postgres 作為資料庫。前端應該使用
具有拖放任務看板、即時更新的 Blazor server。應該建立一個 REST API，包含專案 API、
任務 API 和通知 API。
```

此步驟的輸出將包含多個實作細節文件，你的目錄樹會類似這樣：

```text
.
├── CLAUDE.md
├── memory
│	 ├── constitution.md
│	 └── constitution_update_checklist.md
├── scripts
│	 ├── check-task-prerequisites.sh
│	 ├── common.sh
│	 ├── create-new-feature.sh
│	 ├── get-feature-paths.sh
│	 ├── setup-plan.sh
│	 └── update-claude-md.sh
├── specs
│	 └── 001-create-taskify
│	     ├── contracts
│	     │	 ├── api-spec.json
│	     │	 └── signalr-spec.md
│	     ├── data-model.md
│	     ├── plan.md
│	     ├── quickstart.md
│	     ├── research.md
│	     └── spec.md
└── templates
    ├── CLAUDE-template.md
    ├── plan-template.md
    ├── spec-template.md
    └── tasks-template.md
```

檢查 `research.md` 文件，確保根據你的指示使用正確的技術堆疊。如果任何元件突出，你可以要求 Claude Code 精煉它，甚至讓它檢查你想要使用的平台/框架的本地安裝版本（例如 .NET）。

此外，如果選擇的技術堆疊是快速變化的（例如 .NET Aspire、JS 框架），你可能想要求 Claude Code 研究相關細節，使用這樣的提示：

```text
我希望你檢視實作計畫和實作細節，尋找可能受益於額外研究的領域，
因為 .NET Aspire 是一個快速變化的函式庫。對於你識別出需要進一步研究的領域，
我希望你更新研究文件，加入我們將在這個 Taskify 應用程式中使用的特定版本的額外細節，
並產生平行研究任務，使用網路研究來澄清任何細節。
```

在此過程中，你可能會發現 Claude Code 卡在研究錯誤的事情上 - 你可以用這樣的提示來幫助引導它朝正確方向：

```text
我認為我們需要將此分解為一系列步驟。首先，識別一個你在實作期間需要做的任務清單，
這些任務是你不確定的或會受益於進一步研究的。寫下這些任務的清單。然後對於每一個任務，
我希望你啟動一個單獨的研究任務，這樣最終結果是我們平行研究所有這些非常具體的任務。
我看到你在做的是，看起來你在一般性地研究 .NET Aspire，我認為在這種情況下這對我們沒有太大幫助。
這是過於無目標的研究。研究需要幫助你解決特定的目標問題。
```

> [!NOTE]
> Claude Code 可能過於積極，新增你未要求的元件。請要求它澄清理由和變更來源。

### **步驟 4：** 讓 Claude Code 驗證計畫

有了計畫後，你應該讓 Claude Code 檢視它，確保沒有遺漏的部分。你可以使用這樣的提示：

```text
現在我希望你去稽核實作計畫和實作細節檔案。
仔細閱讀，著眼於確定是否有一系列你需要執行的任務，這些任務從閱讀中是顯而易見的。
因為我不知道這裡是否足夠。例如，當我查看核心實作時，
在實作細節中參考適當的位置會很有用，這樣它就能在核心實作或精煉的每個步驟中找到資訊。
```

這有助於精煉實作計畫，並幫助你避免 Claude Code 在規劃週期中遺漏的潛在盲點。一旦初始精煉通過完成，請要求 Claude Code 在你進入實作之前再次檢視檢查清單。

你也可以要求 Claude Code（如果你已安裝 [GitHub CLI](https://docs.github.com/en/github-cli/github-cli)）繼續從你目前的分支建立一個詳細描述的 pull request 到 `main`，以確保工作得到適當追蹤。

> [!NOTE]
> 在讓代理程式實作之前，也值得提示 Claude Code 交叉檢查細節，看看是否有任何過度工程化的部分（記住 - 它可能過於積極）。如果存在過度工程化的元件或決策，你可以要求 Claude Code 解決它們。確保 Claude Code 遵循 [憲法](base/memory/constitution.md) 作為建立計畫時必須遵守的基礎。

### 步驟 5：實作

準備就緒後，指示 Claude Code 實作你的解決方案（包含範例路徑）：

```text
implement specs/002-create-taskify/plan.md
```

Claude Code 會立即行動並開始建立實作。

> [!IMPORTANT]
> Claude Code 會執行本地 CLI 指令（例如 `dotnet`）- 確保你的機器上已安裝這些指令。

實作步驟完成後，要求 Claude Code 嘗試執行應用程式並解決任何出現的建置錯誤。如果應用程式執行，但有 _執行時期錯誤_ 無法透過 CLI 日誌直接提供給 Claude Code（例如在瀏覽器日誌中呈現的錯誤），請將錯誤複製並貼上到 Claude Code 中，讓它嘗試解決。

</details>

---

## 疑難排解

### Linux 上的 Git 憑證管理員

如果你在 Linux 上遇到 Git 驗證問題，可以安裝 Git 憑證管理員：

```bash
#!/bin/bash
set -e
echo "正在下載 Git 憑證管理員 v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "正在安裝 Git 憑證管理員..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "正在設定 Git 使用 GCM..."
git config --global credential.helper manager
echo "正在清理..."
rm gcm-linux_amd64.2.6.1.deb
```

## 維護者

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 支援

如需支援，請開啟 [GitHub issue](https://github.com/github/spec-kit/issues/new)。我們歡迎錯誤回報、功能請求，以及關於使用規格驅動開發的問題。

## 致謝

此專案深受 [John Lam](https://github.com/jflam) 的工作和研究影響並以此為基礎。

## 授權

此專案依據 MIT 開源授權條款授權。完整條款請參閱 [LICENSE](./LICENSE) 檔案。
