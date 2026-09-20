import os
import glob
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# 自動流水號避覆蓋機制
def get_unique_filepath(directory, base_filename, extension):
    os.makedirs(directory, exist_ok=True)
    v = 1
    while True:
        filepath = os.path.join(directory, f"{base_filename}_v{v}.{extension}")
        if not os.path.exists(filepath):
            return filepath
        v += 1

def get_latest_file(directory, pattern):
    files = glob.glob(os.path.join(directory, pattern))
    if not files:
        return None
    # 依修改時間或版號排序，取最新的檔案
    return sorted(files)[-1]

def read_file_content(filepath):
    if not filepath or not os.path.exists(filepath):
        return "（未找到對應檔案）"
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

async def generate_reflection():
    docs_dir = "docs"
    
    # 1. 取得最新的 B1 Spec Review 與 B3 Bug Report
    b1_path = get_latest_file(docs_dir, "B1_Spec_Review*.md")
    b3_path = get_latest_file(docs_dir, "B3_Bug_Reports*.md")
    code_path = "src/index.html"

    print(f" 讀取上下文檔案中...")
    print(f"  - 規格文件: {b1_path}")
    print(f"  - Bug 報告: {b3_path}")
    print(f"  - 原始碼: {code_path}")

    b1_content = read_file_content(b1_path)
    b3_content = read_file_content(b3_path)
    code_content = read_file_content(code_path)

    # 2. 初始化 Gemini 3.6 Flash 模型
    llm = ChatGoogleGenerativeAI(
        # model="gemini-3.6-flash", 
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # 3. 建立反思報告 Prompt
    prompt = f"""
你是一位資深的 SDET / 測試架構師，正針對一份前端程式碼與規格進行 AI 協作開發與測試的反思報告 (Reflection Report)。

請根據下方提供的資料，撰寫一份高品質且完全對應當前專案與真實 Bug 的 Markdown 報告，必須包含 【C1. AI 第一次生成的程式碼分析】 與 【C2. 在測試工作中使用 AI 的最大風險與防範策略】 兩個核心章節。

【1. 規格審查報告 (B1 Spec Review)】：
{b1_content}

【2. 前端原始碼 (index.html)】：
{code_content}

【3. 靜態分析實際抓出的 Bug 報告 (B3 Bug Report)】：
{b3_content}

---

### 請嚴格依照以下結構與內容重點生成報告 (使用繁體中文)：

# AI 協作反思 (AI Collaboration Reflection)

### C1. AI 第一次生成的程式碼分析
**做對的地方：**
* 結合【1. 規格審查報告】與【2. 前端原始碼】，具體列出 AI 在實作顯性需求上表現優異之處（如：表單基礎 UI 佈局、必填欄位基礎判斷、金額基本計算邏輯等）。

**做錯或偏離規格的地方：**
* **必須精準引用【3. 靜態分析實際抓出的 Bug 報告】中的真實 Bug 項目（如 BUG-001, BUG-002 等）**。
* 分析 AI 在隱性邊界值、防呆機制或跨元件狀態連動上的缺陷（例如：未阻擋小數點輸入、票種切換狀態殘留、Email 正則漏洞等）。

**發現方式：**
* 說明如何透過 `B2_Test_Cases` 中的等價類劃分 (Equivalence Partitioning) 與邊界值分析 (Boundary Value Analysis)，結合黑箱測試與靜態審查，精準定位這些缺陷。

---

### C2. 在測試工作中使用 AI 的最大風險與防範策略
* **自動化與權威偏見 (Automation Bias)**：探討工程師過度依賴 AI 產出的格式精美程式碼或測試案例時，可能產生的盲點。
* **缺乏領域商業脈絡 (Business Context)**：說明 AI 擅長處理語法與顯性邏輯，但缺乏對使用者真實行為與複雜業務連動的洞察能力。
* **QA 工程師的 3 大防範策略**：
  1. 建立嚴格的人工 Review 與邊界案例補強機制。
  2. 注入領域知識 (Domain Knowledge) 與複雜情境疊加。
  3. 強化探索性測試 (Exploratory Testing) 以破除 AI 設下的線性思考框架。

請直接輸出最終 Markdown 內容，不要包含額外的說明文字。
"""

    print(" 正在呼叫 AI 深度對比並生成 AI 協作反思報告 (C_Reflection)...")
    response = await llm.ainvoke(prompt)
    
    # 4. 寫入 docs/C_Reflection_vX.md
    output_path = get_unique_filepath(docs_dir, "C_Reflection", "md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.content)

    print(f" 反思報告生成成功！已儲存至: {output_path}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_reflection())