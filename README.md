# AI-News-Monitor-Pipeline
自動化新聞監測管線：整合 Google News 爬蟲、Selenium 動態渲染、LLM 審核，並自動產出 Excel 報表寄 Email 。
# AI News Monitor Pipeline

這是一個基於 Python 開發的自動化新聞監測工具。系統會根據指定的關鍵字擷取 Google News 報導，透過本地端大語言模型 (LLM) 判斷內容關聯性並生成摘要，最後匯出 Excel 報表並透過電子郵件發送。

## 功能說明

* **新聞擷取**：整合 `pygooglenews` 與 `newspaper3k`，並備用 `Selenium` 處理需要動態渲染的網頁內文。
* **AI 內容審核**：串接本地端 LLM (如 LM Studio)，依據自訂的 Prompt 規則篩選新聞，排除不相關的報導。
* **資料匯出**：將符合條件的資料結構化，按狀態排序後匯出為 Excel (`.xlsx`) 檔案。
* **郵件通知**：透過 SMTP 伺服器，自動將生成的 Excel 報表作為附件寄送至指定信箱。
* **參數化設定**：將搜尋條件、API 網址、Prompt 與機密資訊獨立存放，便於修改與維護。

## 專案架構

```text
├── .env                  # 存放 Email 帳號與應用程式密碼 (請勿上傳至版本控制)
├── config.json           # 搜尋關鍵字、天數與 API 參數設定
├── system_prompt.txt     # 提供給 LLM 的系統提示詞
├── main.py               # 主程式執行入口
└── src/
    ├── __init__.py
    ├── scraper.py        # 負責新聞連結檢索與內文擷取
    ├── analyzer.py       # 負責 LLM API 呼叫與 JSON 解析
    ├── formatter.py      # 負責 Pandas 資料處理與 Excel 輸出
    └── mailer.py         # 負責構建與發送電子郵件
