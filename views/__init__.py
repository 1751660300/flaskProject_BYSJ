# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


db = SQLAlchemy()


def init_app():
    global db
    app = Flask(__name__, static_folder="static/img/")
    app.config.from_object('setting.config')
    db.init_app(app)

    from . import login
    from . import showData
    from . import my
    from . import roles
    from . import accmanage
    from . import navmenus
    from . import Requisition
    # 登录页面
    app.register_blueprint(login.appLogin)
    # 数据展示页面
    app.register_blueprint(showData.appShowData)
    # 个人信息
    app.register_blueprint(my.my)
    # 角色管理
    app.register_blueprint(roles.appRoles)
    # 账号管理
    app.register_blueprint(accmanage.accm)

    # 账号权限
    app.register_blueprint(navmenus.nav)
    # 填写报销单
    app.register_blueprint(Requisition.ticket)

    return app
