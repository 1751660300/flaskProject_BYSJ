# -*- coding:utf-8 -*-
# 申请单页面
from flask import Blueprint, request, make_response
from models import *
import json
import os
import utils
import shutil


def checkData(data):
    result = ''
    for key, value in data.items():
        if key == 'startdate' and value is None:
            result += "开始时间为空\n"
        if key == 'enddate' and value is None:
            result += "结束时间为空\n"
        if key == 'remark' and value is None:
            result += "出差描述为空\n"
        if key == 'sumamt' and value is None:
            result += "总计为空\n"
        if key == 'staylist':
            for stayid, stay in enumerate(value):
                for staykey, stayvalue in stay.items():
                    if staykey == 'detaildate' and stayvalue is None:
                        result += "第{}项，住宿时间为空\n".format(stayid+1)
                    if staykey == 'address' and stayvalue is None:
                        result += "第{}项，住宿地址为空\n".format(stayid+1)
                    if staykey == 'amount' and stayvalue is None:
                        result += "第{}项，住宿金额为空\n".format(stayid+1)
                    if staykey == 'paddress' and stayvalue is None:
                        result += "第{}项，住宿票据为空\n".format(stayid+1)
        if key == 'carlist':
            for carindex, carvalue in enumerate(value):
                for ckey, cvalue in carvalue.items():
                    if ckey == 'paddress' and cvalue is None:
                        result += "第{}项，用车票据为空\n".format(carindex+1)
                    if ckey == 'detaildate' and cvalue is None:
                        result += "第{}项，用车时间为空\n".format(carindex+1)
                    if ckey == 'startaddress' and cvalue is None:
                        result += "第{}项，用车起点为空\n".format(carindex+1)
                    if ckey == 'endaddress' and cvalue is None:
                        result += "第{}项，用车终点为空\n".format(carindex+1)
                    if ckey == 'amount' and cvalue is None:
                        result += "第{}项，用车金额为空\n".format(carindex+1)
                    if ckey == 'paddress' and cvalue is None:
                        result += "第{}项，用车票据为空\n".format(carindex+1)
        if key == 'lunchlist':
            for luindex, luvalue in enumerate(value):
                for lkey, lvalue in luvalue.items():
                    if lkey == 'paddress' and lvalue is None:
                        result += "第{}项，用餐票据为空\n".format(luindex+1)
                    if lkey == 'detaildate' and lvalue is None:
                        result += "第{}项，用餐时间为空\n".format(luindex+1)
                    if lkey == 'amount' and lvalue is None:
                        result += "第{}项，用餐金额为空\n".format(luindex+1)
                    if lkey == 'paddress' and lvalue is None:
                        result += "第{}项，用餐票据为空\n".format(luindex+1)
    return result


ticket = Blueprint("ticket", __name__, url_prefix='/ticket')


@ticket.route("/saveTicket", methods=["post", "get"])
def saveTicket():
    data = request.form
    # data = list(data)[0]
    print(data)
    data = dict(data)
    print(data)
    filedata = request.files.get("file")
    print(type(filedata), filedata.filename)
    filedata.save("static/imgtemp/{}{}{}{}.{}".format(data['cid'], data['id'], data['fdata'], data['index'],
                                                      filedata.filename.split('.')[1]))
    return '123'


@ticket.route("/deleteTicket", methods=["post", "get"])
def deleteTicket():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    dirs = os.listdir("static/imgtemp/")
    for dir in dirs:
        if dir.find("{}{}".format(data["cid"], data["id"])) != -1:
            os.remove("static/imgtemp/{}".format(dir))
            print("删除成功！！")
        else:
            continue
    return '123'


@ticket.route("/saveTicketInfo", methods=["post", "get"])
def saveTicketInfo():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    if data["state"] == 2:
        result = checkData(data)
        if result != '':
            return json.dumps({"data": result, "result": 500})
    try:
        userInfo = data["userinfo"]
        ticketInfo = data["ticket"]
        staylist = data["ticketdata"]['staylist']
        carlist = data["ticketdata"]['carlist']
        lunchlist = data["ticketdata"]['lunchlist']
        u = users.query.filter(users.id == userInfo["id"]).first()
        if ticketInfo["id"] != "":
            rt = rticket.query.filter(rticket.id == ticketInfo["id"]).first()
            rt.start = ticketInfo["date1"][0:10] if ticketInfo["date1"] != '' else ''
            rt.end = ticketInfo["date2"][0:10] if ticketInfo["date2"] != '' else ''
            rt.remark = ticketInfo["desc"]
            rt.userid = userInfo["id"]
            rt.username = u.username
            rt.cid = userInfo["cid"]
            rt.statue = data["state"]
            rt.sumamt = data["sumamt"],
            rt.submitdate = utils.getNowTime().split(" ")[0],
            rt.transbank = ticketInfo["bank"]
            for index, stay in enumerate(staylist):
                filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "STAY", index)
                newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], stay["value"]["id"],
                                                              'STAY', index)
                if os.path.exists(filePath + 'jpg'):
                    shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                    paddress = newFilePath + 'jpg'
                elif os.path.exists(filePath + 'png'):
                    shutil.copy(filePath + 'png', newFilePath + 'png')
                    paddress = newFilePath + 'png'
                else:
                    paddress = ''
                st = stayinfo.query.filter(stayinfo.id == stay["value"]["id"]).first()
                st.address = stay["value"]["address"]
                st.stime = stay["value"]["amount"]
                st.stime = stay["value"]["detaildate"][0:10] if stay["value"]["detaildate"] != '' else ''
                if paddress != '':
                    st.paddress = paddress
            for index, stay in enumerate(carlist):
                # 路径 staic/img/cid/uid/申请单id/stay[car,lunch]/ord .jpg .png
                # 复制票据到img中
                filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "CAR", index)
                newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], stay["value"]["id"],
                                                              'CAR', index)
                if os.path.exists(filePath + 'jpg'):
                    shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                    paddress = newFilePath + 'jpg'
                elif os.path.exists(filePath + 'png'):
                    shutil.copy(filePath + 'png', newFilePath + 'png')
                    paddress = newFilePath + 'png'
                else:
                    paddress = ''
                ca = carinfo.query.filter(carinfo.id == stay["value"]["id"]).first()
                ca.stime = stay["value"]["detaildate"][0:10] if stay["value"]["detaildate"] != '' else ''
                ca.saddress = stay["value"]["startaddress"]
                ca.eaddress = stay["value"]["endaddress"]
                ca.amount = stay["value"]["amount"]
                if paddress != '':
                    ca.paddress = paddress
                for index, lunch in enumerate(lunchlist):
                    # 路径 staic/img/cid/uid/申请单id/stay[car,lunch]/ord .jpg .png
                    # 复制票据到img中
                    filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "LUNCH", index)
                    newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], lunch["value"]["id"],
                                                                  'LUNCH',
                                                                  index)
                    if os.path.exists(filePath + 'jpg'):
                        shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                        paddress = newFilePath + 'jpg'
                    elif os.path.exists(filePath + 'png'):
                        shutil.copy(filePath + 'png', newFilePath + 'png')
                        paddress = newFilePath + 'png'
                    else:
                        paddress = ''
                    lu = lunchinfo.query.filter(lunchinfo.id == lunch["value"]["id"]).first()
                    lu.stime = lunch["value"]["detaildate"][0:10] if lunch["value"]["detaildate"] != '' else ''
                    lu.amount = stay["value"]["amount"]
                    if paddress != '':
                        lu.paddress = paddress
        else:
            oldRt = rticket.query.order_by(db.desc(rticket.id)).first()
            if oldRt is None:
                newRtId = 1
            else:
                newRtId = oldRt.id + 1

            newRt = rticket(newRtId, 0, 0, 0, ticketInfo["date1"][0:10] if ticketInfo["date1"] != '' else '',
                            ticketInfo["date2"][0:10] if ticketInfo["date2"] != '' else '', ticketInfo["desc"],
                            userInfo["id"],
                            u.username, userInfo["cid"], data["state"], data["sumamt"],
                            utils.getNowTime().split(" ")[0],
                            '', '',
                            ticketInfo["bank"])
            db.session.add(newRt)

            # 处理住宿

            oldStay = stayinfo.query.order_by(db.desc(stayinfo.id)).first()
            if oldStay is None:
                newStayId = 1
            else:
                newStayId = oldStay.id + 1
            for index, stay in enumerate(staylist):
                # 路径 staic/img/cid/uid/申请单id/stay[car,lunch]/ord .jpg .png
                # 复制票据到img中
                newStayId += 1
                filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "STAY", index)
                newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], newRtId, 'STAY', index)
                if os.path.exists(filePath + 'jpg'):
                    shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                    paddress = newFilePath + 'jpg'
                elif os.path.exists(filePath + 'png'):
                    shutil.copy(filePath + 'png', newFilePath + 'png')
                    paddress = newFilePath + 'png'
                else:
                    paddress = ''
                newStay = stayinfo(newStayId, newRtId,
                                   stay["value"]["detaildate"][0:10] if stay["value"]["detaildate"] != '' else '',
                                   stay["value"]["address"],
                                   stay["value"]["amount"], paddress)
                db.session.add(newStay)

            oldCar = carinfo.query.order_by(db.desc(carinfo.id)).first()
            if oldCar is None:
                newCarId = 1
            else:
                newCarId = oldCar.id + 1
            for index, stay in enumerate(carlist):
                # 路径 staic/img/cid/uid/申请单id/stay[car,lunch]/ord .jpg .png
                # 复制票据到img中
                newCarId += 1
                filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "CAR", index)
                newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], newRtId, 'CAR', index)

                if os.path.exists(filePath + 'jpg'):
                    shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                    paddress = newFilePath + 'jpg'
                elif os.path.exists(filePath + 'png'):
                    shutil.copy(filePath + 'png', newFilePath + 'png')
                    paddress = newFilePath + 'png'
                else:
                    paddress = ''
                newCar = carinfo(newCarId, newRtId,
                                 stay["value"]["detaildate"][0:10] if stay["value"]["detaildate"] != '' else '',
                                 stay["value"]["startaddress"],
                                 stay["value"]["endaddress"],
                                 stay["value"]["amount"], paddress)
                db.session.add(newCar)

            oldLunch = carinfo.query.order_by(db.desc(carinfo.id)).first()
            if oldLunch is None:
                newLunchId = 1
            else:
                newLunchId = oldLunch.id + 1

            for index, lunch in enumerate(lunchlist):
                newLunchId += 1
                filePath = "static/imgtemp/{}{}{}{}.".format(userInfo["cid"], userInfo["id"], "LUNCH", index)
                newFilePath = "static/img/{}{}{}{}{}.".format(userInfo["cid"], userInfo["id"], newRtId, 'LUNCH', index)
                if os.path.exists(filePath + 'jpg'):
                    shutil.copy(filePath + 'jpg', newFilePath + 'jpg')
                    paddress = newFilePath + 'jpg'
                elif os.path.exists(filePath + 'png'):
                    shutil.copy(filePath + 'png', newFilePath + 'png')
                    paddress = newFilePath + 'png'
                else:
                    paddress = ''
                newLunch = lunchinfo(newLunchId, newRtId,
                                     lunch["value"]["detaildate"][0:10] if lunch["value"]["detaildate"] != '' else '',
                                     lunch["value"]["amount"], paddress)
                db.session.add(newLunch)
    except Exception as e:
        print(e)
        return json.dumps({"result": 500})
    db.session.commit()
    return json.dumps({"result": 200})


@ticket.route("/getTicketInfo", methods=["post", "get"])
def getTicketInfo():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(data)
    result = []
    urls = []
    if data["state"][0] == '-' and data["state"][1:] != "0":
        tid = data["state"][1:]
        if data["flag"] == "ticket":
            rt = rticket.query.filter(rticket.id == tid).first()
            print(rt)
            if rt is None:
                return json.dumps({"id": "", "date1": "", "date2": "", "desc": "", "tag": 'STAY',
                                   "bank": ""})
            return json.dumps(
                {"id": rt.id, "date1": rt.start.strftime('%Y-%m-%d'), "date2": rt.end.strftime('%Y-%m-%d'),
                 "desc": rt.remark, "tag": 'STAY',
                 "bank": rt.transbank})
        if data["flag"] == "stay":
            sts = stayinfo.query.filter(stayinfo.rticketid == tid).all()
            if len(sts) == 0:
                staydatalist = [{"label": "",
                                 "value": {"id": "", "detaildate": '', "address": '', "amount": '',
                                           "paddress": []}}]
            else:
                staydatalist = [{"label": st.id,
                                 "value": {"id": st.id, "detaildate": st.stime.strftime('%Y-%m-%d'),
                                           "address": st.address, "amount": st.amount,
                                           "paddress": [{"name": st.paddress,
                                                         "url": 'http://127.0.0.1:5000/ticket/getTicketPhoto/' +
                                                                st.paddress.split('/')[2] if
                                                         st.paddress != "" else ''}]}} for st in sts]
            return json.dumps({"data": staydatalist})
        if data["flag"] == "lunch":
            lus = lunchinfo.query.filter(lunchinfo.rticketid == tid).all()
            if len(lus) == 0:
                lunchdatalist = [{"label": "",
                                  "value": {"id": "", "detaildate": "", "amount": "",
                                            "paddress": []}}]
            else:
                lunchdatalist = [{"label": lu.id,
                                  "value": {"id": lu.id, "detaildate": lu.stime.strftime('%Y-%m-%d'),
                                            "amount": lu.amount,
                                            "paddress": [{"name": lu.paddress,
                                                          "url": 'http://127.0.0.1:5000/ticket/getTicketPhoto/' +
                                                                 lu.paddress.split('/')[2] if
                                                          lu.paddress != "" else ''}]}} for lu in lus]
            return json.dumps({"data": lunchdatalist})
        if data["flag"] == 'car':
            cas = carinfo.query.filter(carinfo.rticketid == tid).all()
            if len(cas) == 0:
                cardatalist = [{"label": "",
                                "value": {"id": "", "detaildate": "", "amount": "",
                                          "startaddress": "",
                                          "endaddress": "",
                                          "paddress": []}}]
            else:
                cardatalist = [{"label": ca.id,
                                "value": {"id": ca.id, "detaildate": ca.stime.strftime('%Y-%m-%d'), "amount": ca.amount,
                                          "startaddress": ca.saddress,
                                          "endaddress": ca.eaddress,
                                          "paddress": [{"name": ca.paddress,
                                                        "url": 'http://127.0.0.1:5000/ticket/getTicketPhoto/' +
                                                               ca.paddress.split('/')[2] if
                                                        ca.paddress != "" else ''}]}} for ca in cas]
            return json.dumps({"data": cardatalist})
    if data["flag"] == "ticket":
        if data["state"] == "0":
            rts = rticket.query.filter(rticket.userid == data["id"]).all()
        else:
            rts = rticket.query.filter(rticket.userid == data["id"], rticket.statue == data["state"]).all()
    elif data["flag"] == "check":
        if data["state"] == "0":
            rts = rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '2').all()
            rts.extend(rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '3').all())
            rts.extend(rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '5').all())
        else:
            rts = rticket.query.filter(rticket.cid == data["cid"], rticket.statue == data["state"]).all()
            if data["state"] == "3":
                rts.extend(rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '5').all())
    elif data.get("flag") == 'trans':
        if data["state"] == "0":
            rts = rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '3').all()
            rts.extend(rticket.query.filter(rticket.cid == data["cid"], rticket.statue == '4').all())
        else:
            rts = rticket.query.filter(rticket.cid == data["cid"], rticket.statue == data["state"]).all()
    else:
        rts = []
    for rt in rts:
        rtData = rt.getJson()
        sts = stayinfo.query.filter(stayinfo.rticketid == rt.id).all()
        rtData["staylist"] = [st.getJson() for st in sts]
        urls.extend(['http://127.0.0.1:5000/ticket/getTicketPhoto/' + st.getJson()["paddress"].split('/')[2] if
                     st.getJson()["paddress"] != "" else '' for st in sts])
        lus = lunchinfo.query.filter(lunchinfo.rticketid == rt.id).all()
        rtData["lunchlist"] = [lu.getJson() for lu in lus]
        urls.extend(['http://127.0.0.1:5000/ticket/getTicketPhoto/' + lu.getJson()["paddress"].split('/')[2] if
                     lu.getJson()["paddress"] != "" else '' for lu in lus])
        cas = carinfo.query.filter(carinfo.rticketid == rt.id).all()
        rtData["carlist"] = [ca.getJson() for ca in cas]
        urls.extend(['http://127.0.0.1:5000/ticket/getTicketPhoto/' + ca.getJson()["paddress"].split('/')[2] if
                     ca.getJson()["paddress"] != "" else '' for ca in cas])
        result.append(rtData)
    print(result)
    return json.dumps({"data": result, "urls": urls})


@ticket.route("/getTicketPhoto/<string:filename>", methods=["post", "get"])
def getTicketPhoto(filename):
    print(filename)
    if os.path.exists("static/img/{}".format(filename)):
        image_data = open("static/img/{}".format(filename), "rb").read()
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return 'error'


@ticket.route("/submitTicket", methods=["post", "get"])
def submitTicket():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    print(str(data))
    result = ""
    if data.get("result") != 'F':
        result = checkData(data)
    if result == "":
        rt = rticket.query.filter(rticket.id == data["id"]).first()
        if rt is not None:
            if data.get("flag") == 'check' and data.get("result") == 'F':
                rt.statue = 5
                result = '退回成功！！！'
            else:
                rt.statue = data["state"]+1
                result = "提交成功！！！"
        else:
            result = "提交失败，联系管理员！！！"
    db.session.commit()
    return json.dumps({"data": result})


@ticket.route("/pay", methods=["post", "get"])
def pay():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    newTransId = 1
    print(str(data))
    try:
        us = users.query.filter(users.id == data["userid"]).first()
        rt = rticket.query.filter(rticket.id == data.get("id")).first()
        rt.statue = 4
        oldTr = transhis.query.order_by(db.desc(transhis.id)).first()
        if oldTr is not None:
            newTransId = int(oldTr.id)+1
        tr = transhis(newTransId,rt.id,data["sumamt"],rt.transbank,utils.getNowTime().split(" ")[0],data["userid"],us.username)
        db.session.add(tr)
        db.session.commit()
    except Exception as e:
        print(e.args)
        return json.dumps({"code": 500, "result": "转账失败！！！"})
    return json.dumps({"code": 200, "result": "转账成功！！！"})
