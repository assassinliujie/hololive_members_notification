# hololive_members_notification
members stream notification

会限直播通知。清填写app.py中smtp邮箱部分。

如果在中国大陆等网络受限制区域使用，查找app.py中这一句，配置你的代理地址。['yt-dlp', '--proxy', 'http://192.168.99.189:7899','-I', '1','--flat-playlist','--skip-download','--print', 'live_status', url],
其余地区人请改为['yt-dlp','-I', '1','--flat-playlist','--skip-download','--print', 'live_status', url],

使用前先安装yt-dlp，确定你使用的终端能直接使用yt-dlp命令。具体请github搜索yt-dlp
