# -*- coding:utf-8 -*-
from flask import Blueprint, request
from models import *
import json

accm = Blueprint("accm", __name__, url_prefix='/accm')


@accm.route("/getAccs", methods=["get", "post"])
def getAccs():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    result = []
    acs = accountinfo.query.filter(accountinfo.company == data['cid']).all()
    for ac in acs:
        us = users.query.filter(users.id == ac.id).first()
        ro = role.query.filter(role.roleid == ac.role).first()
        if us is not None:
            result.append({"acc": ac.id, "name": us.username, "roleid": ac.role, "rolename": ro.rolename})
        else:
            result.append({"acc": ac.id, "name": '', "roleid": ac.role, "rolename": ro.rolename})
    return json.dumps({"data": result})


@accm.route("/getRoles", methods=["get", "post"])
def getRoles():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    result = []
    ros = role.query.filter(role.cid == data["cid"]).all()
    for ro in ros:
        result.append({"value": ro.roleid, "label": ro.rolename})
    result.append({"value": "0000", "label": "默认"})
    result.append({"value": "9999", "label": "超级管理员"})
    return json.dumps({"data": result})


@accm.route("/updateAcc", methods=["get", "post"])
def updateAcc():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    ac = accountinfo.query.filter(accountinfo.id == data['acc']).first()
    ac.role = data["roleid"]
    db.session.commit()
    return json.dumps({"result": 200})
