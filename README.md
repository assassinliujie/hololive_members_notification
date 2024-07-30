[中文](#hololive会限直播通知)|[ENGLISH](#hololive_members_live_stream_notification)

自行修改csv表格中的频道名和频道URL即可实现对任意直播进行直播通知

# hololive会限直播通知

此应用旨在通知用户直播活动。请按照以下步骤配置和运行应用程序。

## 配置

### SMTP 邮箱设置

1. 打开 `app.py` 文件，找到 SMTP 邮箱配置部分。
2. 输入你的 SMTP 服务器详细信息，包括服务器地址、端口、用户名和密码。
```python
SMTP_SERVER = 'smtp.qq.com' //smtp服务器地址
SMTP_PORT = 465 //smtp服务器地址
SMTP_USERNAME = 'x@qq.com' //邮箱名，即你用来发送通知邮件的邮箱
SMTP_PASSWORD = 'passwd' //用来发送通知邮件的邮箱的SMTP密码，许多服务商，比如QQ，是有独立SMTP密码的，请自行搜索
FROM_EMAIL = 'x@qq.com' //邮箱名，即你用来发送通知邮件的邮箱
TO_EMAIL = 'yourself@qq.com' //接受邮件的邮箱
FROM_NAME = 'x' //发送邮件的昵称，跟邮箱名一样即可
```

### 代理配置

如果你在中国大陆或其他网络受限的区域，请按以下步骤配置你的代理：

1. 打开 `app.py` 文件，找到包含 `yt-dlp` 代理配置的行。
2. 将该行更新为以下内容，以包括你的代理地址：
   ```python
   ['yt-dlp', '--proxy', 'http://192.168.99.189:7899', '-I', '1', '--flat-playlist', '--skip-download', '--print', 'live_status', url]
   ```
   将 `'http://192.168.99.189:7899'` 替换为你的代理地址。

   对于其他没有网络限制的地区，请使用：
   ```python
   ['yt-dlp', '-I', '1', '--flat-playlist', '--skip-download', '--print', 'live_status', url]
   ```

## 安装与运行

1. 首先，安装所需的 Python 包：
   ```bash
   pip install -r requirements.txt
   ```
2. 然后，运行应用程序：
   ```bash
   python app.py
   ```

---

如有其他需要，请根据实际情况调整相关细节。

---

# hololive_members_live_stream_notification

This application is designed to notify users about live streams. Please follow the steps below to configure and run the application.

## Configuration

### SMTP Email Settings

1. Open `app.py` and locate the SMTP email configuration section.
2. Enter your SMTP server details, including the server address, port, username, and password.

### Proxy Configuration

If you are in China or other regions with restricted network access, follow these steps to configure your proxy:

1. Open `app.py` and find the line that contains the proxy configuration for `yt-dlp`.
2. Update the line to include your proxy address as follows:
   ```python
   ['yt-dlp', '--proxy', 'http://192.168.99.189:7899', '-I', '1', '--flat-playlist', '--skip-download', '--print', 'live_status', url]
   ```
   Replace `'http://192.168.99.189:7899'` with your proxy address.

   For other regions without network restrictions, use:
   ```python
   ['yt-dlp', '-I', '1', '--flat-playlist', '--skip-download', '--print', 'live_status', url]
   ```

## Installation and Running

1. First, install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
2. Then, run the application:
   ```bash
   python app.py
   ```
