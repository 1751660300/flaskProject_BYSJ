# -*- coding:utf-8 -*-
from flask import Blueprint, request
import json
from models import *
from redis import Redis

"""
    登录页面存在三个组件（可只完成登录，注册两个组件）
"""
tokens = {}
r = Redis()
appLogin = Blueprint("login", __name__, url_prefix='/login')


@appLogin.route("/", methods=('post', 'get'))
def login():
    global tokens
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(type(data), data)
    acc = accountinfo.query.filter(accountinfo.company == data["company"], accountinfo.id == data["username"]).first()
    if acc is None:
        return json.dumps({"code": "404", "data": {"token": ""}})
    else:
        print(acc.pwd)
        if acc.pwd != data["password"]:
            return json.dumps({"code": "500", "data": {"token": ""}})
    print("logined!!!")
    # tokens[acc.id] = {"id": acc.id, "cid": acc.company, "roleid": acc.role}
    r.set(acc.id, json.dumps({"id": acc.id, "cid": acc.company, "roleid": acc.role}), nx=86400)
    return json.dumps({"code": "200", "data": {"token": acc.id, "roleid": acc.role}})


@appLogin.route("/getinfo", methods=('post', 'get'))
def getinfo():
    data = request.args
    data = dict(data)
    print(data)
    try:
        if data["token"] is not None:
            u = r.get(data.get("token"))
            # return json.dumps({"code": 20000, "userinfo": tokens[data["token"]]})
            return json.dumps({"code": 20000, "userinfo": json.loads(u)})
        print("getinfo!!!")
    except:
        return json.dumps({"code": 50008})
    return json.dumps({"code": 50012})


@appLogin.route("/logout", methods=('post', 'get'))
def logout():
    data = request.args
    data = dict(data)
    print(data)
    return json.dumps({"code": 20000, "message": ""})


@appLogin.route("/getCompany", methods=('post', 'get'))
def getCompany():
    com = companyinfo.query.all()
    print(com)
    data = []
    for i in com:
        data.append({"value": i.cname, "cid": i.cid})
    return json.dumps({"data": data})


@appLogin.route("/register", methods=('post', 'get'))
def register():
    data = request.form
    data = dict(data)
    roleid = '0000'
    if len(data) == 0:
        return json.dumps({"data": False})
    else:
        try:
            print(data, type(data))
            if data["cid"] == '':
                com = companyinfo.query.filter(companyinfo.cname == data['company']).first()
                data['cid'] = com.cid if com is not None else ''
            if data["cid"] == '':
                # 添加新公司，并注册账号
                com = companyinfo.query.order_by(db.desc(companyinfo.cid)).first()
                if com is None:
                    data["cid"] = 20210001
                else:
                    data["cid"] = str(int(com.cid) + 1)
                newCom = companyinfo(data["cid"], data["company"])
                db.session.add(newCom)
                roleid = "9999"
            # 为已有的公司注册账号
            com = companyinfo.query.filter(companyinfo.cid == data.get("cid")).first()
            print(com, "注册账号")
            if com is not None:
                acc = accountinfo(data["username"], data["password"], roleid, data["cid"])
                db.session.add(acc)
        except Exception as e:
            print(e)
            return json.dumps({"data": False})
    db.session.commit()
    return json.dumps({"data": True})
