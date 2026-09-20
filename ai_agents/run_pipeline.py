import subprocess
import sys

def run_script(script_path):
    print(f"\n==============================================")
    print(f"🚀 正在啟動 Agent 引擎: {script_path}")
    print(f"==============================================")
    
    # 使用當前虛擬環境的 python 解釋器執行子腳本
    result = subprocess.run([sys.executable, script_path])
    
    if result.returncode != 0:
        print(f"\n❌ 錯誤：執行 {script_path} 時發生異常，流程中斷。")
        sys.exit(1)
    
    print(f"✅ 完成：{script_path} 執行成功！\n")

def main():
    # 定義 0 到 4 號引擎的執行順序
    pipeline = [
        "ai_agents/generate_prompt_history.py",  # 引擎零：逆向生成 Prompt 歷史
        "ai_agents/extract_specs_to_feature.py", # 引擎一：規格審查與精煉
        "ai_agents/generate_qase_bdd.py",        # 引擎二：生成 BDD 並同步 Qase
        "ai_agents/validate_and_report.py",      # 引擎三：靜態抓蟲與 Bug 報告
        "ai_agents/generate_reflection.py"       # 引擎四：反思與風險評估報告
    ]

    print("開始執行完整 SDET Agent 自動化工作流...")
    
    for script in pipeline:
        run_script(script)

    print("==============================================")
    print("太棒了！整個工作流已 100% 全自動執行完畢！")
    print("所有交付檔案皆已安全更新至 prompts/ 與 docs/ 目錄中。")
    print("==============================================")

if __name__ == "__main__":
    main()