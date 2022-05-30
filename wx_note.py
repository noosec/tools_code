#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码编写: evilzz
邮箱地址: info@noosec.com
创建日期: 2022/5/29 11:51 
模块说明:
"""

import requests, sys


def push_wechat_msg(webhook_key, content):
    """
    wx webhook 消息推送模块
    参考文档：https://developer.work.weixin.qq.com/document/path/91770

    :param webhook_url:  机器人地址
    :param content: 要发送的消息
    :return:
    """
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    content = f"**<font color=\"warning\"># 新增漏洞提醒</font>**\n{content}"
    # 要发送的消息体
    payload_json = {
        "msgtype": "markdown",
        "markdown": {
            # 文本内容，最长不超过2048个字节，必须是utf8编码
            "content": content,
            # userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人
            "mentioned_list": ["@all"]
        }
    }

    # 发送消息
    resp = requests.post(webhook_url, json=payload_json)

    if resp.json()["errcode"] == 0:
        print('webhook 消息推送成功，请查收！')
    else:
        print(f"webhook 消息推送失败, {resp.text}")


def post_file(webhook_key, file_name):
    """
    通过webhook 向wx 发送消息，上传文件，大小限制20M
    :param webhook_key:  webhook key
    :param file_name:  要上传的文件
    :return:
    """
    # 上传文件到wx 临时平台，获取到media_id,用于向机器人发送，有效期3天

    file_data = {'file': open(file_name, 'rb')}

    # 请求id_url(将文件上传微信临时平台),返回media_id
    id_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webhook_key}&type=file"

    response = requests.post(url=id_url, files=file_data)
    json_res = response.json()
    media_id = json_res['media_id']

    # 通过wx机器人发送消息到群里

    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    post_data = {"msgtype": "file",
            "file": {"media_id": media_id}
            }
    result = requests.post(url=webhook_url, json=post_data)

    if result.json()["errcode"] == 0:
        print('webhook 文件推送成功，请查收！')
    else:
        print(f"webhook 文件推送失败, {result.json()}")



if __name__ == '__main__':
    # 这里修改为自己机器人的webhook地址
    webhook_key = "3c85dc21-6216-4a24-xxxxce7"

    obj_file = sys.argv[1]
    with open(obj_file) as f:
        data = f.read()

    # 读取文件，将内容发送到wx， post 最长不超过4096个字节，必须是utf8编码
    push_wechat_msg(webhook_key, str(data))

    # 直接传文件到wx，适用于文件内容过多
    post_file(webhook_key, "target.txt")
