# -*- coding:utf-8 -*-
from redis import Redis, ConnectionPool

# 连接redis
r = Redis(password='123456')
# redis连接池
# pool = ConnectionPool(host="172.0.0.1", port="6379")
# r = Redis(connection_pool=pool)

# r.set("id", "123456", nx=10)

print(r.get("100001"))


