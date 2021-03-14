# -*- coding:utf-8 -*-
# 获取当前时间
import time  # 引入time模块


def getNowTime():
    ticks = time.time()
    nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ticks))
    return nowTime
