# -*- coding:utf-8 -*-
from views import db

'''
    修改模型记得修改数据库
'''
state = {1:"待处理", 2:"待审批", 3:"待转账", 4:"已完成", 5:"退回"}


# 创建模板
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.CHAR(6), primary_key=True)
    username = db.Column(db.VARCHAR(20))
    sex = db.Column(db.CHAR(1))
    age = db.Column(db.Integer)
    phone = db.Column(db.VARCHAR(11))
    presonid = db.Column(db.VARCHAR(20))

    def __init__(self, id, username, sex, age, phone, presonid):
        self.username = username
        self.id = id
        self.sex = sex
        self.age = age
        self.phone = phone
        self.presonid = presonid

    def getJson(self):
        return {"username": self.username, "detail": {
            '性别': self.sex,
            '年龄': self.age,
            '手机号': self.phone,
            '身份证号': self.presonid
        }}


# 账户信息表
class accountinfo(db.Model):
    __tablename__ = 'accountinfo'
    id = db.Column(db.CHAR(6), primary_key=True)
    pwd = db.Column(db.CHAR(8), nullable=False)
    role = db.Column(db.CHAR(4), nullable=False)
    company = db.Column(db.CHAR(8), nullable=False)

    def __init__(self, id, pwd, role, company):
        self.id = id
        self.pwd = pwd
        self.role = role
        self.company = company


# 公司信息
class companyinfo(db.Model):
    __tablename__ = 'companyinfo'
    cid = db.Column(db.CHAR(8), primary_key=True)
    cname = db.Column(db.VARCHAR(200), nullable=False)

    def __init__(self, cid, cname):
        self.cid = cid
        self.cname = cname


# 角色表
class role(db.Model):
    __tablename__ = 'role'
    roleid = db.Column(db.CHAR(4), primary_key=True)
    rolename = db.Column(db.VARCHAR(50), nullable=False)
    cid = db.Column(db.CHAR(8), nullable=False)
    menutid = db.Column(db.CHAR(8), nullable=False)
    freeid = db.Column(db.CHAR(8), nullable=False)
    enddate = db.Column(db.DATE, nullable=False)
    comment = db.Column(db.VARCHAR(200))

    def __init__(self, roleid, rolename, cid, menutid, freeid, enddate, comment):
        self.roleid = roleid
        self.rolename = rolename
        self.cid = cid
        self.menutid = menutid
        self.freeid = freeid
        self.enddate = enddate
        self.comment = comment

    def getJson(self):
        return {"roleid": self.roleid, "name": self.rolename, "menutid": self.menutid, "freeid": self.freeid,
                "cid": self.cid, "comment": self.comment, "enddate": self.enddate.strftime('%Y-%m-%d')}


# 菜单模板表（menutem）
class menutem(db.Model):
    __tablename__ = 'menutem'
    menutid = db.Column(db.CHAR(8), primary_key=True)
    mid = db.Column(db.CHAR(4), nullable=False)
    cid = db.Column(db.CHAR(8), nullable=False, primary_key=True)
    menutname = db.Column(db.VARCHAR(200), nullable=False)
    isuse = db.Column(db.CHAR(1), nullable=False)
    mord = db.Column(db.Integer, nullable=False, primary_key=True)

    def __init__(self, menutid, mid, cid, menutname, isuse, mord):
        self.menutid = menutid
        self.mid = mid
        self.cid = cid
        self.menutname = menutname
        self.isuse = isuse
        self.mord = mord

    def getJson(self):
        return {"value": self.menutid, "label": self.menutname, "cid": self.cid, "mid": self.mid,
                "isuse": False if self.isuse == "N" else True, "mord": self.mord}


# 菜单表
class menu(db.Model):
    __tablename__ = 'menu'
    mid = db.Column(db.CHAR(4), primary_key=True)
    mname = db.Column(db.VARCHAR(200), nullable=False)
    comment = db.Column(db.VARCHAR(200), nullable=False)

    def __init__(self, mid, mname, comment):
        self.mid = mid
        self.mname = mname
        self.comment = comment

    def getJson(self):
        return {"value": self.mid, "label": self.mname, "comment": self.comment}


# 费用标准模板表
class free(db.Model):
    __tablename__ = 'free'
    freeid = db.Column(db.CHAR(8), primary_key=True)
    cid = db.Column(db.CHAR(8), nullable=False, primary_key=True)
    freename = db.Column(db.VARCHAR(50), nullable=False)
    fname = db.Column(db.VARCHAR(50), nullable=False)
    maxamt = db.Column(db.FLOAT, nullable=False)
    comment = db.Column(db.VARCHAR(500), nullable=True)
    ford = db.Column(db.Integer, nullable=False, primary_key=True)

    def __init__(self, freeid, cid, freename, fname, maxamt, comment, ford):
        self.freeid = freeid
        self.cid = cid
        self.freename = freename
        self.fname = fname
        self.maxamt = maxamt
        self.comment = comment
        self.ford = ford


# 付款银行卡号
class banks(db.Model):
    __tablename__ = 'banks'
    bord = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.CHAR(8), nullable=False)
    bid = db.Column(db.NVARCHAR(20), nullable=True)

    def __init__(self, bord, id, bid):
        self.bord = bord
        self.id = id
        self.bid = bid


class rticket(db.Model):
    __tablename__ = 'rticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stayid = db.Column(db.Integer)
    carid = db.Column(db.Integer)
    lunchid = db.Column(db.Integer)
    start = db.Column(db.DATE)
    end = db.Column(db.DATE)
    remark = db.Column(db.TEXT)
    userid = db.Column(db.CHAR(6), nullable=False)
    username = db.Column(db.VARCHAR(20), nullable=False)
    cid = db.Column(db.CHAR(8), nullable=False)
    statue = db.Column(db.Integer, nullable=False)
    sumamt = db.Column(db.FLOAT)
    submitdate = db.Column(db.DATE, nullable=False)
    checkid = db.Column(db.CHAR(6))
    checkname = db.Column(db.VARCHAR(20))
    transbank = db.Column(db.NVARCHAR(20))

    def __init__(self, id, stayid, carid, lunchid, start, end, remark, userid, username, cid, statue, sumamt,
                 submitdate,
                 checkid, checkname, transbank):
        self.id = id
        self.stayid = stayid
        self.caselfrid = carid
        self.lunchid = lunchid
        self.start = start
        self.end = end
        self.remark = remark
        self.userid = userid
        self.username = username
        self.cid = cid
        self.statue = statue
        self.sumamt = sumamt
        self.submitdate = submitdate
        self.checkid = checkid
        self.checkname = checkname
        self.transbank = transbank

    def getJson(self):
        return {'title': '单号:{} | 姓名:{} | 事由:{}... | 时间:{} 至 {} | 合计: {}  |状态: {}'.format(self.id,self.username ,self.remark if len(
                                                                              self.remark) < 15 else self.remark[0:15],self.start, self.end,
                                                                          self.sumamt, state.get(self.statue)), 'id': self.id,
                'startdate': self.start.strftime('%Y-%m-%d'), 'enddate': self.end.strftime('%Y-%m-%d'), 'remark': self.remark, "sumamt": self.sumamt,"state": self.statue,
                "staylist": [], "carlist": [], "lunchlist": []}


class stayinfo(db.Model):
    __tablename__ = 'stayinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rticketid = db.Column(db.Integer)
    stime = db.Column(db.DATE)
    address = db.Column(db.TEXT)
    amount = db.Column(db.FLOAT, nullable=False)
    paddress = db.Column(db.TEXT)

    def __init__(self, id, rticketid, stime, address, amount, paddress):
        self.id = id
        self.rticketid = rticketid
        self.stime = stime
        self.address = address
        self.amount = amount
        self.paddress = paddress

    def getJson(self):
        return {'id': self.id,
                'detaildate': self.stime.strftime('%Y-%m-%d'),
                'address': self.address,
                'amount': self.amount,
                'paddress': self.paddress}


class carinfo(db.Model):
    __tablename__ = 'carinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rticketid = db.Column(db.Integer)
    stime = db.Column(db.DATE)
    saddress = db.Column(db.TEXT)
    eaddress = db.Column(db.TEXT)
    amount = db.Column(db.FLOAT, nullable=False)
    paddress = db.Column(db.TEXT)

    def __init__(self, id, rticketid, stime, saddress, eaddress, amount, paddress):
        self.id = id
        self.rticketid = rticketid
        self.stime = stime
        self.saddress = saddress
        self.eaddress = eaddress
        self.amount = amount
        self.paddress = paddress

    def getJson(self):
        return {'id': self.id,
                'detaildate': self.stime.strftime('%Y-%m-%d'),
                'startaddress': self.saddress,
                'endaddress': self.eaddress,
                'amount': self.amount,
                'paddress': self.paddress}


class lunchinfo(db.Model):
    __tablename__ = 'lunchinfo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rticketid = db.Column(db.Integer)
    stime = db.Column(db.DATE)
    amount = db.Column(db.FLOAT, nullable=False)
    paddress = db.Column(db.TEXT)

    def __init__(self, id, rticketid, stime, amount, paddress):
        self.id = id
        self.rticketid = rticketid
        self.stime = stime
        self.amount = amount
        self.paddress = paddress

    def getJson(self):
        return {'id': self.id,
                'detaildate': self.stime.strftime('%Y-%m-%d'),
                'amount': self.amount,
                'paddress': self.paddress}


class transhis(db.Model):
    __tablename__ = 'transhis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rticketid = db.Column(db.Integer)
    amount = db.Column(db.FLOAT, nullable=False)
    transbank = db.Column(db.NVARCHAR(20))
    transdate = db.Column(db.DATE)
    userid = db.Column(db.CHAR(6), nullable=False)
    username = db.Column(db.VARCHAR(20), nullable=False)

    def __init__(self, id, rticketid, amount, transbank, transdate, userid, username):
        self.id = id
        self.rticketid = rticketid
        self.amount = amount
        self.transbank = transbank
        self.transdate = transdate
        self.userid = userid
        self.username = username
