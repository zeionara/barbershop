# -*- coding: utf-8 -*-
import datetime

import redis
r = redis.StrictRedis(host='host', port=1488, db=0)
#print("setting foo...")
#r.set("foo","bar")
#r.set("foo",["a","b"])
foo = [(4, datetime.datetime(2002, 11, 10, 14, 10), 2, 1, 2, None, None, None),
       (5, datetime.datetime(2002, 11, 10, 16, 10), 2, 2, 2, None, None, None),
       (22, datetime.datetime(2002, 2, 2, 0, 0), 2, 1, 2, None, None, None),
       (23, datetime.datetime(2002, 2, 3, 0, 0), 2, 1, 2, None, None, None)]

#r.set("foo",foo)


print("getting foo...")
fi = str(r.get("foo"),"utf-8")
print(rebuild_list(fi))
#print(type(fi))
#result = []

