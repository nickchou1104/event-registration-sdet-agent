# QA-Assignment-Event-Registration
此專案為「活動報名表單」的測試自動化與 QA 工程師作業交付內容。專案涵蓋了由 AI 生成之前端待測系統，以及完整的規格審查、測試案例設計、缺陷報告與 Agent 自動化工作流。

## 專案目錄結構
*   `src/index.html`: Part A - AI 生成之待測前端程式碼
*   `prompts/prompt_history.md`: Part A - AI 提示詞與生成歷程紀錄
*   `ai_agents/`: 自動化 Agent 工作流腳本 (引擎 0 ~ 4)
*   `docs/B1_Spec_Review.md`: Part B1 - 規格審查報告 (產出檔支援 `_v1`, `_v2` 動態流水號避覆蓋)
*   `docs/B2_Test_Cases.md`: Part B2 - 測試案例設計 (涵蓋正向、負向、邊界與異常)
*   `docs/B3_Bug_Reports.md`: Part B3 - 缺陷報告 (Bug Reports)
*   `docs/C_Reflection.md`: Part C - AI 協作反思與風險評估

---

## 專案目錄結構樹 (SDET Agent Architecture)

```text
Event-Registration-SDET-Architecture/
├── src/
│   └── index.html                           # Part A: AI 生成的前端待測程式碼
├── prompts/
│   └── prompt_history_v1.md                 # 引擎零自動逆向生成的 Prompt 歷史檔案
├── ai_agents/ (SDET 自動化測試代理引擎)
│   ├── run_pipeline.py                      # 總協調主控腳本 (一鍵自動執行 0 ~ 4 號引擎)
│   ├── generate_prompt_history.py           # 引擎零：逆向分析 index.html 並自動產出 Prompt 歷史
│   ├── extract_specs_to_feature.py          # 引擎一：處理 B1 規格審查與萃取測試重點
│   ├── generate_qase_bdd.py                 # 引擎二：處理 B2 生成測試案例並打 API 上傳 Qase
│   ├── validate_and_report.py               # 引擎三：靜態程式碼審查並自動產生 Bug 報告
│   ├── generate_reflection.py               # 引擎四：自動對比需求與 Bug，產出 C_Reflection 反思報告
│   ├── qase_style.md                        # 規範定義：Qase 欄位對映與 BDD 撰寫標準
│   └── pending_specs/                       # 進件區
│       ├── 測試工程師作業.pdf                # 原始需求文件
│       └── feature.md                       # 規格精煉後的作業需求檔
├── docs/ (作業交付文件，生成檔自動儲存為 _v1, _v2...)
│   ├── B1_Spec_Review.md                    # Part B1: 規格審查報告
│   ├── B2_Test_Cases.md                     # Part B2: BDD 測試案例設計
│   ├── B3_Bug_Reports.md                    # Part B3: 缺陷報告
│   └── C_Reflection.md                      # Part C: AI 協作反思
└── README.md                                # 專案總結與自動化指令說明


## Agent 架構互動流程圖 (Data Flow & Architecture)
```text
                   +---------------------------------------------+
                   |   ai_agents/run_pipeline.py (一鍵自動化主控)  |
                   +---------------------+-----------------------+
                                         | 依序調用引擎 (0 ~ 4)
                                         v
                   +-----------------------------+
                   |  src/index.html (待測前端)   |
                   +--------------+--------------+
                                  |
                                  v
             [ 引擎零: generate_prompt_history.py ]
                                  |
                                  v
                 prompts/prompt_history_vX.md
                                  |
                                  v
                   +-----------------------------+
                   |  測試工程師作業.pdf (原始需求) |
                   +--------------+--------------+
                                  |
                                  v
             [ 引擎一: extract_specs_to_feature.py ]
                                  |
                         +--------+--------+
                         |                 |
                         v                 v
           docs/B1_Spec_Review_vX.md   pending_specs/feature.md (精煉規格)
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
[ 引擎二: generate_qase_bdd.py ]            [ 引擎三: validate_and_report.py ]
 (參照 ai_agents/qase_style.md)                              ^
      |                        \                            | (靜態比對)
      v                         v                           |
docs/B2_Test_Cases_vX.md    Qase.io API               src/index.html (待測系統)
                            (同步雲端案例)                    |
                                                            v
                                            docs/B3_Bug_Reports_vX.md
                                                            |
                   +----------------------------------------+
                   | (讀取 B1 + B3 + index.html 上下文)
                   v
[ 引擎四: generate_reflection.py ]
                   |
                   v
        docs/C_Reflection_vX.md
```

## 自動化工作流執行指令 (LLM -> BDD 順序)
**0. 逆向分析前端程式碼，自動生成 Prompt 歷史紀錄**
```bash
python3 ai_agents/generate_prompt_history.py

**1. 提煉規格與 B1 審查**
```bash
python3 ai_agents/extract_specs_to_feature.py

**2. 生成 BDD 案例並同步至 Qase**
```bash
python3 ai_agents/generate_qase_bdd.py

**3. 靜態程式碼審查並自動產生 Bug Report**
```bash
python3 ai_agents/validate_and_report.py

**4. 深度對比需求與 Bug，自動生成 AI 協作反思報告**
```bash
python3 ai_agents/generate_reflection.py

**一鍵自動化執行**
```bash
python3 ai_agents/run_pipeline.py


## 如何執行待測系統
1. 進入 `src` 目錄。
2. 使用任一瀏覽器 (如 Chrome, Safari) 直接開啟 `index.html` 檔案。
3. 即可開始依照 `B2_Test_Cases.md` 進行手動測試比對。

## 實際花費時間總結
*   Part A (AI 詠唱與環境建置): 約 0.5 小時
*   Part B (規格審查、案例設計與抓蟲): 約 1.5 小時
*   Part C (反思撰寫與專案收尾): 約 1.0 小時
*   **總計花費時間: 約 3 小時**


<!-- # Automation
[ B2 測試案例 (BDD) ]
       ↓ (AI 腳本生成 Agent)
[ 生成 Playwright / Cypress 測試程式碼 (e2e.spec.ts) ]
       ↓ (CLI 執行)
[ 啟動 Headless 瀏覽器 (Chromium) 實機點擊輸入與斷言 ]
       ↓ (測試結果 Logs / Screenshots)
[ AI 讀取 Fail Log 產出最終測試執行報告 ] --> -->