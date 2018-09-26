#!/usr/bin/python
# coding: utf-8
import itchat
import os

# import importlib
import pandas as pd
import matplotlib.pyplot as plot
from wordcloud import WordCloud
from pyecharts import Bar, Page, Pie
import jieba

# import sys
# importlib.reload(sys)
# sys.setdefaultencoding("utf-8")

# 获取所有的群聊列表
def getRoomList():
    roomslist = itchat.get_chatrooms()
    return roomslist


# 获取指定群聊的信息
def getRoomMsg(roomName):
    itchat.dump_login_status()
    myroom = itchat.search_chatrooms(name=roomName)
    return myroom


# 统计省份信息
def getProvinceCount(cityCount, countName):
    indexs = []
    counts = []
    for index in cityCount.index:
        indexs.append(index)
        counts.append(cityCount[index])
    page = Page()
    labels = [indexs]
    sizes = [counts]
    attr = indexs
    v1 = counts
    bar = Bar(countName)
    bar.add(
        "地区分布",
        attr,
        v1,
        is_stack=True,
        is_label_show=True,
        is_datazoom_show=True,
        is_random=True,
    )
    page.add(bar)
    bar.show_config()
    bar.render(path="./地区分布.html")


# 制作性别统计图
def getSexCount(sexs, countName):
    labels = [u"男", u"女", u"未知"]
    sizes = [sexs["男"], sexs["女"], sexs["未知"]]
    print(sizes)
    pie = Pie("群性别分布")
    pie.add("", labels, sizes, radius=[40, 75], is_label_show=True)
    pie.render(path="./性别分布.html")

    # colors = ["red", "yellow", "blue", "green"]
    # explode = (0, 0, 0)
    # patches, l_text, p_text = plot.pie(
    #     sizes,
    #     explode=explode,
    #     labels=labels,
    #     colors=colors,
    #     labeldistance=1.1,
    #     autopct="%2.0f%%",
    #     shadow=False,
    #     startangle=90,
    #     pctdistance=0.6,
    # )
    # for t in l_text:
    #     t.set_size = 30
    # for t in p_text:
    #     t.set_size = 20
    # plot.axis("equal")
    # plot.legend(loc="upper left", bbox_to_anchor=(-0.1, 1))
    # # plot.rcParams["font.sans-serif"] = ["./SimHei.ttf"]
    # plot.rcParams["axes.unicode_minus"] = False
    # plot.title(countName)
    # plot.grid()
    # plot.show()


# 制作词云
def makeWorldCount(userName):
    users = []
    for user in userName:
        users.append(user)
    users = ",".join(users)
    print(users)
    # font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
    font = os.path.join(os.path.dirname(__file__), "SimHei.ttf")

    wordcloud = WordCloud(
        font_path=font,
        width=1800,
        height=800,
        min_font_size=4,
        max_font_size=80,
        margin=2,
    ).generate(users)
    plot.figure()
    plot.imshow(wordcloud, interpolation="bilinear")
    plot.axis("off")
    plot.show()


# 获取性别统计
def getSex(df_friends):
    sex = df_friends["Sex"].replace({1: "男", 2: "女", 0: "未知"})
    sexCount = sex.value_counts()
    return sexCount


# 男性个性签名统计
def analyMale(df_friends):
    signature = df_friends[df_friends.Sex == 1]["Signature"]
    signature = signature.unique()
    signature = "".join(signature)
    wordlist_after_jieba = jieba.cut(signature, cut_all=True)
    wl_space_split = " ".join(wordlist_after_jieba)
    # font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
    font = os.path.join(os.path.dirname(__file__), "SimHei.ttf")

    wordcloud = WordCloud(
        font_path=font, max_words=200, max_font_size=50, margin=2
    ).generate(wl_space_split)
    plot.figure()
    plot.imshow(wordcloud, interpolation="bilinear")
    plot.axis("off")
    plot.show()


# 女性个性签名统计
def analyFemale(df_friends):
    signature = df_friends[df_friends.Sex == 2]["Signature"]
    signature = signature.unique()
    signature = "".join(signature)
    wordlist_after_jieba = jieba.cut(signature, cut_all=True)
    wl_space_split = " ".join(wordlist_after_jieba)
    # font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
    font = os.path.join(os.path.dirname(__file__), "SimHei.ttf")
    wordcloud = WordCloud(
        font_path=font, max_words=200, max_font_size=50, margin=2
    ).generate(wl_space_split)
    plot.figure()
    plot.imshow(wordcloud, interpolation="bilinear")
    plot.axis("off")
    plot.show()


def main(room):
    itchat.auto_login(hotReload=True)  # 自动登陆
    roomMsg = getRoomMsg(room)  # 获取指定群聊的信息
    gsq = itchat.update_chatroom(roomMsg[0]["UserName"], detailedMember=True)
    df_friends = pd.DataFrame(gsq["MemberList"])  # 取出其中的用户信息并转为dataframe

    # sexs = getSex(df_friends)  # 获取性别统计
    # getSexCount(sexs, "公司性别统计图")  # 制作性别统计图，第一个参数为性别统计的结果，第二个参数为该图的名称

    # city = df_friends['Province']   #取出省份信息
    # City_count = city.value_counts()[:15]
    # City_count = City_count[City_count.index != '']
    # getProvinceCount(City_count, "位置统计图")     #制作位置统计图，第一个参数为位置统计的结果，第二个参数为该图的名称

    # makeWorldCount(df_friends['NickName'])  #制作词云，传入用户昵称
    # makeWorldCount(signature)

    # analyFemale(df_friends)
    # analyMale(df_friends)


if __name__ == "__main__":
    # room是群名称
    room = "hhh"
    main(room)
