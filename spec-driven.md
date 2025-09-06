# 規格驅動開發 (SDD)

## 權力倒轉

數十年來，程式碼一直是王道。規格為程式碼服務——它們是我們建構的鷹架，一旦「真正的」編碼工作開始就會被丟棄。我們撰寫 PRD 來指導開發，建立設計文件來告知實作，繪製圖表來視覺化架構。但這些總是從屬於程式碼本身。程式碼就是真理。其他一切充其量只是良好的意圖。程式碼是真相的來源，隨著它向前推進，規格很少能跟上步調。由於資產（程式碼）和實作是一體的，在不嘗試從程式碼建構的情況下，很難有平行實作。

規格驅動開發 (SDD) 顛覆了這種權力結構。規格不為程式碼服務——程式碼為規格服務。產品需求文件規格 (PRD) 不是實作的指南；它是產生實作的來源。技術計畫不是告知編碼的文件；它們是產生程式碼的精確定義。這不是我們建構軟體方式的漸進式改進。這是對驅動開發的根本重新思考。

規格與實作之間的差距自軟體開發誕生以來就一直困擾著它。我們試圖透過更好的文件、更詳細的需求、更嚴格的流程來彌合這個差距。這些方法失敗是因為它們接受差距是不可避免的。它們試圖縮小差距但從未消除它。SDD 透過讓規格或從規格誕生的具體實作計畫變得可執行來消除差距。當規格到實作計畫產生程式碼時，就沒有差距——只有轉換。

這種轉換現在成為可能，因為 AI 能夠理解和實作複雜的規格，並建立詳細的實作計畫。但沒有結構的原始 AI 生成會產生混亂。SDD 透過足夠精確、完整且明確的規格和後續實作計畫來提供這種結構，以產生可運作的系統。規格成為主要工件。程式碼成為它在特定語言和框架中的表達（作為實作計畫的實作）。

在這個新世界中，維護軟體意味著演進規格。開發團隊的意圖以自然語言（「**意圖驅動開發**」）、設計資產、核心原則和其他指導方針來表達。開發的 **通用語言** 移向更高層次，程式碼是最後一哩路的方法。

除錯意味著修復產生錯誤程式碼的規格和其實作計畫。重構意味著為了清晰度而重新結構化。整個開發工作流程圍繞規格作為中央真相來源重新組織，實作計畫和程式碼作為持續重新生成的輸出。因為我們是有創造力的存在，用新功能更新應用程式或建立新的平行實作，意味著重新審視規格並建立新的實作計畫。因此這個過程是 0 -> 1, (1', ..), 2, 3, N。

開發團隊專注於他們的創造力、實驗和批判性思考。

## SDD 工作流程實務

工作流程從一個想法開始——通常是模糊且不完整的。透過與 AI 的迭代對話，這個想法變成一個全面的 PRD。AI 提出澄清問題，識別邊緣情況，並協助定義精確的接受標準。在傳統開發中可能需要數天會議和文件工作的事情，在專注的規格工作中幾小時就能完成。這轉換了傳統的 SDLC——需求和設計變成持續的活動而非離散的階段。這支援 **團隊流程**，即團隊審查的規格被表達和版本化，在分支中建立並合併。

當產品經理更新接受標準時，實作計畫會自動標記受影響的技術決策。當架構師發現更好的模式時，PRD 會更新以反映新的可能性。

在整個規格流程中，研究代理程式收集關鍵背景資訊。它們調查函式庫相容性、效能基準和安全性影響。組織限制被自動發現和應用——你公司的資料庫標準、驗證需求和部署政策無縫整合到每個規格中。

從 PRD 開始，AI 產生將需求對應到技術決策的實作計畫。每個技術選擇都有記錄的理由。每個架構決策都可追溯到特定需求。在整個過程中，一致性驗證持續改善品質。AI 分析規格的模糊性、矛盾和差距——不是作為一次性的關卡，而是作為持續的精煉。

程式碼生成在規格和其實作計畫足夠穩定時就開始，但它們不必是「完整的」。早期生成可能是探索性的——測試規格在實務上是否合理。領域概念變成資料模型。使用者故事變成 API 端點。接受情境變成測試。這透過規格合併開發和測試——測試情境不是在程式碼之後撰寫，它們是產生實作和測試的規格的一部分。

回饋迴圈延伸到初始開發之外。生產指標和事件不只是觸發熱修復——它們為下一次重新生成更新規格。效能瓶頸變成新的非功能需求。安全性漏洞變成影響所有未來生成的限制。規格、實作和營運現實之間的這種迭代舞蹈是真正理解出現的地方，也是傳統 SDLC 轉換為持續演進的地方。

## 為什麼 SDD 現在很重要

三個趨勢讓 SDD 不僅成為可能，而且是必要的：

首先，AI 能力已達到自然語言規格可以可靠地產生可運作程式碼的門檻。這不是要取代開發者——而是透過自動化從規格到實作的機械性翻譯來放大他們的效能。它可以放大探索和創造力，可以輕鬆支援「重新開始」，支援加法減法和批判性思考。

其次，軟體複雜性持續指數級增長。現代系統整合數十個服務、框架和相依性。透過手動流程讓所有這些部分與原始意圖保持一致變得越來越困難。SDD 透過規格驅動生成提供系統性對齊。框架可能演進為提供 AI 優先支援，而非人類優先支援，或圍繞可重用元件進行架構。

第三，變化的步調加速。今天的需求變化比以往任何時候都更快速。轉向不再是例外——而是預期的。現代產品開發要求基於使用者回饋、市場條件和競爭壓力的快速迭代。傳統開發將這些變化視為干擾。每次轉向都需要手動將變化傳播到文件、設計和程式碼中。結果要麼是限制速度的緩慢、謹慎更新，要麼是累積技術債務的快速、魯莽變化。

SDD 可以支援假設/模擬實驗，「如果我們需要重新實作或變更應用程式以促進銷售更多 T 恤的商業需求，我們會如何實作和實驗？」。

SDD 將需求變化從障礙轉換為正常工作流程。當規格驅動實作時，轉向變成系統性重新生成而非手動重寫。變更 PRD 中的核心需求，受影響的實作計畫會自動更新。修改使用者故事，對應的 API 端點會重新生成。這不僅關於初始開發——而是關於透過不可避免的變化維持工程速度。

## 核心原則

**規格作為通用語言**：規格成為主要工件。程式碼成為它在特定語言和框架中的表達。維護軟體意味著演進規格。

**可執行規格**：規格必須足夠精確、完整且明確，以產生可運作的系統。這消除了意圖與實作之間的差距。

**持續精煉**：一致性驗證持續進行，而非作為一次性關卡。AI 分析規格的模糊性、矛盾和差距作為持續過程。

**研究驅動背景**：研究代理程式在整個規格過程中收集關鍵背景資訊，調查技術選項、效能影響和組織限制。

**雙向回饋**：生產現實告知規格演進。指標、事件和營運學習成為規格精煉的輸入。

**分支探索**：從同一規格產生多種實作方法，以探索不同的最佳化目標——效能、可維護性、使用者體驗、成本。

## 實作方法

今天，實踐 SDD 需要組合現有工具並在整個過程中保持紀律。該方法論可以透過以下方式實踐：

- 用於迭代規格開發的 AI 助理
- 用於收集技術背景的研究代理程式
- 用於將規格翻譯為實作的程式碼生成工具
- 適應規格優先工作流程的版本控制系統
- 透過 AI 分析規格文件的一致性檢查

關鍵是將規格視為真相來源，程式碼作為服務規格的生成輸出，而非相反。

## 使用 Claude 指令簡化 SDD

SDD 方法論透過兩個強大的 Claude 指令得到顯著增強，這些指令自動化規格和規劃工作流程：

### `new_feature` 指令

此指令將簡單的功能描述（使用者提示）轉換為完整、結構化的規格，並自動管理儲存庫：

1. **自動功能編號**：掃描現有規格以確定下一個功能編號（例如 001、002、003）
2. **分支建立**：從你的描述產生語義分支名稱並自動建立
3. **基於範本的生成**：複製並使用你的需求自訂功能規格範本
4. **目錄結構**：為所有相關文件建立適當的 `specs/[branch-name]/` 結構

### `generate_plan` 指令

一旦功能規格存在，此指令會建立全面的實作計畫：

1. **規格分析**：讀取並理解功能需求、使用者故事和接受標準
2. **憲法合規**：確保與專案憲法和架構原則一致
3. **技術翻譯**：將商業需求轉換為技術架構和實作細節
4. **詳細文件**：為資料模型、API 合約和測試情境產生支援文件
5. **手動測試計畫**：為每個使用者故事建立逐步驗證程序

### 範例：建構聊天功能

以下是這些指令如何轉換傳統開發工作流程：

**傳統方法：**

```
1. 在文件中撰寫 PRD（2-3 小時）
2. 建立設計文件（2-3 小時）
3. 手動設定專案結構（30 分鐘）
4. 撰寫技術規格（3-4 小時）
5. 建立測試計畫（2 小時）
總計：約 12 小時的文件工作
```

**使用指令的 SDD 方法：**

```bash
# 步驟 1：建立功能規格（5 分鐘）
/new_feature Real-time chat system with message history and user presence

# 這會自動：
# - 建立分支 "003-chat-system"
# - 產生 specs/003-chat-system/feature-spec.md
# - 用結構化需求填充它

# 步驟 2：產生實作計畫（10 分鐘）
/generate_plan WebSocket for real-time messaging, PostgreSQL for history, Redis for presence

# 這會自動建立：
# - specs/003-chat-system/implementation-plan.md
# - specs/003-chat-system/implementation-details/
#   - 00-research.md (WebSocket 函式庫比較)
#   - 02-data-model.md (訊息和使用者架構)
#   - 03-api-contracts.md (WebSocket 事件、REST 端點)
#   - 06-contract-tests.md (Message flow scenarios)
#   - 08-inter-library-tests.md (Database-WebSocket integration)
# - specs/003-chat-system/manual-testing.md
```

在 15 分鐘內，你擁有：

- 包含使用者故事和接受標準的完整功能規格
- 包含技術選擇和理由的詳細實作計畫
- 準備好進行程式碼生成的 API 合約和資料模型
- 自動化和手動測試的全面測試情境
- 在功能分支中適當版本化的所有文件

### 結構化自動化的力量

這些指令不僅節省時間——它們強制執行一致性和完整性：

1. **沒有遺忘的細節**：範本確保考慮每個方面，從非功能需求到錯誤處理
2. **可追溯的決策**：每個技術選擇都連結回特定需求
3. **活文件**：規格與程式碼保持同步，因為它們產生程式碼
4. **快速迭代**：在幾分鐘而非幾天內變更需求並重新生成計畫

這些指令透過將規格視為可執行工件而非靜態文件來體現 SDD 原則。它們將規格流程從必要之惡轉換為開發的驅動力。

### 範本驅動品質：結構如何約束 LLM 以獲得更好的結果

這些指令的真正力量不僅在於自動化，還在於範本如何引導 LLM 行為朝向更高品質的規格。範本作為複雜的提示，以有效的方式約束 LLM 的輸出：

#### 1. **Preventing Premature Implementation Details**

The feature specification template explicitly instructs:

```
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
```

This constraint forces the LLM to maintain proper abstraction levels. When an LLM might naturally jump to "implement using React with Redux," the template keeps it focused on "users need real-time updates of their data." This separation ensures specifications remain stable even as implementation technologies change.

#### 2. **Forcing Explicit Uncertainty Markers**

Both templates mandate the use of `[NEEDS CLARIFICATION]` markers:

```
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question]
2. **Don't guess**: If the prompt doesn't specify something, mark it
```

This prevents the common LLM behavior of making plausible but potentially incorrect assumptions. Instead of guessing that a "login system" uses email/password authentication, the LLM must mark it as `[NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]`.

#### 3. **Structured Thinking Through Checklists**

The templates include comprehensive checklists that act as "unit tests" for the specification:

```
### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
```

These checklists force the LLM to self-review its output systematically, catching gaps that might otherwise slip through. It's like giving the LLM a quality assurance framework.

#### 4. **Constitutional Compliance Through Gates**

The implementation plan template enforces architectural principles through phase gates:

```
### Phase -1: Pre-Implementation Gates
#### Simplicity Gate (Article VII)
- [ ] Using ≤3 projects?
- [ ] No future-proofing?
#### Anti-Abstraction Gate (Article VIII)
- [ ] Using framework directly?
- [ ] Single model representation?
```

These gates prevent over-engineering by making the LLM explicitly justify any complexity. If a gate fails, the LLM must document why in the "Complexity Tracking" section, creating accountability for architectural decisions.

#### 5. **Hierarchical Detail Management**

The templates enforce proper information architecture:

```
**IMPORTANT**: This implementation plan should remain high-level and readable.
Any code samples, detailed algorithms, or extensive technical specifications
must be placed in the appropriate `implementation-details/` file
```

This prevents the common problem of specifications becoming unreadable code dumps. The LLM learns to maintain appropriate detail levels, extracting complexity to separate files while keeping the main document navigable.

#### 6. **Test-First Thinking**

The implementation template enforces test-first development:

```
### File Creation Order
1. Create `contracts/` with API specifications
2. Create test files in order: contract → integration → e2e → unit
3. Create source files to make tests pass
```

This ordering constraint ensures the LLM thinks about testability and contracts before implementation, leading to more robust and verifiable specifications.

#### 7. **Preventing Speculative Features**

Templates explicitly discourage speculation:

```
- [ ] No speculative or "might need" features
- [ ] All phases have clear prerequisites and deliverables
```

This stops the LLM from adding "nice to have" features that complicate implementation. Every feature must trace back to a concrete user story with clear acceptance criteria.

### The Compound Effect

These constraints work together to produce specifications that are:

- **Complete**: Checklists ensure nothing is forgotten
- **Unambiguous**: Forced clarification markers highlight uncertainties
- **Testable**: Test-first thinking baked into the process
- **Maintainable**: Proper abstraction levels and information hierarchy
- **Implementable**: Clear phases with concrete deliverables

The templates transform the LLM from a creative writer into a disciplined specification engineer, channeling its capabilities toward producing consistently high-quality, executable specifications that truly drive development.

## The Constitutional Foundation: Enforcing Architectural Discipline

At the heart of SDD lies a constitution—a set of immutable principles that govern how specifications become code. The constitution (`base/memory/constitution.md`) acts as the architectural DNA of the system, ensuring that every generated implementation maintains consistency, simplicity, and quality.

### The Nine Articles of Development

The constitution defines nine articles that shape every aspect of the development process:

#### Article I: Library-First Principle

Every feature must begin as a standalone library—no exceptions. This forces modular design from the start:

```
Every feature in Specify MUST begin its existence as a standalone library.
No feature shall be implemented directly within application code without
first being abstracted into a reusable library component.
```

This principle ensures that specifications generate modular, reusable code rather than monolithic applications. When the LLM generates an implementation plan, it must structure features as libraries with clear boundaries and minimal dependencies.

#### Article II: CLI Interface Mandate

Every library must expose its functionality through a command-line interface:

```
All CLI interfaces MUST:
- Accept text as input (via stdin, arguments, or files)
- Produce text as output (via stdout)
- Support JSON format for structured data exchange
```

This enforces observability and testability. The LLM cannot hide functionality inside opaque classes—everything must be accessible and verifiable through text-based interfaces.

#### Article III: Test-First Imperative

The most transformative article—no code before tests:

```
This is NON-NEGOTIABLE: All implementation MUST follow strict Test-Driven Development.
No implementation code shall be written before:
1. Unit tests are written
2. Tests are validated and approved by the user
3. Tests are confirmed to FAIL (Red phase)
```

This completely inverts traditional AI code generation. Instead of generating code and hoping it works, the LLM must first generate comprehensive tests that define behavior, get them approved, and only then generate implementation.

#### Articles VII & VIII: Simplicity and Anti-Abstraction

These paired articles combat over-engineering:

```
Section 7.3: Minimal Project Structure
- Maximum 3 projects for initial implementation
- Additional projects require documented justification

Section 8.1: Framework Trust
- Use framework features directly rather than wrapping them
```

When an LLM might naturally create elaborate abstractions, these articles force it to justify every layer of complexity. The implementation plan template's "Phase -1 Gates" directly enforce these principles.

#### Article IX: Integration-First Testing

Prioritizes real-world testing over isolated unit tests:

```
Tests MUST use realistic environments:
- Prefer real databases over mocks
- Use actual service instances over stubs
- Contract tests mandatory before implementation
```

This ensures generated code works in practice, not just in theory.

### Constitutional Enforcement Through Templates

The implementation plan template operationalizes these articles through concrete checkpoints:

```markdown
### Phase -1: Pre-Implementation Gates

#### Simplicity Gate (Article VII)

- [ ] Using ≤3 projects?
- [ ] No future-proofing?

#### Anti-Abstraction Gate (Article VIII)

- [ ] Using framework directly?
- [ ] Single model representation?

#### Integration-First Gate (Article IX)

- [ ] Contracts defined?
- [ ] Contract tests written?
```

These gates act as compile-time checks for architectural principles. The LLM cannot proceed without either passing the gates or documenting justified exceptions in the "Complexity Tracking" section.

### 不可變原則的力量

憲法的力量在於其不可變性。雖然實作細節可以演進，但核心原則保持不變。這提供：

1. **跨時間一致性**：今天生成的程式碼遵循與明年生成的程式碼相同的原則
2. **跨 LLM 一致性**：不同的 AI 模型產生架構相容的程式碼
3. **架構完整性**：每個功能都強化而非破壞系統設計
4. **品質保證**：測試優先、函式庫優先和簡潔原則確保可維護的程式碼

### Constitutional Evolution

While principles are immutable, their application can evolve:

```
Section 4.2: Amendment Process
Modifications to this constitution require:
- Explicit documentation of the rationale for change
- Review and approval by project maintainers
- Backwards compatibility assessment
```

This allows the methodology to learn and improve while maintaining stability. The constitution shows its own evolution with dated amendments, demonstrating how principles can be refined based on real-world experience.

### Beyond Rules: A Development Philosophy

The constitution isn't just a rulebook—it's a philosophy that shapes how LLMs think about code generation:

- **Observability Over Opacity**: Everything must be inspectable through CLI interfaces
- **Simplicity Over Cleverness**: Start simple, add complexity only when proven necessary
- **Integration Over Isolation**: Test in real environments, not artificial ones
- **Modularity Over Monoliths**: Every feature is a library with clear boundaries

By embedding these principles into the specification and planning process, SDD ensures that generated code isn't just functional—it's maintainable, testable, and architecturally sound. The constitution transforms AI from a code generator into an architectural partner that respects and reinforces system design principles.

## 轉換

這不是要取代開發者或自動化創造力。而是透過自動化機械性翻譯來放大人類能力。這是關於建立一個緊密的回饋迴圈，其中規格、研究和程式碼一起演進，每次迭代都帶來更深的理解和意圖與實作之間更好的對齊。

軟體開發需要更好的工具來維持意圖與實作之間的對齊。SDD 提供透過產生程式碼而非僅僅指導程式碼的可執行規格來實現這種對齊的方法論。
