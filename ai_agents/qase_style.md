# 聊天室字數優化需求
新增功能：當用戶在 Minikorn 聊天室的輸入欄位中，連續輸入文字並主動按下「換行」時，系統的字數計算必須正確，且換行符號需要被當成字數正確計算，不能造成 App 閃退。

---

# Qase.io 測試案例 (Test Case) 規格與撰寫規範
本文件旨在定義團隊於 Qase.io 建立與維護自動化/手動測試案例的標準規格，確保 AI 生成及人工撰寫的格式一致，便於後續自動化腳本的串接與執行。

## 1. 目錄架構 (Suites)
測試案例應依據功能模組妥善分類，確保測試庫整潔。Suite 應建立在專案特定的目錄下。

## 2. 測試案例基本欄位 (Basic Fields)
依據 Qase API 系統規範，建立案例時需填寫以下核心屬性。請注意：API 僅接受「數字代碼」，請嚴格輸出對應的數字：

| 欄位名稱 (Field) | 說明與規範 (Description & Rules) | API 允許的數字代碼 (Allowed API Values) |
| :--- | :--- | :--- |
| **Title** (必填) | 簡明扼要地描述測試目的與預期結果。 | 例：`[功能] - [操作] - [預期結果]` |
| **Description** | 測試的 Feature 與 Scenario 描述。 | (AI 自動填寫，純前言描述) |
| **Suite** | 案例所屬的測試目錄。 | (由決策邏輯動態產出 suite_id) |
| **Status** | 測試案例的狀態。 | **`0`** (Actual), `1` (Draft), `2` (Deprecated) |
| **Severity** | 嚴重程度。 | `1` (Not set), `2` (Blocker), `3` (Critical), `4` (Major), `5` (Normal), `6` (Minor) |
| **Priority** | 優先級。 | `0` (Not set), `1` (High), `2` (Medium), `3` (Low) |
| **Type** | 測試類型。 | `1` (Other), **`2` (Functional)**, `3` (Smoke), `4` (Regression) |
| **Layer** | 測試所屬的架構層級。 | `0` (Not set), **`1` (E2E)**, `2` (API), `3` (Unit) |
| **Is flaky** | 是否為不穩定的測試。 | **`0`** (固定選擇 No) |
| **Behavior** | 測試行為。 | **`1`** (固定選擇 Not set) |
| **Automation status**| 自動化狀態。 | **`0`** (Manual), `1` (To be automated), `2` (Automated) |

## 3. 執行條件與標籤 (Conditions & Tags)
* **Pre-conditions / Post-conditions:** 依需求填寫（BDD 模式下可省略，直接寫入 Steps）。
* **Tags (標籤):** 用於標註適用的平台、環境或特定屬性。
    * **常用預設 Tags:** `iOS`, `Android`, `Server`, `Backend`, `Frontend`, `Web`, `H5`

## 4. 測試步驟 (Test Case Steps - BDD / Gherkin 模式)
為順利銜接自動化框架，測試步驟必須設定為 **`Gherkin`** 模式，並遵循 BDD 語法規範。

* **Given:** 定義初始狀態與前置條件。
* **When:** 觸發測試的核心操作動作。
* **Then:** 驗證預期結果與系統行為。
* **And / But:** 連接多個步驟。


### AI 自動化 JSON API 寫入格式規範
透過 API 自動寫入時，必須指定 `"steps_type": "gherkin"`，且所有狀態欄位必須為**數字 (Integer)**，並將步驟格式化為 JSON 陣列：
```json
{
  "title": "用戶貼文被點讚時收到桌面推播通知",
  "description": "Feature: 貼文點讚推播通知\nScenario: 當他人對我的貼文點讚時...",
  "suite_id": 123,
  "status": 0,
  "severity": 5,
  "priority": 2,
  "type": 2,
  "layer": 1,
  "is_flaky": 0,
  "behavior": 1,
  "automation": 0,
  "steps_type": "gherkin",
  "tags": ["iOS", "Android"],
  "steps": [
      {"action": "Given ..."},
      {"action": "When ..."},
      {"action": "Then ..."}
  ]
}
```
