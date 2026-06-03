import os
import json
from dotenv import load_dotenv
from src.scraper import fetch_news_entries, get_real_url, fetch_and_parse_text
from src.analyzer import run_ai_analysis
from src.formatter import export_to_excel
from src.mailer import send_email_with_excel

def main():
    load_dotenv()
    
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    entries = fetch_news_entries(config['search_query'], config['search_days'])
    
    if not entries:
        return

    all_processed_data = []
    
    for entry in entries:
        real_url = get_real_url(entry.link)
        text_content = fetch_and_parse_text(real_url)
        
        if not text_content or len(text_content) < 50:
            all_processed_data.append({
                "判定狀態": "不符合規則",
                "不符合原因": "內文擷取失敗或字數過少",
                "新聞標題": entry.title,
                "新聞連結": real_url,
                "發布時間": entry.published
            })
            continue

        ai_results = run_ai_analysis(entry.title, text_content, system_prompt, config)
        
        if ai_results:
            for item in ai_results:
                status = item.get('status', '未知')
                all_processed_data.append({
                    "判定狀態": status,
                    "不符合原因": item.get('reason', ''),
                    "發布時間": entry.published,
                    "新聞標題": entry.title,
                    "學校": item.get('school', ''),
                    "計畫名稱": item.get('plan_type', '') if status == "符合" else "",
                    "前往國家": item.get('country', ''),
                    "文稿內容": item.get('post_content', ''),
                    "新聞連結": real_url
                })
        else:
            all_processed_data.append({
                "判定狀態": "出錯",
                "不符合原因": "AI 未能產出有效 JSON",
                "新聞標題": entry.title,
                "新聞連結": real_url,
                "發布時間": entry.published
            })

    if all_processed_data:
        excel_path = export_to_excel(all_processed_data)
        success_count = sum(1 for d in all_processed_data if d['判定狀態'] == "符合")
        send_email_with_excel(excel_path, success_count, config['receiver_email'])

if __name__ == "__main__":
    main()