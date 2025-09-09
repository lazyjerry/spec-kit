# 任務：[FEATURE NAME]

**輸入**：來自 `/specs/[###-feature-name]/` 的設計文件
**前置條件**：plan.md（必需）、research.md、data-model.md、contracts/

## 執行流程（main）

```
1. 從功能目錄載入 plan.md
   → 如果找不到：錯誤 "找不到實作計畫"
   → 提取：技術堆疊、函式庫、結構
2. 載入選用設計文件：
   → data-model.md：提取實體 → 模型任務
   → contracts/：每個檔案 → 合約測試任務
   → research.md：提取決策 → 設定任務
3. 按類別產生任務：
   → 設定：專案初始化、相依性、程式碼檢查
   → 測試：合約測試、整合測試
   → 核心：模型、服務、CLI 指令
   → 整合：資料庫、中介軟體、日誌記錄
   → 完善：單元測試、效能、文件
4. 套用任務規則：
   → 不同檔案 = 標記 [P] 為平行
   → 相同檔案 = 循序（無 [P]）
   → 測試在實作之前（TDD）
5. 循序編號任務（T001、T002...）
6. 產生相依性圖表
7. 建立平行執行範例
8. 驗證任務完整性：
   → 所有合約都有測試？
   → 所有實體都有模型？
   → 所有端點都已實作？
9. 回傳：成功（任務準備執行）
```

## 格式：`[ID] [P?] Description`

- **[P]**：可以平行執行（不同檔案，無相依性）
- 在描述中包含確切的檔案路徑

## 路徑慣例

- **單一專案**：儲存庫根目錄的 `src/`、`tests/`
- **Web 應用程式**：`backend/src/`、`frontend/src/`
- **行動裝置**：`api/src/`、`ios/src/` 或 `android/src/`
- 下方顯示的路徑假設為單一專案 - 根據 plan.md 結構調整

## 階段 3.1：設定

- [ ] T001 根據實作計畫建立專案結構
- [ ] T002 使用 [framework] 相依性初始化 [language] 專案
- [ ] T003 [P] 設定程式碼檢查和格式化工具

## 階段 3.2：測試優先（TDD）⚠️ 必須在 3.3 之前完成

**關鍵：這些測試必須在任何實作之前撰寫且必須失敗**

- [ ] T004 [P] 在 tests/contract/test_users_post.py 中進行 POST /api/users 合約測試
- [ ] T005 [P] 在 tests/contract/test_users_get.py 中進行 GET /api/users/{id} 合約測試
- [ ] T006 [P] 在 tests/integration/test_registration.py 中進行使用者註冊整合測試
- [ ] T007 [P] 在 tests/integration/test_auth.py 中進行驗證流程整合測試

## 階段 3.3：核心實作（僅在測試失敗後）

- [ ] T008 [P] 在 src/models/user.py 中建立使用者模型
- [ ] T009 [P] 在 src/services/user_service.py 中建立 UserService CRUD
- [ ] T010 [P] 在 src/cli/user_commands.py 中建立 CLI --create-user
- [ ] T011 POST /api/users 端點
- [ ] T012 GET /api/users/{id} 端點
- [ ] T013 輸入驗證
- [ ] T014 錯誤處理和日誌記錄

## 階段 3.4：整合

- [ ] T015 將 UserService 連接到資料庫
- [ ] T016 驗證中介軟體
- [ ] T017 請求/回應日誌記錄
- [ ] T018 CORS 和安全標頭

## 階段 3.5：完善

- [ ] T019 [P] 在 tests/unit/test_validation.py 中進行驗證的單元測試
- [ ] T020 效能測試（<200ms）
- [ ] T021 [P] 更新 docs/api.md
- [ ] T022 移除重複
- [ ] T023 執行 manual-testing.md

## 相依性

- 測試（T004-T007）在實作（T008-T014）之前
- T008 阻擋 T009、T015
- T016 阻擋 T018
- 實作在完善（T019-T023）之前

## 平行執行範例

```
# 一起啟動 T004-T007：
任務：「在 tests/contract/test_users_post.py 中進行 POST /api/users 合約測試」
任務：「在 tests/contract/test_users_get.py 中進行 GET /api/users/{id} 合約測試」
任務：「在 tests/integration/test_registration.py 中進行註冊整合測試」
任務：「在 tests/integration/test_auth.py 中進行驗證整合測試」
```

## 注意事項

- [P] 任務 = 不同檔案，無相依性
- 在實作之前驗證測試失敗
- 每個任務後提交
- 避免：模糊任務、相同檔案衝突

## 任務產生規則

_在 main() 執行期間套用_

1. **來自合約**：
   - 每個合約檔案 → 合約測試任務 [P]
   - 每個端點 → 實作任務
2. **來自資料模型**：
   - 每個實體 → 模型建立任務 [P]
   - 關係 → 服務層任務
3. **來自使用者故事**：

   - 每個故事 → 整合測試 [P]
   - 快速開始情境 → 驗證任務

4. **排序**：
   - 設定 → 測試 → 模型 → 服務 → 端點 → 完善
   - 相依性阻擋平行執行

## 驗證檢查清單

_閘門：在回傳之前由 main() 檢查_

- [ ] 所有合約都有對應的測試
- [ ] 所有實體都有模型任務
- [ ] 所有測試都在實作之前
- [ ] 平行任務真正獨立
- [ ] 每個任務都指定確切的檔案路徑
- [ ] 沒有任務修改與另一個 [P] 任務相同的檔案
