import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_email_with_excel(file_path, valid_count, receiver_email):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"【自動化監測報表】今日共產出 {valid_count} 則有效資訊 - {datetime.now().strftime('%Y/%m/%d')}"
    
    body = f"系統自動化抓取與審核已完成。\n本次共發現 {valid_count} 則符合條件的項目。\n詳細資料請參閱附件。\n\n(此為系統自動發送)"
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except Exception:
        pass