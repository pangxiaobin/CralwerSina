
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/8/13 16:37
# @Author  : Hubery
# @File    : crawler_sina.py
# @Software: PyCharm

import re
import json
from helper import get_text, url_to_mid


url = 'https://weibo.com/1926909715/I22YbxDwU?ref=home&rid=0_0_8_3068432500071398696_0_0_0&type=comment#_rnd1565688908814'


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
        if script_context.__len__() >=2:
            rule_2 = r'var \$render_data = (.*?)\|\|'
            render_data = re.findall(rule_2, script_context[1], re.DOTALL)
            data_dict = render_data[0].replace('[0]', '')
            status = json.loads(data_dict)[0].get('status', '')
            if status:
                return status
            return False
        return False
    return False


def write_context(status):
    if status:
        created_at = status.get('created_at', '')
        text = status.get('text', '')
        user = status.get('user', '')
        if user:
            user_name = user.get('screen_name', '')  # 用户名
            verified = user.get('verified', '')  # 是否认证
            verified_reason = user.get('verified_reason', '')  # 认证描述
            followers_count = user.get('followers_count', '')  # 关注量
        reposts_count = status.get('reposts_count', '')   # 转发量
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
        s = '发布时间:{},正文：{}, 用户名：{}, 转发量：{},评论量:{}' \
            '点赞量：{}'.format(created_at, script_html(text), user_name, reposts_count, comments_count, attitudes_count)
        print(s)


def script_html(context):
    pat = re.compile('<[^>]+>', re.S)
    return pat.sub('', context)


if __name__ == '__main__':
    mid = get_mid(url)
    status = get_response(mid)
    write_context(status)