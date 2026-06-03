import os
import pandas as pd
from datetime import datetime

def export_to_excel(data_list):
    df = pd.DataFrame(data_list)
    
    df['判定狀態'] = pd.Categorical(
        df['判定狀態'], 
        categories=["符合", "不符合規則", "出錯", "未知"], 
        ordered=True
    )
    df = df.sort_values(by='判定狀態')
    
    cols = ['判定狀態', '不符合原因', '新聞標題', '學校', '發布時間', '新聞連結', '計畫名稱', '前往國家', '文稿內容']
    df = df[[c for c in cols if c in df.columns]]
    
    today_str = datetime.now().strftime('%Y%m%d')
    base_filename = f"自動化監測報表_{today_str}"
    excel_filename = f"{base_filename}.xlsx"
    
    counter = 1
    while os.path.exists(excel_filename):
        excel_filename = f"{base_filename}({counter}).xlsx"
        counter += 1
        
    df.to_excel(excel_filename, index=False)
    return excel_filename