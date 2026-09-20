import asyncio
import glob
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# =========================================================================
# 設定 Qase API 與專案資訊
# =========================================================================
QASE_API_TOKEN = os.environ.get("QASE_API_TOKEN")
QASE_PROJECT_CODE = os.environ.get("QASE_PROJECT_CODE", "EC")
QASE_BASE_URL = "https://api.qase.io/v1"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Token": QASE_API_TOKEN
}

# =========================================================================
# 多模型備援引擎 (Multi-Model Failover Engine)
# =========================================================================
def get_available_llms():
    """動態偵測 .env 中的 API Key，建立優先順序模型鏈 (Gemini -> OpenAI -> Claude)"""
    llm_chain = []

    # 1. 主模型：Google Gemini
    google_key = os.getenv("GOOGLE_API_KEY")
    if google_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_google_genai import ChatGoogleGenerativeAI
            # llm_chain.append(("Google Gemini (3.6-Flash)", ChatGoogleGenerativeAI(
            #     model="gemini-3.6-flash",
            #     temperature=0.2,
            #     google_api_key=google_key
            # )))
            llm_chain.append(("Google Gemini (2.5-Flash)", ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.2,
                google_api_key=google_key
            )))
        except Exception as e:
            print(f" 無法初始化 Google Gemini: {e}")

    # 2. 備援模型一：OpenAI GPT-4o
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and not openai_key.startswith("sk-請替換"):
        try:
            from langchain_openai import ChatOpenAI
            llm_chain.append(("OpenAI (GPT-4o)", ChatOpenAI(
                model="gpt-4o",
                temperature=0.2,
                api_key=openai_key
            )))
        except Exception as e:
            print(f" 無法初始化 OpenAI: {e}")

    # 3. 備援模型二：Anthropic Claude
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and not anthropic_key.startswith("sk-ant-api03-請替換"):
        try:
            from langchain_anthropic import ChatAnthropic
            llm_chain.append(("Anthropic Claude (3.5-Sonnet)", ChatAnthropic(
                model="claude-3-5-sonnet-20240620",
                temperature=0.2,
                api_key=anthropic_key
            )))
        except Exception as e:
            print(f" 無法初始化 Anthropic Claude: {e}")

    return llm_chain

# =========================================================================
# 輔助函式：自動檢查既存檔案並生成不重複的流水號檔名
# =========================================================================
def get_unique_filepath(directory, prefix, extension=".md"):
    """
    自動檢查資料夾內既存檔案，回傳下一個不重複的流水號路徑。
    範例：若已存在 B2_Test_Cases_v1.md，則會自動產出 B2_Test_Cases_v2.md
    """
    i = 1
    while True:
        filename = f"{prefix}_v{i}{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1

# =========================================================================
# 輔助函式：將測試案例同步輸出為 Markdown 備份
# =========================================================================
def save_cases_to_markdown(cases, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    md_content = ["# 測試案例設計 (Test Cases)\n"]
    priority_map = {1: "High", 2: "Medium", 3: "Low"}
    severity_map = {1: "Blocker", 2: "Critical", 3: "Major", 4: "Normal", 5: "Minor"}

    for idx, case in enumerate(cases, 1):
        tc_id = f"TC-{idx:03d}"
        title = case.get("title", "未命名測試案例")
        desc = case.get("description", "").replace("\n", " ")
        prio = priority_map.get(case.get("priority"), "Medium")
        sev = severity_map.get(case.get("severity"), "Normal")

        md_content.append(f"### [{tc_id}] {title}")
        md_content.append(f"* **優先級 (Priority)**: {prio}")
        md_content.append(f"* **嚴重程度 (Severity)**: {sev}")
        if desc:
            md_content.append(f"* **描述 / 情境**: {desc}")

        md_content.append("* **測試步驟 (BDD Gherkin)**:")
        steps = case.get("steps", [])
        for s in steps:
            action = s.get("action", "")
            md_content.append(f"  * {action}")

        md_content.append("\n---")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content))

    print(f" 已成功將 {len(cases)} 個測試案例同步備份至: {output_path}")

# =========================================================================
# 步驟 1：向 Qase 抓取現有的 Suites (目錄) 清單
# =========================================================================
def get_existing_suites():
    url = f"{QASE_BASE_URL}/suite/{QASE_PROJECT_CODE}?limit=100"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            res_data = response.json()
            entities = res_data.get("result", {}).get("entities", [])
            suites_map = {item["title"]: item["id"] for item in entities}
            return suites_map
        else:
            print(f" 無法抓取 Qase 目錄，狀態碼: {response.status_code}")
            return {}
    except Exception as e:
        print(f" 抓取 Qase 目錄發生異常: {e}")
        return {}

# =========================================================================
# 步驟 2：建立新 Suite (支援階層目錄)
# =========================================================================
def create_new_suite(suite_title, parent_id=None):
    url = f"{QASE_BASE_URL}/suite/{QASE_PROJECT_CODE}"
    payload = {"title": suite_title}

    if parent_id:
        payload["parent_id"] = parent_id

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            new_suite_id = response.json().get("result", {}).get("id")
            parent_msg = f" (建立於父目錄 ID: {parent_id} 之下)" if parent_id else " (建立於最外層)"
            print(f" [Qase] 成功建立新目錄: {suite_title} [ID: {new_suite_id}]{parent_msg}")
            return new_suite_id
        else:
            print(f" 建立新目錄失敗: {response.text}")
            return None
    except Exception as e:
        print(f" 建立新目錄發生異常: {e}")
        return None

# =========================================================================
# 步驟 3：將測試案例壓入 Qase
# =========================================================================
def push_case_to_qase(case_data):
    url = f"{QASE_BASE_URL}/case/{QASE_PROJECT_CODE}"

    try:
        response = requests.post(url, json=case_data, headers=headers)
        if response.status_code == 200:
            case_id = response.json().get("result", {}).get("id")
            print(f" 成功寫入！Case ID: {QASE_PROJECT_CODE}-{case_id}")
            return case_id
        else:
            print(f" 寫入失敗: {response.text}")
            return None
    except Exception as e:
        print(f" 寫入發生異常: {e}")
        return None

# =========================================================================
# 步驟 4：核心大腦 - 具備自動備援 (Failover) 的 AI QA 決策引擎
# =========================================================================
async def smart_ai_qa_orchestrator(spec_text, existing_suites, b2_output_path):
    llm_chain = get_available_llms()

    if not llm_chain:
        print(" 未偵測到任何有效的 LLM API Key，請檢查 .env 設定。")
        return False

    prompt = f"""
你是一位殿堂級的 QA 自動化架構師。請閱讀以下的功能需求 (Spec) 與 Qase 撰寫規範，並對照目前 Qase.io 系統中已有的目錄結構，做出分類決策，並生成 BDD 測試案例與所有必要屬性。

{spec_text}

【Qase 目前已有的目錄結構 (格式為 名稱: ID)】:
{json.dumps(existing_suites, ensure_ascii=False, indent=2)}

【決策與生成規則】:
1. 目錄分類決策 (directory_decision)：
   - 若現有目錄符合，請填 "USE_EXISTING"，並將目標目錄 ID 填入 "suite_id"。
   - 若無合適目錄，請填 "CREATE_NEW"，並在 "new_suite_title" 輸入新目錄名稱。"suite_id" 設為 null。
   - 在 CREATE_NEW 時，若新目錄歸屬於現有「大目錄」，請將該大目錄 ID 填入 "parent_suite_id"；否則設為 null。
2. 測試案例生成：請根據 Spec，列出所有相關的正向 (Happy Path)、負向 (Negative/Error) 與極端/邊界 (Edge/Boundary) Test Cases。
3. 步驟 (Steps)：每個 Test Case 的 BDD (Gherkin) 步驟必須獨立拆解為陣列放入 "steps" 中。
4. 屬性 (Attributes)：請嚴格參考 Spec 預設值限制填入數字代碼。

請嚴格以 JSON 格式回覆，不要包含 ```json 等 Markdown 標記。回傳結構如下：
{{
    "directory_decision": {{
        "decision_action": "USE_EXISTING",
        "suite_id": 35,
        "new_suite_title": null,
        "parent_suite_id": null
    }},
    "test_cases": [
        {{
            "title": "[正向] 報名付費票且人數為 1 時成功計算金額 NT$500",
            "description": "Feature: 活動報名表單\\nScenario: 正確計算付費票金額",
            "status": 0,
            "severity": 4,
            "priority": 2,
            "type": 2,
            "layer": 1,
            "is_flaky": 0,
            "behavior": 1,
            "automation": 0,
            "steps_type": "gherkin",
            "tags": ["Frontend", "Web"],
            "steps": [
                {{"action": "Given 使用者進入活動報名表單頁面"}},
                {{"action": "When 票種選擇『付費票』且人數輸入『1』"}},
                {{"action": "Then 畫面即時顯示總金額『NT$ 500』"}}
            ]
        }}
    ]
}}
"""

    raw_response_text = None

    # 自動備援迴圈：依序試用可用的 LLM
    for model_name, llm in llm_chain:
        try:
            print(f"\n 正在使用 【{model_name}】 分析需求並生成 Qase 案例...")
            response = await llm.ainvoke(prompt)

            raw_content = response.content
            if isinstance(raw_content, list):
                raw_response_text = "".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in raw_content])
            else:
                raw_response_text = str(raw_content)

            if raw_response_text:
                print(f"【{model_name}】 呼叫成功！")
                break
        except Exception as e:
            print(f"【{model_name}】 呼叫失敗 ({e})，自動切換至下一個備援模型...")

    if not raw_response_text:
        print(" 所有模型皆呼叫失敗，無法完成自動化任務。")
        return False

    # 解析與清理 JSON
    try:
        text_content = raw_response_text.strip()
        if text_content.startswith("```json"):
            text_content = text_content[7:]
        elif text_content.startswith("```"):
            text_content = text_content[3:]
        if text_content.endswith("```"):
            text_content = text_content[:-3]

        ai_response = json.loads(text_content.strip())

        dir_decision = ai_response.get("directory_decision", {})
        cases = ai_response.get("test_cases", [])

        print(f" AI 決策分析完成：[動作: {dir_decision.get('decision_action')}]")
        print(f" 共生成了 {len(cases)} 個 Test Cases。")

        # 1. 備份到 docs/B2_Test_Cases_vX.md
        if cases:
            save_cases_to_markdown(cases, b2_output_path)

        # 2. 推送到 Qase.io
        final_suite_id = None
        if dir_decision.get("decision_action") == "USE_EXISTING":
            final_suite_id = dir_decision.get("suite_id")
            print(f" 匹配現有目錄 ID: [{final_suite_id}]")
        elif dir_decision.get("decision_action") == "CREATE_NEW":
            new_title = dir_decision.get("new_suite_title")
            parent_id = dir_decision.get("parent_suite_id")
            print(f" 準備建立新目錄: {new_title}")
            final_suite_id = create_new_suite(new_title, parent_id)

        if final_suite_id:
            print(f"\n 準備將 {len(cases)} 個測試案例批次寫入 Qase.io...")
            for idx, case_payload in enumerate(cases, 1):
                case_payload["suite_id"] = final_suite_id
                print(f" 正在寫入第 {idx} 個 Case: {case_payload.get('title')}")
                push_case_to_qase(case_payload)
            return True
        else:
            print(" 無法確定目標目錄 ID，自動化終止。")
            return False

    except Exception as e:
        print(f" JSON 解析或 Qase 寫入過程中發生錯誤: {e}")
        return False

# =========================================================================
# 測試執行入口
# =========================================================================
async def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # ai_agents/ 資料夾
    ROOT_DIR = os.path.dirname(BASE_DIR)                   # 專案根目錄

    rules_file = os.path.join(BASE_DIR, "qase_style.md")
    specs_dir = os.path.join(BASE_DIR, "pending_specs")
    docs_dir = os.path.join(ROOT_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)

    # 動態取得不重複的流水號路徑 (如 B2_Test_Cases_v1.md)
    b2_output_path = get_unique_filepath(docs_dir, "B2_Test_Cases")

    if not os.path.exists(rules_file):
        print(f" 找不到規則檔：{rules_file}。請確認它存在於專案目錄。")
        return

    with open(rules_file, "r", encoding="utf-8") as f:
        base_rules = f.read()

    print(" 正在從 Qase.io 讀取目前的目錄架構...")
    existing_suites = get_existing_suites()
    print(f"已偵測到現有目錄數: {len(existing_suites)} 個\n" + "-" * 40)

    search_pattern = os.path.join(specs_dir, "*.md")
    pending_files = glob.glob(search_pattern)

    # 過濾出未處理的 md 檔案（排除 feature.md 避免混淆，或依需求調整）
    pending_files = [f for f in pending_files if not f.endswith(".processed")]

    if not pending_files:
        print(f" 在 {specs_dir}/ 中沒有找到任何待處理的需求檔。")
        return

    print(f" 偵測到 {len(pending_files)} 個待處理需求檔，開始批次作業...\n")

    for file_path in pending_files:
        print(f" 正在處理檔案: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            feature_req = f.read()

        combined_spec = f"【當前處理的功能需求】:\n{feature_req}\n\n---\n\n【Qase 撰寫規範】:\n{base_rules}"

        success = await smart_ai_qa_orchestrator(combined_spec, existing_suites, b2_output_path)

        if success:
            os.rename(file_path, file_path + ".processed")
            print(f" {file_path} 處理完畢，已標記為 .processed\n" + "-" * 40)

if __name__ == "__main__":
    asyncio.run(main())