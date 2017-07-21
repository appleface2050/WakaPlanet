# coding=utf-8
import os
import sys


def screenshots_modify(screenshots):
    """
    规整截屏
    """
    if screenshots:
        try:
            result = screenshots.split(",")
            return result
        except Exception as e:
            return screenshots


def modify_date_modify(modify_date):
    """
    只留日期
    """
    return modify_date[:10]


def app_size_modify(size):
    """
    app大小规整
    """
    type = {
        0:"B",
        1:"KB",
        2:"MB",
        3:"GB",
        4:"TB",
    }
    count = 0
    while size > 1024:
        size /= 1024.
        count += 1
    try:
        res = "%.01f"%size + type[count]
    except Exception as e:
        res = "0MB"
    return res


def cal_total_page(total_num, res_num):
    return 1 + ((total_num-1) / res_num)


def content_chinese_word(query):
    """
    判断是否含有中文
    """
    # if query == "qq":
    #     return True
    import re
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    match = zhPattern.search(query)
    if match:
        return True
    else:
        return False


def handle_tojson_type(type):
    """
    将type改为合适的数据
    """
    type_tmp = []
    if type.find(",") != -1:
        type = type.split(",")
        for i in type:
            if i.find(":") != -1:
                type_tmp.append(i.split(":")[1])
            else:
                type_tmp.append(i)
    elif type.find(":") != -1:
        type_tmp.append(type.split(":")[1])
    else:
        type_tmp.append(type)
    type = type_tmp
    return type


def sort_game_by_name(res, query):
    """
    根据游戏名字排序

    完全匹配靠前
    1 名字 game_name
    2 完整拼音 pinyin
    3 拼音缩写 initails_pinyin
    """
    order1, order2, order3, last = [], [], [], []
    for game in res:
        if query == game.get("game_name",""):
            order1.append(game)
            continue
        elif query == game.get("pinyin",""):
            order2.append(game)
            continue
        elif query == game.get("initails_pinyin",""):
            order3.append(game)
            continue
        else:
            last.append(game)
    return order1+order2+order3+last


def check_if_download_url_is_game9(origin_download):
    "http://downum.game.uc.cn/download/package/96658-100026081"
    if not origin_download:
        return False
    if origin_download.find("downum.game.uc.cn") != -1:
        return True
    else:
        return False




def make_game9_download_url(origin_download, code):
    try:
        url = origin_download.split("-")[0]
        return url + "-" + code
    except Exception, e:
        #通常是手动进行了下载地址配置，或者没配对
        print e
        return origin_download


def if_result_have_accurate_app(result, query):
    """
    搜索结果的游戏名称是否有精确匹配的
    """
    for i in result:
        if i.get("game_name","") == query.strip():
            return True
    return False
