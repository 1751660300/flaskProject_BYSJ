# -*- coding:utf-8 -*-
class config(object):
	SECRET_KEY = '123456'
	DEBUG = True
	# 数据库配置
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/bysj?charset=utf8"
	SQLALCHEMY_POOL_SIZE = 10  # 数据库连接池的大小。默认值 5
	SQLALCHEMY_POOL_TIMEOUT = 30  # 指定数据库连接池的超时时间。默认是 10
	SQLALCHEMY_POOL_RECYCLE = -1
	SQLALCHEMY_MAX_OVERFLOW = 3  # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接回收到连接池后将会被断开和抛弃
	SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪对象的修改并且发送信号