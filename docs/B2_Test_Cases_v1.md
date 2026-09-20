# 測試案例設計 (Test Cases)

### [TC-001] [正向] 填寫有效資料，選擇免費票且報名人數為 1，成功提交表單
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 使用者成功報名免費活動
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 所有必填欄位皆為空
  * When 使用者輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-002] [正向] 填寫有效資料，選擇付費票且報名人數為 1，總金額正確顯示 NT$500 並成功提交
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 使用者成功報名付費活動並驗證金額
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 使用者輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『付費票』
  * And 指定報名人數為『1』
  * Then 畫面即時顯示總金額『NT$500』
  * When 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-003] [正向] 填寫有效資料，選擇付費票且報名人數為 10，總金額正確顯示 NT$5000 並成功提交
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 使用者報名付費活動最大人數並驗證金額
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 使用者輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『付費票』
  * And 指定報名人數為『10』
  * Then 畫面即時顯示總金額『NT$5000』
  * When 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-004] [正向] 選擇付費票後，動態修改報名人數，總金額即時更新
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證付費票總金額的即時動態計算
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 選擇票種『付費票』
  * When 指定報名人數為『1』
  * Then 畫面即時顯示總金額『NT$500』
  * When 將報名人數修改為『5』
  * Then 畫面即時顯示總金額『NT$2500』

---
### [TC-005] [正向] 從免費票切換至付費票，總金額正確顯示並計算
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證票種切換後付費票金額的正確顯示
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 指定報名人數為『3』
  * And 選擇票種『免費票』
  * When 將票種切換為『付費票』
  * Then 畫面即時顯示總金額『NT$1500』

---
### [TC-006] [異常] 姓名欄位為空時提交表單，顯示必填錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證姓名欄位必填性
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 姓名欄位留空
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『姓名為必填』的錯誤訊息

---
### [TC-007] [異常] Email 欄位為空時提交表單，顯示必填錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證 Email 欄位必填性
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When Email 欄位留空
  * And 輸入姓名『測試者』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『Email 為必填』的錯誤訊息

---
### [TC-008] [異常] Email 欄位輸入無 '@' 符號的字串，顯示格式錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證 Email 格式必須包含 '@' 符號
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入 Email 『testexample.com』
  * And 輸入姓名『測試者』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『Email 格式不正確』的錯誤訊息

---
### [TC-009] [異常] Email 欄位輸入無網域的字串，顯示格式錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證 Email 格式必須包含有效網域
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入 Email 『test@.com』
  * And 輸入姓名『測試者』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『Email 格式不正確』的錯誤訊息

---
### [TC-010] [異常] 報名人數欄位為空時提交表單，顯示必填錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位必填性
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 報名人數欄位留空
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數為必填』的錯誤訊息

---
### [TC-011] [異常] 報名人數欄位輸入非數字字串，顯示格式錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位只接受數字
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『abc』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數格式不正確』的錯誤訊息

---
### [TC-012] [異常] 報名人數欄位輸入小數，顯示格式錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位不接受小數
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『1.5』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數格式不正確』的錯誤訊息

---
### [TC-013] [異常] 同時存在多個欄位驗證失敗，提交表單顯示所有錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證多個欄位同時驗證失敗時的錯誤訊息顯示
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 姓名欄位留空
  * And 輸入 Email 『invalid-email』
  * And 報名人數欄位留空
  * And 點擊『提交』按鈕
  * Then 系統顯示『姓名為必填』的錯誤訊息
  * And 系統顯示『Email 格式不正確』的錯誤訊息
  * And 系統顯示『報名人數為必填』的錯誤訊息

---
### [TC-014] [異常] 錯誤訊息顯示後，修正欄位為有效值，錯誤訊息自動消失
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證錯誤訊息的即時清除機制
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 姓名欄位留空並點擊『提交』按鈕
  * Then 系統顯示『姓名為必填』的錯誤訊息
  * When 使用者在姓名欄位輸入『有效姓名』
  * Then 『姓名為必填』的錯誤訊息自動消失

---
### [TC-015] [邊界] 姓名欄位輸入單一字元，成功提交表單
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證姓名欄位最小長度邊界
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入姓名『A』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-016] [邊界] 姓名欄位輸入包含特殊符號，成功提交表單
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證姓名欄位接受特殊符號
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入姓名『張三-李四'』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-017] [邊界] Email 欄位輸入最短有效格式，成功提交表單
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證 Email 欄位最短有效格式
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入 Email 『a@b.co』
  * And 輸入姓名『測試者』
  * And 選擇票種『免費票』
  * And 指定報名人數為『1』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-018] [邊界] 報名人數欄位輸入最小值 1，成功提交表單
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位最小值
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『1』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-019] [邊界] 報名人數欄位輸入最大值 10，成功提交表單
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位最大值
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『10』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名成功』訊息

---
### [TC-020] [邊界] 報名人數欄位輸入 0，顯示超出範圍錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位輸入小於最小值
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『0』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數必須介於 1 到 10 之間』的錯誤訊息

---
### [TC-021] [邊界] 報名人數欄位輸入 11，顯示超出範圍錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位輸入大於最大值
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『11』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數必須介於 1 到 10 之間』的錯誤訊息

---
### [TC-022] [邊界] 報名人數欄位輸入負數，顯示格式錯誤訊息
* **優先級 (Priority)**: Medium
* **嚴重程度 (Severity)**: Normal
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證報名人數欄位不接受負數
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入報名人數『-1』
  * And 輸入姓名『測試者』
  * And 輸入 Email 『test@example.com』
  * And 選擇票種『免費票』
  * And 點擊『提交』按鈕
  * Then 系統顯示『報名人數格式不正確』的錯誤訊息

---
### [TC-023] [狀態] 從付費票切換至免費票時，總金額顯示欄位立即隱藏
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證票種切換時總金額欄位的顯示狀態
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 選擇票種『付費票』
  * And 總金額顯示欄位可見
  * When 將票種切換為『免費票』
  * Then 總金額顯示欄位立即隱藏

---
### [TC-024] [狀態] 已選擇付費票並輸入人數，切換至免費票再切回付費票，總金額正確重新顯示並計算
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證票種多次切換後付費票金額的持久性與正確性
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 選擇票種『付費票』
  * And 指定報名人數為『2』
  * Then 畫面即時顯示總金額『NT$1000』
  * When 將票種切換為『免費票』
  * Then 總金額顯示欄位隱藏
  * When 再次將票種切換為『付費票』
  * Then 總金額顯示欄位重新可見
  * And 畫面即時顯示總金額『NT$1000』

---
### [TC-025] [狀態] 成功提交表單後，所有輸入欄位清空或重置為預設狀態
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證表單成功提交後的重置行為
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 填寫所有有效資料並成功提交表單
  * Then 姓名欄位清空
  * And Email 欄位清空
  * And 票種選擇重置為預設值（例如：免費票）
  * And 報名人數重置為預設值（例如：1）

---
### [TC-026] [狀態] 提交失敗後，所有輸入欄位保留使用者上次輸入的值，且錯誤訊息正確顯示
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證表單提交失敗後的資料保留行為
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入姓名『測試者』
  * And 輸入 Email 『invalid-email』
  * And 選擇票種『付費票』
  * And 指定報名人數為『5』
  * And 點擊『提交』按鈕
  * Then 系統顯示『Email 格式不正確』的錯誤訊息
  * And 姓名欄位仍顯示『測試者』
  * And Email 欄位仍顯示『invalid-email』
  * And 票種仍選擇『付費票』
  * And 報名人數仍顯示『5』

---
### [TC-027] [狀態] 表單提交過程中，提交按鈕變為禁用狀態，防止重複提交
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證提交按鈕的防呆機制
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * And 填寫所有有效資料
  * When 點擊『提交』按鈕
  * Then 『提交』按鈕立即變為禁用狀態
  * And 在系統處理提交期間，按鈕保持禁用
  * And 提交成功或失敗後，按鈕恢復可用狀態

---
### [TC-028] [狀態] 輸入部分資料後，不提交，直接刷新頁面，表單清空
* **優先級 (Priority)**: Low
* **嚴重程度 (Severity)**: Minor
* **描述 / 情境**: Feature: 活動報名表單 Scenario: 驗證頁面刷新後的表單狀態重置
* **測試步驟 (BDD Gherkin)**:
  * Given 使用者進入活動報名表單頁面
  * When 輸入姓名『部分資料』
  * And 輸入 Email 『partial@example.com』
  * And 刷新頁面
  * Then 姓名欄位清空
  * And Email 欄位清空
  * And 票種選擇重置為預設值
  * And 報名人數重置為預設值

---