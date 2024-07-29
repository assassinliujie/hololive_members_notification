import sqlite3
import os
import subprocess
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import pandas as pd

# 数据库文件名和表名
DATABASE_FILE = 'channel.db'
TABLE_NAME = 'hololive'
CHANNEL_FILE = 'channel.xlsx'

# SMTP 配置
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465
SMTP_USERNAME = 'x@qq.com'
SMTP_PASSWORD = 'passwd'
FROM_EMAIL = 'x@qq.com'
TO_EMAIL = 'yourself@qq.com'
FROM_NAME = 'x'

def check_live_status(url):
    """使用yt-dlp检查频道是否在直播"""
    try:
        result = subprocess.run(
            ['yt-dlp', '--proxy', 'http://192.168.99.189:7899','-I', '1','--flat-playlist','--skip-download','--print', 'live_status', url],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip() == 'is_live'
    except subprocess.CalledProcessError as e:
        print(f"Error checking live status for {url}: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def init_database():
    """初始化数据库并从XLSX文件加载数据"""
    if os.path.exists(DATABASE_FILE):
        print(f"{DATABASE_FILE} 已存在，跳过创建表格")
        return

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE {TABLE_NAME} (
            channelname TEXT,
            is_live TEXT DEFAULT 'no',
            url TEXT
        )
    ''')
    
    # 从XLSX文件中读取数据并插入数据库
    df = pd.read_excel(CHANNEL_FILE)
    for index, row in df.iterrows():
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (channelname, is_live, url)
            VALUES (?, 'no', ?)
        ''', (row[0], row[1]))

    conn.commit()
    conn.close()

def send_email(subject, body):
    """发送邮件通知"""
    msg = MIMEMultipart()
    msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

def update_live_status():
    """循环检查频道的直播状态并更新数据库"""
    while True:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(f'SELECT channelname, url, is_live FROM {TABLE_NAME}')
        channels = cursor.fetchall()
        conn.close()
        
        for channelname, url, old_status in channels:
            is_live = check_live_status(url)
            new_status = 'yes' if is_live else 'no'
            
            if new_status != old_status:
                subject = f"{channelname} 开始直播" if new_status == 'yes' else f"{channelname} 停止直播"
                body = f"{channelname} 的直播状态已更新为: {new_status}"
                send_email(subject, body)
            
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE {TABLE_NAME}
                SET is_live = ?
                WHERE url = ?
            ''', (new_status, url))
            conn.commit()
            conn.close()
        
        time.sleep(60)  # 等待一分钟后再次检查

def main():
    init_database()
    update_live_status()

if __name__ == '__main__':
    main()
