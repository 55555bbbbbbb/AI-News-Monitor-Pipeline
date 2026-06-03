import re
import json
from openai import OpenAI

def clean_json_output(text):
    try:
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match: 
            return json.loads(match.group(0))
    except:
        pass
    return None

def run_ai_analysis(title, text, system_prompt, config):
    try:
        client_ai = OpenAI(base_url=config['api_base'], api_key=config['api_key'])
        
        response = client_ai.chat.completions.create(
            model=config['model'],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"標題：{title}\n內文：\n{text[:2000]}"}
            ],
            temperature=0.1
        )
        
        raw_ai_text = response.choices[0].message.content
        return clean_json_output(raw_ai_text)
    except Exception as e:
        return [{"status": "出錯", "reason": str(e)}]