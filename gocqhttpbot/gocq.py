import requests
import datetime  # time()
import json
from .gocqDB import GoCQHttpDB,view_go_cq_http_config


def cq_images(url):
    text = "[CQ:image,file=" + url + ",subType=0]"
    return text


def time():
    curr_time = datetime.datetime.now()
    return curr_time.strftime("%Y年%m月%d日 | %H:%M:%S")


def send_group_msg(qq_gourp_id, text):
    goconfig = view_go_cq_http_config()
    if goconfig:
        ip = goconfig['address']
        auth = goconfig['goauth']
    else:
        ip,auth = "",""
    body = {
        "Authorization": auth
    }
    data = {
        "group_id": qq_gourp_id,
        "message": text
    }
    q = requests.post("http://" + ip + "/send_group_msg", data=data, headers=body)
    print(q.status_code)
    print(q.text)


# 发送飞书卡片消息
def send_feishu_card(feishu_id, title, text, content, url):
    data = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True
            },
            "elements": [{
                "tag": "div",
                "text": {
                    "content": text,
                    "tag": "lark_md"
                }
            }, {
                "actions": [{
                    "tag": "button",
                    "text": {
                        "content": content,
                        "tag": "lark_md"
                    },
                    "url": url,
                    "type": "default",
                    "value": {}
                }],
                "tag": "action"
            }],
            "header": {
                "title": {
                    "content": title,
                    "tag": "plain_text"
                }
            }
        }
    }
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    data = json.dumps(data, ensure_ascii=True).encode("utf-8")
    q = requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/" + feishu_id, data=data,
                      headers=header)
    print(q.status_code)
    print(q.text)


# 发送飞书json(富文本消息)
def send_feishu_json(feishu_id, title, text, a_text, a_href):
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [{
                            "tag": "text",
                            "text": text,
                        },
                            {
                                "tag": "a",
                                "text": a_text,
                                "href": a_href
                            }
                        ]
                    ]
                }
            }
        }
    }
    data = json.dumps(data, ensure_ascii=True).encode("utf-8")
    q = requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/" + feishu_id, data=data,
                      headers=header)
    print(q.status_code)
    print(q.text)


def group_flag_post(challenges_name, challenges_category, challenges_value, username, status):
    s = "  ☆---题目解出---☆  \n题目名称：" + challenges_name + "\n题目分区：" + challenges_category + "\n题目分值：" + challenges_value + "\n提交人：" + username + "\n状态：" + status
    s_feishu = "题目名称：" + challenges_name + "\n题目分区：" + challenges_category + "\n题目分值：" + challenges_value + "\n提交人：" + username + "\n状态：" + status
    # 发送到列表中全部的QQ群
    goconfig = view_go_cq_http_config()
    if goconfig:
        group_id = goconfig['groupid']
        feishu_uuid = goconfig['feishuid']
    else:
        group_id, feishu_uuid = "", ""
    send_group_msg(group_id, s)
    send_feishu_card(feishu_uuid, "☆题目提交☆", s_feishu, "前往平台", "https://www.qsnctf.com/")  # 发送到飞书


def flag_post_too_fast(challenges_name, challenges_category, username, status):
    s = "  !---提交过快---!  \n题目名称：" + challenges_name + "\n题目分区：" + challenges_category + "\n提交人：" + username + "\n状态：" + status
    s_feishu = "题目名称：" + challenges_name + "\n题目分区：" + challenges_category + "\n提交人：" + username + "\n状态：" + status
    # 发送到列表中全部的QQ群
    goconfig = view_go_cq_http_config()
    if goconfig:
        group_id = goconfig['groupid']
        feishu_uuid = goconfig['feishuid']
    else:
        group_id, feishu_uuid = "", ""
    send_group_msg(group_id, s)
    send_feishu_card(feishu_uuid, "-=题目提交过快=-", s_feishu, "前往平台", "https://www.qsnctf.com/")  # 发送到飞书


def flag_error(challenges_name, challenges_category, challenges_value, username, Flag, IP_Address):
    s_feishu = "\n题目名称：" + challenges_name + "\n题目分区：" + challenges_category +"\n题目分数："+challenges_value+ "\n提交人：" + username + "\nFlag为：" + Flag + "\n提交IP地址：" + IP_Address+"\n提交时间："+time()
    goconfig = view_go_cq_http_config()
    if goconfig:
        feishu_uuid = goconfig['feishuid']
    send_feishu_card(feishu_uuid, "*错误的FLAG提交*", s_feishu, "前往平台", "https://www.qsnctf.com/")  # 发送到飞书


def flag_true(challenges_name, challenges_category, challenges_value, username, Flag, IP_Address):
    s_feishu = "\n题目名称：" + challenges_name + "\n题目分区：" + challenges_category + "\n题目分数：" + challenges_value + "\n提交人：" + username + "\nFlag为：" + Flag + "\n提交IP地址：" + IP_Address+"\n提交时间："+time()
    goconfig = view_go_cq_http_config()
    if goconfig:
        feishu_uuid = goconfig['feishuid']
    send_feishu_card(feishu_uuid, "★正确的FLAG提交★", s_feishu, "前往平台", "https://www.qsnctf.com/")  # 发送到飞书


def send_admin_ip(text,ip):
    s_feishu = "有一个"+ text + "的访问，在admin路由中。\nIP："+ip+"\n访问时间："+time()
    goconfig = view_go_cq_http_config()
    if goconfig:
        feishu_uuid = goconfig['feishuid']
    send_feishu_card(feishu_uuid, "★访问到Admin★", s_feishu, "前往平台", "https://www.qsnctf.com/")  # 发送到飞书