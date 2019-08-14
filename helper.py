#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 19-7-4 下午5:55
# @Author  : Hubery
# @File    : helper.py
# @Software: PyCharm

import time
import requests
from requests.exceptions import ConnectionError

from settings import BASE_HEADERS


def retry(max_tries=3, wait=5):
    """
    获取失败，进行再次爬取
    :param max_tries: 失败次数
    :param wait: 每次失败时等待时间
    :return:
    """
    def deco(fun):
        def wrapper(*args, **kwargs):
            for i in range(max_tries):
                result = fun(*args, **kwargs)
                if result is None:
                    print('retry%s' %i)
                    time.sleep(wait)
                    continue
                else:
                    return result
        return wrapper
    return deco


@retry()
def get_text(url, options={}):
    """
    :param method: 请求方法
    :param url: 请求的目标url
    :param options:添加的请求头
    :return:
    """
    headers = dict(BASE_HEADERS, **options)
    print('正在抓取------>💪💪💪')
    try:
        res = requests.get(url, headers=headers, timeout=5)
        # print(res.status_code)
        if res.status_code == 200:
            print('抓取成功------>😊😊😊')
            return res
    except ConnectionError:
        print('抓取失败(灬ꈍ ꈍ灬)，请重试')
        return None


# 参考链接http://qinxuye.me/article/mid-and-url-in-sina-weibo/
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num


def url_to_mid(url):
    url = str(url)[::-1]
    size = len(url) // 4 if len(url) % 4 == 0 else len(url) // 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))
