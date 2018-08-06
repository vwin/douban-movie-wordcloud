# -*- coding: utf-8 -*-
# Created by Duanwei on 2018/3/21
import requests
import re
import jieba
import pandas as pd
import numpy  # numpy计算包
from bs4 import BeautifulSoup as bs
from requests.exceptions import RequestException
from wordcloud import WordCloud  # 词云包
import matplotlib.pyplot as plt

import matplotlib


matplotlib.rcParams["figure.figsize"] = (10.0, 5.0)
import warnings


warnings.filterwarnings("ignore")


# 抓取电影评论
def getCommentsById(movieId, pageNum):
    eachCommentList = []
    if pageNum > 0:
        start = (pageNum - 1) * 20
    else:
        return False
    requrl = (
        "https://movie.douban.com/subject/"
        + movieId
        + "/comments"
        + "?"
        + "start="
        + str(start)
        + "&limit=20"
    )
    try:
        resp = requests.get(requrl)
        html_data = resp.content.decode("utf-8")
        soup = bs(html_data, "html.parser")
        comment_div_lits = soup.find_all("div", class_="comment")
        for item in comment_div_lits:
            # 豆瓣网页元素变更
            # print(item.find_all(name='span', attrs={"class": "short"})[0].string)
            if item.find_all(name='span', attrs={"class": "short"})[0].string is not None:
                eachCommentList.append(item.find_all(name='span', attrs={"class": "short"})[0].string)
                print(eachCommentList)
        if eachCommentList is None:
            print("未获取到评论！")
            exit(1)
    except RequestException as e:
        print("请求问题，原因：%s" % e)

    return eachCommentList


def main(movieId, movieName):
    # 循环获取第一个电影的前十页评论
    commentList = []
    for i in range(10):
        num = i + 1
        commentList_temp = getCommentsById(movieId=movieId, pageNum=num)
        commentList.append(commentList_temp)
        # 将列表中的数据转换为字符串
    comments = ""
    for k in range(len(commentList)):
        print(commentList[k])
        for m in range(len(commentList[k])):
            comments = comments + str(commentList[k][m]).strip()
    # print(comments)

    # 使用正则去掉标点
    filtrate = re.compile(r"[^\u4E00-\u9FA5]")  # 提取中文，过滤掉非中文字符
    filtered_str = filtrate.sub(r"", comments)  # replace
    # print(filtered_str)

    # 用结巴分词进行中文分词
    segment = jieba.lcut(filtered_str)
    words_df = pd.DataFrame({"segment": segment})

    # 去掉停用词
    stopwords = pd.read_csv(
        "./stopwords.txt",
        index_col=False,
        quoting=3,
        sep="t",
        names=["stopword"],
        encoding="utf-8",
    )
    words_df = words_df[~words_df.segment.isin(stopwords.stopword)]
    # print(words_df)

    # 统计词频
    words_stat = words_df.groupby(by=["segment"])["segment"].agg({"计数": numpy.size})
    words_stat = words_stat.reset_index().sort_values(by=["计数"], ascending=False)
    print(words_stat)

    # 用词云进行显示
    # wordcloud = WordCloud(font_path="./SimHei.ttf", background_color="white", max_font_size=80, width=1000, height=860,
    #                       margin=2)
    wordcloud = WordCloud(
        font_path="./simkai.ttf",
        background_color="white",
        max_font_size=80,
        width=1000,
        height=860,
        margin=2,
    )
    word_frequence = {x[0]: x[1] for x in words_stat.head(1000).values}

    wordcloud = wordcloud.fit_words(word_frequence)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show(block=False)
    img_name = "./" + movieName + ".jpg"
    wordcloud.to_file(img_name)


if __name__ == "__main__":
    # main("26752852", "水形物语")
    # main("26861685", "红海行动")
    # main("4920389", "头号玩家")
    # main("26366496", "邪不压正")
    # main("26752088", "我不是药神")
    # main("27605698", "西虹市首富")
    main("27622447","小偷家族")