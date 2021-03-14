# -*- coding:utf-8 -*-
# 个人信息
from flask import Blueprint, request
from models import *
import json

my = Blueprint("my", __name__, url_prefix='/my')


@my.route("/getUserinfo", methods=['get', 'post'])
def getUserinfo():
    data = request.form
    print(data.get('id'))
    try:
        u = users.query.get(data.get('id'))
        jsondata = u.getJson()
    except:
        return json.dumps({})
    return jsondata


@my.route("/getBanks", methods=['get', 'post'])
def getBanks():
    data = request.form
    jsondata = {}
    b = banks.query.filter(banks.id == data.get('id')).all()
    if b is not None:
        for i, j in enumerate(b):
            jsondata["卡{}".format(i + 1)] = j.bid
    return json.dumps(jsondata)


@my.route("/saveUserinfo", methods=['get', 'post'])
def saveUserinfo():
    data = request.form
    data = list(data)
    data = json.loads(data[0])
    print(data)
    u = users.query.get(data.get('id'))
    if u is not None:
        u.username = data.get("name")
        u.sex = data.get("detail").get("性别")
        u.phone = data.get("detail").get("手机号")
        u.age = data.get("detail").get("年龄")
        u.presonid = data.get("detail").get("身份证号")
    else:
        u = users(data.get('id'),
                  data.get("name"),
                  data.get("detail").get("性别"),
                  data.get("detail").get("年龄"),
                  data.get("detail").get("手机号"),
                  data.get("detail").get("身份证号"))
        db.session.add(u)
    db.session.commit()
    return json.dumps({"result": "ok"})


@my.route("/saveBanks", methods=['get', 'post'])
def saveBanks():
    data = request.form
    data = list(data)
    data = json.loads(data[0])
    # print(data)
    try:
        b = banks.query.filter(banks.id == data.get('id')).all()
        # print(b, '2222222')
        if len(b) != 0:
            for i, j in enumerate(b):
                j.bid = data['banks']['卡' + str(i + 1)]
        else:
            b = banks.query.order_by(db.desc(banks.bord)).first()
            newBord = b.bord
            print(b.bord)
            for i, j in data['banks']:
                newBord += 1
                newBanks = banks(newBord, data.get('id'), j)
                db.session.add(newBanks)
        db.session.commit()
    except Exception as e:
        print(e)
        return json.dumps({"result": "err"})
    return json.dumps({"result": "ok"})
