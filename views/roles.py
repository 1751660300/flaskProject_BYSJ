# -*- coding:utf-8 -*-
# 角色管理模块
from flask import Blueprint, request
import json
from models import *
import utils

appRoles = Blueprint("roles", __name__, url_prefix='/roles')


# 获取公司的角色信息
@appRoles.route("/getRolesInfo", methods=["get", "post"])
def getRolesInfo():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    roleInfo = []
    print(data)
    if data["roleid"] == "9999":
        ro = role.query.filter(role.cid == data["cid"]).all()
        for i in ro:
            roleInfo.append(i.getJson())
    else:
        return json.dumps({"data": []})
    print(roleInfo)
    return json.dumps({"data": roleInfo})


@appRoles.route("/getMenuOptions", methods=["get", "post"])
def getMenuOptions():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    result = []
    mt = menutem.query.filter(menutem.cid == data["cid"]).with_entities(menutem.menutid, menutem.menutname).distinct().all()
    print(mt, type(mt))
    for i in mt:
        result.append({"value": i[0], "label": i[1]})
    return json.dumps(result)


@appRoles.route("/getFreeOptions", methods=["get", "post"])
def getFreeOptions():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    result = []
    mt = free.query.filter(free.cid == data["cid"]).with_entities(free.freeid, free.freename).distinct().all()
    print(mt, type(mt))
    for i in mt:
        result.append({"value": i[0], "label": i[1]})
    return json.dumps(result)


@appRoles.route("/updateRoles", methods=["get", "post"])
def updateRoles():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)

    ro = role.query.filter(role.roleid == data["roleid"], role.cid == data["cid"]).first()
    if ro is not None:
        ro.menutid = data["menutid"]
        ro.freeid = data["freeid"]
        ro.enddate = utils.getNowTime()
        db.session.commit()
        print(ro)
    else:
        return json.dumps({"result": 404})
    return json.dumps({"result": 200})


@appRoles.route("/addRoles", methods=["get", "post"])
def addRoles():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    try:
        ro = role.query.filter(role.roleid != '9999').order_by(db.desc(role.roleid)).first()
        newRoleid = int(ro.roleid) + 1
        print(newRoleid)
        newRo = role(newRoleid, data["name"], data["cid"], data["menuvalue"], data["freevalue"], utils.getNowTime(),
                     data["desc"])
        db.session.add(newRo)
        db.session.commit()
    except Exception as e:
        print(e)
        return json.dumps({"result": 500})
    return json.dumps({"result": 200})


@appRoles.route("/deleteRoles", methods=["get", "post"])
def deleteRoles():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    try:
        role.query.filter(role.roleid == data["roleid"], role.cid == data["cid"]).delete()
        db.session.commit()
    except:
        return json.dumps({"result": 500})
    return json.dumps({"result": 200})


@appRoles.route("/getFrees", methods=["get", "post"])
def getFrees():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    result = {}
    print(data)
    fr = free.query.filter(free.cid == data["cid"]).all()
    if fr is None:
        return json.dumps(result)
    for i in fr:
        if result.get(i.freeid) is None:
            result[i.freeid] = [{"fname": i.fname, "maxamt": i.maxamt, "comment": i.comment, "ford": i.ford}]
        else:
            result[i.freeid].append({"fname": i.fname, "maxamt": i.maxamt, "comment": i.comment, "ford": i.ford})
    return json.dumps(result)


@appRoles.route("/saveFree", methods=["get", "post"])
def saveFree():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    tempName = data[len(data) - 1]
    if tempName["newtempname"] == "":
        for i in range(len(data) - 1):
            if data[i]["ford"] != "":
                fr = free.query.filter(free.ford == data[i]["ford"],
                                       free.freeid == tempName["tempname"]["value"]).first()
                fr.fname = data[i]["fname"]
                fr.maxamt = data[i]["maxamt"]
                fr.comment = data[i]["comment"]
            else:
                fr = free.query.filter(free.freeid == tempName["tempname"]["value"]).order_by(
                    db.desc(free.ford)).first()
                newFree = free(tempName["tempname"]["value"], tempName['cid'], tempName["tempname"]["label"],
                               data[i]["fname"], data[i]["maxamt"], data[i]["comment"], fr.ford + 1)
                db.session.add(newFree)
    else:
        FR = free.query.filter().order_by(db.desc(free.freeid)).first()
        newFreeid = str(int(FR.freeid if FR is not None else '0') + 1)
        for i in range(len(data) - 1):
            fr = free.query.filter(free.freeid == newFreeid).order_by(
                db.desc(free.ford)).first()
            if fr is None:
                newFree = free(newFreeid, tempName['cid'], tempName["newtempname"],
                               data[i]["fname"], data[i]["maxamt"], data[i]["comment"], 0)
            else:
                newFree = free(newFreeid, tempName['cid'], tempName["newtempname"],
                               data[i]["fname"], data[i]["maxamt"], data[i]["comment"], fr.ford + 1)
            db.session.add(newFree)
    db.session.commit()
    return json.dumps({"result": 200})


# 获取公司菜单信息
@appRoles.route("/getMenus", methods=["get", "post"])
def getMenus():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    result = {}
    print(data)
    fr = menutem.query.filter(menutem.cid == data["cid"]).all()
    if fr is None:
        return json.dumps(result)
    for i in fr:
        me = menu.query.filter(menu.mid == i.mid).first()
        menus = i.getJson()
        menus["menuname"] = me.mname
        menus["comment"] = me.comment
        if result.get(i.menutid) is None:

            result[i.menutid] = [menus]
        else:
            result[i.menutid].append(menus)
    return json.dumps(result)


@appRoles.route("/saveMenuTemp", methods=["get", "post"])
def saveMenuTemp():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    tempName = data[len(data) - 1]
    print(data)
    if tempName["newtempname"] == "":
        for i in range(len(data) - 1):
            if data[i]["mord"] != "":
                me = menutem.query.filter(menutem.mord == data[i]["mord"],
                                          menutem.menutid == tempName["tempname"]["value"]).first()
                me.mid = data[i]["mid"]
                me.isuse = "Y" if data[i]["isuse"] == True else "N"
            else:
                me = menutem.query.filter(menutem.menutid == tempName["tempname"]["value"]).order_by(
                    db.desc(menutem.mord)).first()
                newMe = menutem(tempName["tempname"]["value"], data[i]["mid"], tempName['cid'],tempName["tempname"]["label"],
                                "Y" if data[i]["isuse"] == True else "N",
                                me.mord + 1)
                db.session.add(newMe)
    else:
        MR = menutem.query.filter().order_by(db.desc(menutem.menutid)).first()
        newmenutid = str(int(MR.menutid if MR is not None else '0') + 1)
        for i in range(len(data) - 1):
            me = menutem.query.filter(menutem.menutid == newmenutid).order_by(
                db.desc(menutem.mord)).first()
            if me is None:
                # menutid, mid, cid, menutname, isuse, mord
                newFree = menutem(newmenutid, data[i]["mid"], tempName['cid'], tempName["newtempname"],
                                  "Y" if data[i]["isuse"] == True else "N", 0)
            else:
                newFree = menutem(newmenutid, data[i]["mid"], tempName['cid'], tempName["newtempname"],
                               "Y" if data[i]["isuse"] == True else "N", me.mord + 1)
            db.session.add(newFree)
    db.session.commit()
    return json.dumps({"result": 200})


@appRoles.route("/getMenu", methods=["get", "post"])
def getMenu():
    result = []
    m = menu.query.all()
    if m is None:
        return json.dumps(result)
    for i in m:
        menus = i.getJson()
        result.append(menus)
    return json.dumps({"data": result})
