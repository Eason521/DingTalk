# -*- coding:utf-8 -*-
# @Author : Tany
# @Date : 2020-5-18


import json
import time
import hmac
import hashlib
import base64
import requests
import urllib.parse

timestamp = str(round(time.time() * 1000))
# secret = 'this is secret'
secret = 'SECf86497abfba4b29e03723421edfca4fa6cc2cb1725170454a8f3f2cf46013a50'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
# print(timestamp)
# print(sign)

access_token = input('请输入机器人链接：')


def sendmessage_start(access_token):
    """
    定义艾特所有人
    """
    url = 'https://oapi.dingtalk.com/robot/send?access_token=%s&timestamp=%s&sign=%s' % (
        access_token, timestamp, sign)  # 钉钉机器人的webhook地址
    HEADERS = {
        "Content-Type": "application/json ;charset=utf-8 "
    }
    message = """
        今日知识点分享来啦
    """
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
    # print(res.text)


sendmessage_start(access_token)
