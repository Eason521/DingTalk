# -*- coding:utf-8 -*-
# Author : Tany
# Date :2020-4-29
from bs4 import BeautifulSoup
import random
import requests
import json
import time

password = input('请输入启动密码：')
while password != 'kkb':
    password = input('密码错误，请重新输入输入启动密码或直接关闭退出：')

# 构造机器人列表
access_token_num = int(input('请输入机器人个数：'))
access_token_list = []
for i in range(access_token_num):
    access_token = input('请输入机器人链接：')
    access_token_list.append(access_token)

url = input('请输入石墨链接：')
"""定义开始语句艾特所有人"""


def sendmessage_start(access_token, message):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token  # 钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = message
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


"""发送内容"""


def sendmessage_content(access_token, message):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = message
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 0  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


"""实现发送链接"""


def sendmessage_link(access_token, message):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    Link_textMsg = {
        "msgtype": "link",
        "link": {
            "text": " https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png",
            "title": " ",
            "picUrl": "https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png",
            "messageUrl": "https://uploader.shimo.im/f/qtMrUTT2hdQgguKL.png"
        }
    }
    Link_textMsg = json.dumps(Link_textMsg)
    res = requests.post(url, data=Link_textMsg, headers=HEADERS)
    print(res.text)


"""实现发送图片"""


def sendmessage_image(access_token, src):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % (access_token)

    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    Image_textMsg = {
        "msgtype": "markdown",
        "markdown": {
            "title": "知识点",
            "text": "![](%s)" % src,
        },
        "at": {
            "atMobiles": [
                ""
            ],
            "isAtAll": 0
        }
    }
    Image_textMsg = json.dumps(Image_textMsg)
    res = requests.post(url, data=Image_textMsg, headers=HEADERS)
    print(res.text)


"""结束语"""


def sendmessage_stop(access_token, ):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s' % access_token  # 钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = """以上就是我们今天分享的内容"""
    String_textMsg = {
        "msgtype": "text",
        "text": {"content": message},
        "at": {
            "atMobiles": [
                ""  # 如果需要@某人，这里写他的手机号
            ],
            "isAtAll": 1  # 如果需要@所有人，这些写1
        }
    }
    String_textMsg = json.dumps(String_textMsg)
    res = requests.post(url, data=String_textMsg, headers=HEADERS)
    print(res.text)


"""
爬取石墨文档
"""

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

res = requests.get(url, headers=headers).content.decode('utf-8')
# print(res)
# with open(r'F:\Pythonwork\Person\钉钉机器人\zhishidian.html', 'w', encoding='utf-8') as f:
#     f.write(res)

bs = BeautifulSoup(res, 'html.parser')

# 获取标题
title = bs.find('div', class_='ql-title').find(class_='ql-title-box')['data-value']
print(title)
print('-' * 100)
# 获取内容
content_list = bs.find('div', class_='ql-editor')

"""
调用方法开始发送消息
"""
# 遍历所有的access_token
for access_token in access_token_list:
    """开局艾特所有人"""
    message = """今日知识点分享来啦
        """
    sendmessage_start(access_token, message)
    time.sleep(10)
    """
    解析数据发送分享内容
    """
    for content in content_list.children:
        num = random.randint(6, 10)
        try:
            res = content.find('img')
            res = res['src']  # 获取图片链接
            if res:
                sendmessage_image(access_token, res)
                # print(res)
                # print('发送图片')

                time.sleep(num)
            else:
                pass
        except Exception as e:
            res = content.text  # 获取正常文字
            if res:
                # print('************', res)
                sendmessage_content(access_token, res)
                time.sleep(num)
                # print('=========' * 100)
                # print(e)
                # print('=========' * 100)
            else:
                pass
        # print(res)

    sendmessage_stop(access_token)
    print('一个群发送完成')
print('所有发送完成')
