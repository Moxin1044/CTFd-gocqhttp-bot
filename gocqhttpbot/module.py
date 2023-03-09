from flask import request, render_template, Blueprint, Markup, abort, redirect, url_for, send_from_directory
from CTFd.utils.decorators import admins_only, during_ctf_time_only, require_verified_emails, require_team, authed_only

pages = Blueprint("CTFd GOCQHTTP", __name__, template_folder="templates")
from .gocqDB import view_go_cq_http_config, update_go_cq_http_config, add_go_cq_http_config


def load_page(route, plugin_dir='.'):
    @pages.route(route, methods=['GET', 'POST'])
    @admins_only
    def view_page():
        address = request.args.get("address")
        qqgroup = request.args.get("qqgroup")
        Authorization = request.args.get("Authorization")
        feishutoken = request.args.get("feishutoken")
        type = request.args.get("type")
        submit = request.args.get("submit")

        if submit and address and qqgroup and Authorization and feishutoken and type:
            if view_go_cq_http_config():
                update_go_cq_http_config(address, qqgroup, Authorization, feishutoken, type)
                message = view_go_cq_http_config()
                return render_template("gocqhttp_config.html", gocqaddress=message['address'],
                                       gocqgroupnumber=message['groupid'], gocqAuthorization=message['goauth'],
                                       gocqfeishutoken=message['feishuid'])
            else:
                add_go_cq_http_config(address, qqgroup, Authorization, feishutoken, type)
                message = view_go_cq_http_config()
                return render_template("gocqhttp_config.html", gocqaddress=message['address'],
                                       gocqgroupnumber=message['groupid'], gocqAuthorization=message['goauth'],
                                       gocqfeishutoken=message['feishuid'])
        else:
            if view_go_cq_http_config():
                message = view_go_cq_http_config()
                return render_template("gocqhttp_config.html", gocqaddress=message['address'],
                                       gocqgroupnumber=message['groupid'], gocqAuthorization=message['goauth'],
                                       gocqfeishutoken=message['feishuid'])
            else:
                # message = {"address": "Go-CQ-HTTP听守的地址和端口", "groupid": "通知的QQ群号码", "goauth": "Authorization", "feishuid": "飞书机器人的Token"}
                return render_template("gocqhttp_config.html")
    return pages
