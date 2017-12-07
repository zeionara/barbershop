# -*- coding: utf-8 -*-
import datetime
import configparser
import redis
import json
import jsonpickle
import pickle
import sys
import marshal
from bson.objectid import ObjectId
sys.path.insert(0, 'C://Users//Zerbs//Desktop//databases_kursach//python_mongo_crud//crud')
import qualifications

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

class ExampleObject():
    def __init__(self, prop):
        self.prop = prop


r = redis.StrictRedis(host=config['redis']['host'], port=int(config['redis']['port']), db=0)
for key in r.scan_iter('contacts*_'):
    print(r.get(key))
#ids = ["5a25779089ad93358c97d6eb","5a2576e189ad93250cc64a9b"]
#pickled = pickle.dumps(ids)
#r.set('foo', pickled)
#unpacked = pickle.loads(r.get('foo'))
#print(unpacked)
#print(qualifications.Qualification.query.find({"_id" : ObjectId(unpacked[0])}).all())
#print(pickled == unpacked)
