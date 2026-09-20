import os
from dotenv import load_dotenv
from google import genai

# 1. 載入根目錄的 .env 檔案
load_dotenv()

def reverse_engineer_prompt():
    html_path = "src/index.html"
    output_dir = "prompts"

    if not os.path.exists(html_path):
        print(f"錯誤：找不到待測檔案 {html_path}")
        return

    # 讀取 index.html 原始碼
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    print(" AI 正在分析前端程式碼以逆向反推 Prompt 歷史...")

    # 確保 GOOGLE_API_KEY 能正確對應給 GEMINI_API_KEY
    if "GOOGLE_API_KEY" in os.environ and "GEMINI_API_KEY" not in os.environ:
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

    # 初始化新版 Client
    client = genai.Client()

    meta_prompt = f"""
    你是一個資深前端架構師與 AI 提示詞工程專家。
    以下是一支由 AI 生成的單頁「活動報名表單」前端程式碼 (`src/index.html`)：

    ```html
    {html_content}
    ```

    請根據這支程式碼的實際結構、欄位、驗證邏輯與 CSS 樣式，逆向推導並撰寫一份專業的 Markdown 格式「AI 提示詞紀錄 (Prompt History)」。
    內容必須包含：
    1. 使用工具 (Gemini / Claude 等)
    2. 當時工程師輸入的具體原始提示詞 (Prompt) 內容，需精準對應這支程式碼實作出來的欄位（姓名、Email、票種、人數、500元即時總金額計算、錯誤驗證提示與成功訊息）。
    3. 產出結果與備註說明。

    請直接輸出乾淨的 Markdown 格式內容，不要帶有額外的贅字。
    """

    # 呼叫模型生成
    # response = client.models.generate_content(
    #         model='gemini-3.6-flash',
    #         contents=meta_prompt,
    # )
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=meta_prompt,
    )
    
    
    # 確保 prompts 目錄存在
    os.makedirs(output_dir, exist_ok=True)

    # 動態產生流水號檔名 (prompt_history_v1.md, prompt_history_v2.md...)
    existing_files = [f for f in os.listdir(output_dir) if f.startswith("prompt_history_v") and f.endswith(".md")]
    next_version = len(existing_files) + 1
    output_filename = f"prompt_history_v{next_version}.md"
    output_path = os.path.join(output_dir, output_filename)

    # 寫入檔案
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f" 成功逆向生成 Prompt 歷史記錄至: {output_path}")

if __name__ == "__main__":
    reverse_engineer_prompt()