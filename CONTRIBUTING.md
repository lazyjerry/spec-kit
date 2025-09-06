## 為 Spec Kit 做出貢獻

嗨！我們很高興你想要為 Spec Kit 做出貢獻。對此專案的貢獻會在 [專案的開源授權](LICENSE) 下 [發布](https://help.github.com/articles/github-terms-of-service/#6-contributions-under-repository-license) 給大眾。

請注意，此專案發布時附有 [貢獻者行為準則](CODE_OF_CONDUCT.md)。參與此專案即表示你同意遵守其條款。

## 執行和測試程式碼的前置需求

這些是一次性安裝，作為 pull request (PR) 提交流程的一部分，需要能夠在本地測試你的變更。

1. 安裝 [Python 3.11+](https://www.python.org/downloads/)
1. 安裝 [uv](https://docs.astral.sh/uv/) 用於套件管理
1. 安裝 [Git](https://git-scm.com/downloads)
1. 準備一個 AI 編碼代理程式：[Claude Code](https://www.anthropic.com/claude-code)、[GitHub Copilot](https://code.visualstudio.com/) 或 [Gemini CLI](https://github.com/google-gemini/gemini-cli)

## 提交 pull request

1. Fork 並複製儲存庫
1. 設定並安裝相依套件：`uv sync`
1. 確保 CLI 在你的機器上運作：`uv run specify --help`
1. 建立新分支：`git checkout -b my-branch-name`
1. 進行變更、新增測試，並確保一切仍正常運作
1. 如果相關，請使用範例專案測試 CLI 功能
1. 推送到你的 fork 並提交 pull request
1. 等待你的 pull request 被審查和合併。

以下是一些可以增加你的 pull request 被接受機會的做法：

- 遵循專案的編碼慣例。
- 為新功能撰寫測試。
- 如果你的變更影響使用者面向的功能，請更新文件（`README.md`、`spec-driven.md`）。
- 盡可能保持你的變更專注。如果你想要進行多個彼此不相依的變更，請考慮將它們作為單獨的 pull request 提交。
- 撰寫 [良好的提交訊息](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)。
- 使用規格驅動開發工作流程測試你的變更，以確保相容性。

## 開發工作流程

在開發 spec-kit 時：

1. 在你選擇的編碼代理程式中使用 `specify` CLI 指令（`/specify`、`/plan`、`/tasks`）測試變更
2. 驗證 `templates/` 目錄中的範本是否正常運作
3. 測試 `scripts/` 目錄中的腳本功能
4. 如果進行重大流程變更，請確保記憶檔案（`memory/constitution.md`）已更新

## 資源

- [規格驅動開發方法論](./spec-driven.md)
- [如何為開源專案做出貢獻](https://opensource.guide/how-to-contribute/)
- [使用 Pull Request](https://help.github.com/articles/about-pull-requests/)
- [GitHub 說明](https://help.github.com)
