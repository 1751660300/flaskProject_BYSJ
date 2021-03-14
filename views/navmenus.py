# -*- coding:utf-8 -*-
from flask import Blueprint, request
from models import *
import json

nav = Blueprint("nav", __name__, url_prefix='/nav')
p = [{'mid': '0001', 'isuse': False}, {'mid': '0002', 'isuse': False}, {'mid': '0003', 'isuse': False},
     {'mid': '0004', 'isuse': False}, {'mid': '0005', 'isuse': False}, {'mid': '0006', 'isuse': False},
     {'mid': '0007', 'isuse': False}, {'mid': '0008', 'isuse': False}, {'mid': '0009', 'isuse': False},
     {'mid': '0010', 'isuse': False}]
p1 = [{'mid': '0001', 'isuse': False}, {'mid': '0002', 'isuse': True}, {'mid': '0003', 'isuse': True},
      {'mid': '0004', 'isuse': True}, {'mid': '0005', 'isuse': False}, {'mid': '0006', 'isuse': False},
      {'mid': '0007', 'isuse': True}, {'mid': '0008', 'isuse': False}, {'mid': '0009', 'isuse': True},
      {'mid': '0010', 'isuse': True}]


@nav.route("/", methods=['get', 'post'])
def get():
    data = request.form
    data = list(data)[0]
    data = json.loads(data)
    result = []
    print(data)
    if data['roleid'] == '9999':
        return json.dumps({"data": p})
    if data['roleid'] == '0000':
        return json.dumps({"data": p})
    ro = role.query.filter(role.roleid == data['roleid']).first()
    mts = menutem.query.filter(menutem.menutid == ro.menutid).all()
    print(mts)
    for mt in mts:
        result.append({"mid": mt.mid, "isuse": False if mt.isuse == 'Y' else True})
    print(result)
    return json.dumps({"data": result})
