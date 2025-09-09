# 實作計畫：[FEATURE]

**分支**：`[###-feature-name]` | **日期**：[DATE] | **規格**：[link]
**輸入**：來自 `/specs/[###-feature-name]/spec.md` 的功能規格

## 執行流程（/plan 指令範圍）

```
1. 從輸入路徑載入功能規格
   → 如果找不到：錯誤 "在 {path} 找不到功能規格"
2. 填寫技術背景（掃描 NEEDS CLARIFICATION）
   → 從背景偵測專案類型（web=前端+後端，mobile=應用程式+api）
   → 根據專案類型設定結構決策
3. 評估下方憲法檢查章節
   → 如果存在違規：記錄在複雜度追蹤中
   → 如果無法證明合理性：錯誤 "請先簡化方法"
   → 更新進度追蹤：初始憲法檢查
4. 執行階段 0 → research.md
   → 如果仍有 NEEDS CLARIFICATION：錯誤 "解決未知項目"
5. 執行階段 1 → contracts、data-model.md、quickstart.md、代理程式特定範本檔案（例如 Claude Code 的 `CLAUDE.md`、GitHub Copilot 的 `.github/copilot-instructions.md`，或 Gemini CLI 的 `GEMINI.md`）
6. 重新評估憲法檢查章節
   → 如果有新違規：重構設計，回到階段 1
   → 更新進度追蹤：設計後憲法檢查
7. 規劃階段 2 → 描述任務產生方法（不要建立 tasks.md）
8. 停止 - 準備執行 /tasks 指令
```

**重要**：/plan 指令在步驟 7 停止。階段 2-4 由其他指令執行：

- 階段 2：/tasks 指令建立 tasks.md
- 階段 3-4：實作執行（手動或透過工具）

## 摘要

[從功能規格中提取：主要需求 + 來自研究的技術方法]

## 技術背景

**語言/版本**：[例如 Python 3.11、Swift 5.9、Rust 1.75 或 NEEDS CLARIFICATION]  
**主要相依性**：[例如 FastAPI、UIKit、LLVM 或 NEEDS CLARIFICATION]  
**儲存**：[如果適用，例如 PostgreSQL、CoreData、檔案或 N/A]  
**測試**：[例如 pytest、XCTest、cargo test 或 NEEDS CLARIFICATION]  
**目標平台**：[例如 Linux 伺服器、iOS 15+、WASM 或 NEEDS CLARIFICATION]
**專案類型**：[single/web/mobile - 決定原始碼結構]  
**效能目標**：[領域特定，例如 1000 req/s、10k lines/sec、60 fps 或 NEEDS CLARIFICATION]  
**限制條件**：[領域特定，例如 <200ms p95、<100MB 記憶體、離線功能或 NEEDS CLARIFICATION]  
**規模/範圍**：[領域特定，例如 10k 使用者、1M LOC、50 個畫面或 NEEDS CLARIFICATION]

## 憲法檢查

_閘門：必須在階段 0 研究之前通過。在階段 1 設計後重新檢查。_

**簡潔性**：

- 專案：[#]（最多 3 個 - 例如 api、cli、tests）
- 直接使用框架？（無包裝類別）
- 單一資料模型？（除非序列化不同，否則無 DTO）
- 避免模式？（沒有經過驗證的需求就不使用 Repository/UoW）

**架構**：

- 每個功能都作為函式庫？（無直接應用程式程式碼）
- 函式庫清單：[每個的名稱 + 目的]
- 每個函式庫的 CLI：[具有 --help/--version/--format 的指令]
- 函式庫文件：計畫使用 llms.txt 格式？

**測試（不可協商）**：

- 強制執行 RED-GREEN-重構循環？（測試必須先失敗）
- Git 提交顯示測試在實作之前？
- 順序：嚴格遵循 Contract→Integration→E2E→Unit？
- 使用真實相依性？（實際資料庫，非模擬）
- 整合測試用於：新函式庫、合約變更、共享架構？
- 禁止：在測試之前實作、跳過 RED 階段

**可觀測性**：

- 包含結構化日誌記錄？
- 前端日誌 → 後端？（統一串流）
- 錯誤背景足夠？

**版本控制**：

- 已指派版本號？（MAJOR.MINOR.BUILD）
- BUILD 在每次變更時遞增？
- 處理破壞性變更？（平行測試、遷移計畫）

## 專案結構

### 文件（此功能）

```
specs/[###-feature]/
├── plan.md              # 此檔案（/plan 指令輸出）
├── research.md          # 階段 0 輸出（/plan 指令）
├── data-model.md        # 階段 1 輸出（/plan 指令）
├── quickstart.md        # 階段 1 輸出（/plan 指令）
├── contracts/           # 階段 1 輸出（/plan 指令）
└── tasks.md             # 階段 2 輸出（/tasks 指令 - 不由 /plan 建立）
```

### 原始碼（儲存庫根目錄）

```
# 選項 1：單一專案（預設）
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# 選項 2：Web 應用程式（偵測到「前端」+「後端」時）
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# 選項 3：行動裝置 + API（偵測到「iOS/Android」時）
api/
└── [與上述後端相同]

ios/ or android/
└── [平台特定結構]
```

**結構決策**：[預設為選項 1，除非技術背景指示 web/mobile 應用程式]

## 階段 0：大綱與研究

1. **從上述技術背景中提取未知項目**：

   - 每個 NEEDS CLARIFICATION → 研究任務
   - 每個相依性 → 最佳實務任務
   - 每個整合 → 模式任務

2. **產生並派遣研究代理程式**：

   ```
   對於技術背景中的每個未知項目：
     任務：「為 {功能背景} 研究 {未知項目}」
   對於每個技術選擇：
     任務：「在 {領域} 中尋找 {技術} 的最佳實務」
   ```

3. **在 `research.md` 中整合發現**，使用格式：
   - 決策：[選擇了什麼]
   - 理由：[為什麼選擇]
   - 考慮的替代方案：[還評估了什麼]

**輸出**：解決所有 NEEDS CLARIFICATION 的 research.md

## 階段 1：設計與合約

_前置條件：research.md 完成_

1. **從功能規格中提取實體** → `data-model.md`：

   - 實體名稱、欄位、關係
   - 來自需求的驗證規則
   - 狀態轉換（如果適用）

2. **從功能需求產生 API 合約**：

   - 每個使用者動作 → 端點
   - 使用標準 REST/GraphQL 模式
   - 輸出 OpenAPI/GraphQL 架構到 `/contracts/`

3. **從合約產生合約測試**：

   - 每個端點一個測試檔案
   - 斷言請求/回應架構
   - 測試必須失敗（尚未實作）

4. **從使用者故事中提取測試情境**：

   - 每個故事 → 整合測試情境
   - 快速開始測試 = 故事驗證步驟

5. **增量更新代理程式檔案**（O(1) 操作）：
   - 為你的 AI 助理執行 `/scripts/update-agent-context.sh [claude|gemini|copilot]`
   - 如果存在：僅從當前計畫新增新技術
   - 保留標記之間的手動新增內容
   - 更新最近變更（保留最後 3 個）
   - 保持在 150 行以下以提高 token 效率
   - 輸出到儲存庫根目錄

**輸出**：data-model.md、/contracts/\*、失敗的測試、quickstart.md、代理程式特定檔案

## 階段 2：任務規劃方法

_此章節描述 /tasks 指令將執行的內容 - 在 /plan 期間不要執行_

**任務產生策略**：

- 載入 `/templates/tasks-template.md` 作為基礎
- 從階段 1 設計文件（合約、資料模型、快速開始）產生任務
- 每個合約 → 合約測試任務 [P]
- 每個實體 → 模型建立任務 [P]
- 每個使用者故事 → 整合測試任務
- 實作任務以使測試通過

**排序策略**：

- TDD 順序：測試在實作之前
- 相依性順序：模型在服務之前，服務在 UI 之前
- 標記 [P] 用於平行執行（獨立檔案）

**預估輸出**：tasks.md 中 25-30 個編號、有序的任務

**重要**：此階段由 /tasks 指令執行，不是由 /plan 執行

## 階段 3+：未來實作

_這些階段超出 /plan 指令的範圍_

**階段 3**：任務執行（/tasks 指令建立 tasks.md）  
**階段 4**：實作（遵循憲法原則執行 tasks.md）  
**階段 5**：驗證（執行測試、執行 quickstart.md、效能驗證）

## 複雜度追蹤

_僅在憲法檢查有必須證明合理性的違規時填寫_

| 違規                   | 為什麼需要 | 拒絕更簡單替代方案的原因   |
| ---------------------- | ---------- | -------------------------- |
| [例如第 4 個專案]      | [當前需求] | [為什麼 3 個專案不足]      |
| [例如 Repository 模式] | [特定問題] | [為什麼直接資料庫存取不足] |

## 進度追蹤

_此檢查清單在執行流程期間更新_

**階段狀態**：

- [ ] 階段 0：研究完成（/plan 指令）
- [ ] 階段 1：設計完成（/plan 指令）
- [ ] 階段 2：任務規劃完成（/plan 指令 - 僅描述方法）
- [ ] 階段 3：任務已產生（/tasks 指令）
- [ ] 階段 4：實作完成
- [ ] 階段 5：驗證通過

**閘門狀態**：

- [ ] 初始憲法檢查：通過
- [ ] 設計後憲法檢查：通過
- [ ] 所有 NEEDS CLARIFICATION 已解決
- [ ] 複雜度偏差已記錄

---

_基於憲法 v2.1.1 - 參見 `/memory/constitution.md`_
