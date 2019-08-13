# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 16:37
# @Author  : Hubery
# @File    : crawler_sina.py
# @Software: PyCharm

import re
import json
from datetime import datetime
from dateutil.parser import parse
import os
from helper import get_text, url_to_mid

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# url = 'https://weibo.com/1926909715/I22YbxDwU?ref=home&rid=0_0_8_3068432500071398696_0_0_0&type=comment#_rnd1565688908814'


def get_mid(url):
    re_rule = 'https:\/\/weibo\.com\/\d+\/(\w+?)\?'
    base62_url = re.findall(re_rule, url)
    if base62_url:
        return url_to_mid(base62_url[0])
    return None


def get_response(mid):
    url = 'https://m.weibo.cn/detail/{}'.format(mid)
    response = get_text(url=url)
    if response:
        context = response.text
        rule_1 = r'<script>.*?</script>'
        script_context = re.findall(rule_1, context, re.DOTALL)
        if script_context.__len__() >= 2:
            rule_2 = r'var \$render_data = (.*?)\|\|'
            render_data = re.findall(rule_2, script_context[1], re.DOTALL)
            data_dict = render_data[0].replace('[0]', '')
            status = json.loads(data_dict)[0].get('status', '')
            if status:
                return status
            return False
        return False
    return False


def get_context(status):
    if status:
        ren_zheng = '普通用户'
        created_at = status.get('created_at', '')
        if created_at:
            created_at = datetime.strftime(parse(created_at), '%Y-%m-%d %H:%M:S')
        text = status.get('text', '')
        if text:
            text = script_html(text)
        user = status.get('user', '')
        if user:
            user_name = user.get('screen_name', '')  # 用户名
            verified = user.get('verified', '')  # 是否认证
            if verified:
                ren_zheng = '金V认证'
            verified_reason = user.get('verified_reason', '')  # 认证描述
            followers_count = user.get('followers_count', '')  # 粉丝量
        reposts_count = status.get('reposts_count', '')  # 转发量
        comments_count = status.get('comments_count', '')  # 评论量
        attitudes_count = status.get('attitudes_count', '')  # 点赞量
        image_url_list = []
        # 配图
        pic_num = status.get('pic_num', '')
        pics = status.get('pics', '')
        if pic_num and len(pics) > 0:
            for i in pics:
                image_url = i.get('url')
                image_url_list.append(image_url)
        s = '{}\n{}\n发布时间：{}\n发布情况：{},{},粉丝量：{}\n转发：{},评论：{},点赞{}\n'.format(user_name, text, created_at,
                                                                            ren_zheng, verified_reason, followers_count,
                                                                            reposts_count, comments_count,
                                                                            attitudes_count)
        return s


def script_html(context):
    """
    去除html标签
    :param context: 字符串
    :return: 去除html的结果
    """
    pat = re.compile('<[^>]+>', re.S)
    return pat.sub('', context)


def run():
    while True:
        print('输入q退出')
        url = input('请输入微博连接：')
        date_type = input('请输入类型')
        if url == 'q' or date_type == 'q':
            break
        mid = get_mid(url)
        status = get_response(mid)
        result = get_context(status)
        tem = '{}\n'.format(date_type) + result + '{}\n'.format(url)
        write_context(tem)


def write_context(string):
    dirname = 'result'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    result_path = os.path.join(BASE_DIR, dirname)
    file_name = '{}.txt'.format(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    file_path = os.path.join(result_path, file_name)
    with open(file_path, 'a+', encoding='utf8') as f:
        f.write(string + '\n')


if __name__ == '__main__':
    run()
