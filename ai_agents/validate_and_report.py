import asyncio
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# =========================================================================
# 路徑基底設定 (確保不管在專案何處執行指令皆能正確存取)
# =========================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ai_agents/ 資料夾
ROOT_DIR = os.path.dirname(BASE_DIR)                   # 專案根目錄

# =========================================================================
# 輔助函式：讀取單一檔案
# =========================================================================
def read_file_content(file_path):
    if not os.path.exists(file_path):
        return ""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ 讀取檔案 {file_path} 失敗: {e}")
        return ""

# =========================================================================
# 輔助函式：自動檢查既存檔案並生成不重複的流水號檔名
# =========================================================================
def get_unique_filepath(directory, prefix, extension=".md"):
    """
    自動檢查資料夾內既存檔案，回傳下一個不重複的流水號路徑。
    範例：若已存在 B3_Bug_Reports_v1.md，則會自動產出 B3_Bug_Reports_v2.md
    """
    i = 1
    while True:
        filename = f"{prefix}_v{i}{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1

# =========================================================================
# 輔助函式：自動尋找 docs/ 底下最新版本的 B2 測試案例檔案
# =========================================================================
def find_latest_test_cases(docs_dir):
    if not os.path.exists(docs_dir):
        return ""
    
    # 尋找所有符合 B2_Test_Cases_v*.md 的檔案
    candidates = []
    for f in os.listdir(docs_dir):
        if f.startswith("B2_Test_Cases_v") and f.endswith(".md"):
            candidates.append(f)
    
    if not candidates:
        return ""
    
    # 依版本號排序，取最新的一個
    candidates.sort()
    latest_file = os.path.join(docs_dir, candidates[-1])
    print(f"🔗 已自動對應關聯的 B2 測試案例檔案: {candidates[-1]}")
    return read_file_content(latest_file)

# =========================================================================
# 輔助函式：自動收集 src/ 目錄下的所有原始碼 (HTML, JS, CSS)
# =========================================================================
def collect_source_code(src_dir):
    if not os.path.exists(src_dir):
        print(f"⚠️ 找不到程式碼資料夾: {src_dir}")
        return ""

    code_contents = []
    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.endswith((".html", ".js", ".css")):
                file_path = os.path.join(root, file)
                content = read_file_content(file_path)
                if content:
                    code_contents.append(f"/* 檔案路徑: {file_path} */\n{content}")

    return "\n\n".join(code_contents)

# =========================================================================
# 核心邏輯：讓 AI 對比 Spec、B2 測試案例 與 Source Code 並產出 B3 Bug Report
# =========================================================================
async def validate_code_against_spec(spec_text, test_cases_text, source_code):
    # llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.1)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    prompt = f"""
你是一位極度嚴謹的資深 SDET / 自動化測試專家與軟體安全審查員。
請仔細比對下方【需求規範與測試重點 (Spec/B1 Review)】、【B2 測試案例內容 (Test Cases)】以及【前端實作原始碼 (Source Code)】。

你的任務是找出實作中所有不符合規格、邏輯漏洞、邊界值防呆缺失、或潛在資安風險 (如 XSS/DOM 注入/欄位未轉義) 的 Bug。

【需求規範與測試重點 (Spec)】:
{spec_text}

----------------------------------------------------------------
【B2 測試案例內容 (Test Cases - 供追溯對應)】:
{test_cases_text}

----------------------------------------------------------------
【前端實作原始碼 (Source Code)】:
{source_code}

----------------------------------------------------------------
【任務說明】:
請將發掘到的所有實作漏洞，編寫為一份符合企業標準與作業規範的 Markdown Bug 報告 (B3 Bug Reports)。
每個 Bug 必須包含以下欄位（**特別注意：必須強制對應到上方 B2 測試案例中對應的項目編號**）：
1. **Bug ID** (例如: [BUG-001])
2. **Severity** (嚴重程度: Blocker / High / Medium / Low)
3. **Related Test Case** (對應 B2 的測試案例編號或項目，例如：`對應 B2 第 19 項` 或 `對應 B2 負向/邊界測試案例`)
4. **Bug 標題** (簡短明確點出問題)
5. **重現步驟 (Steps to Reproduce)**
6. **預期結果 (Expected Result)**
7. **實際結果 (Actual Result)**

請直接輸出完整的 Markdown 內容，不要包含問候語或 Markdown 包裹標籤 (如 ```markdown)。

請嚴格格式化輸出為：
# 測試缺陷回報 (Bug Reports)

### [BUG-001] Email 欄位未阻擋錯誤格式輸入
- **Severity**: High
- **Related Test Case**: 對應 B2 第 7 項：驗證 Email 欄位輸入無效格式
- **Steps to Reproduce**:
  1. 進入活動報名表單頁面。
  2. 在姓名欄位填寫「王五」。
  3. 在 Email 欄位輸入缺少 `@` 或網域的錯誤字串（例如 `invalid-email`）。
  4. 點擊「送出報名」按鈕。
- **Expected Result**: 系統應阻擋表單送出，並明確顯示「Email 格式錯誤」之錯誤訊息。
- **Actual Result**: 系統未進行格式驗證，表單成功送出並顯示「報名成功」。

---
"""

    try:
        response = await llm.ainvoke(prompt)
        content = response.content

        if isinstance(content, list):
            text_parts = []
            for block in content:
                if isinstance(block, str):
                    text_parts.append(block)
                elif isinstance(block, dict) and "text" in block:
                    text_parts.append(block["text"])
            content = "\n".join(text_parts)

        content = str(content).strip()
        if content.startswith("```markdown"):
            content = content[11:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        return content.strip()
    except Exception as e:
        print(f"❌ AI 審查程式碼失敗: {e}")
        return ""

# =========================================================================
# 主流程入口
# =========================================================================
async def main():
    docs_dir = os.path.join(ROOT_DIR, "docs")
    src_dir = os.path.join(ROOT_DIR, "src")
    os.makedirs(docs_dir, exist_ok=True)

    # 優先讀取 ai_agents/pending_specs/feature.md，若無則讀取 docs/B1_Spec_Review.md
    spec_path = os.path.join(BASE_DIR, "pending_specs", "feature.md")
    if not os.path.exists(spec_path):
        spec_path = os.path.join(docs_dir, "B1_Spec_Review.md")

    # 動態取得不重複的流水號路徑 (如 B3_Bug_Reports_v1.md)
    output_file = get_unique_filepath(docs_dir, "B3_Bug_Reports")

    print("🔍 正在讀取規格文件、B2 測試案例與 src/ 前端原始碼...")
    spec_text = read_file_content(spec_path)
    test_cases_text = find_latest_test_cases(docs_dir)
    source_code = collect_source_code(src_dir)

    if not spec_text:
        print(f"❌ 找不到有效的 Spec 規範文件 ({spec_path})，請先執行 extract_specs_to_feature.py！")
        return

    if not source_code:
        print(f"❌ 未在 {src_dir} 目錄中找到任何原始碼 (.html, .js)，請確認 src/index.html 存在！")
        return

    print("🤖 正在呼叫 AI 進行程式碼與 B2 案例的雙向比對與 Bug 發掘...")
    bug_report = await validate_code_against_spec(spec_text, test_cases_text, source_code)

    if bug_report:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(bug_report)
        print(f"✅ Bug Report 生成成功！已寫入至: {output_file}")
        print(f"📄 可開啟 {output_file} 檢視產出結果（內含 B2 測試案例對應編號）。")

if __name__ == "__main__":
    asyncio.run(main())