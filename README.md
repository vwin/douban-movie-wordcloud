# 抓取豆瓣电影评论并绘制词云

1. 安装requirements.txt pip install -r requirements.txt
2. 修改douban_spider.py中最后一行的电影ID和电影名称，电影ID可从豆瓣上获取
例子：https://movie.douban.com/subject/26752088/ 电影ID为:26752088
3. 直接运行python3 douban_spider.py即可获得词云

# 分析微信群人群信息
1. 群内性别分布
2. 群内位置分布
3. 群内男性签名词云
4. 群内女性签名词云

# 报错解决
1. pyecharts版本问题，pip install pyecharts==0.1.9.5  https://blog.csdn.net/Nurbiya_K/article/details/105354670
2. itChat问题，显示错误信息：
   ```shell
   utils.msg_formatter(m, 'Content')
   File "D:\envPython\lib\site-packages\itchat\utils.py", line 69, in msg_formatter
   d[k]  = htmlParser.unescape(d[k])
   AttributeError: 'HTMLParser' object has no attribute 'unescape'
   网上的解决方式很多，没有一个真正解决问题了，最简单的方式是修改
   site-packages\itchat\utis.py
   
   from html import unescape
   # 修改d[k] = htmlParser.unescape(d[k])
   d[k] = unescape(d[k])
   ```