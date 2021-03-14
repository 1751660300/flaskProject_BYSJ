# -*- coding:utf-8 -*-
from flask import Blueprint

appShowData = Blueprint("showData", __name__)


@appShowData.route("/showData", methods=('post', 'get'))
def showData():
    pass
