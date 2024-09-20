import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 汇率 API 配置
API_URL = "https://api.exchangerate-api.com/v4/latest/AUD"

# 邮件配置
EMAIL_PROVIDERS = {
    "gmail": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587
    },
    "outlook": {
        "smtp_server": "smtp-mail.outlook.com",
        "smtp_port": 587
    },
    "yahoo": {
        "smtp_server": "smtp.mail.yahoo.com",
        "smtp_port": 587
    }
    # 可以继续添加其他邮箱服务商
}

# 从环境变量获取配置
EMAIL_PROVIDER = os.getenv('EMAIL_PROVIDER', 'gmail').lower()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')

def get_exchange_rate():
    response = requests.get(API_URL)
    data = response.json()
    return data['rates']['CNY']

def send_email(rate):
    subject = f"澳元对人民币汇率 - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"今日澳元对人民币汇率为: 1 AUD = {rate:.4f} CNY"

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    provider_config = EMAIL_PROVIDERS.get(EMAIL_PROVIDER)
    if not provider_config:
        raise ValueError(f"不支持的邮件服务商: {EMAIL_PROVIDER}")

    with smtplib.SMTP(provider_config['smtp_server'], provider_config['smtp_port']) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)

def main():
    try:
        rate = get_exchange_rate()
        send_email(rate)
        print("邮件发送成功!")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()
