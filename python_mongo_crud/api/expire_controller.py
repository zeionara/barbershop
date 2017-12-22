import re
import datetime
import configparser
import redis
import pickle
import time

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')
redis_key_delimiter = "_"
prefix = "sql"
time_prefix = "timemong"
max_lifetime = 30
checking_interval = 5
executing = True

redis_connection = redis.StrictRedis(host=config['redis']['host'], port=int(config['redis']['port']), db=0)

def get_key(key):
    return redis_key_delimiter.join(key.split(redis_key_delimiter)[1:])

def inspect(arg):
    while(executing):
        current_time = datetime.datetime.now()
        pip = redis_connection.pipeline()
        keys = []
        for key in redis_connection.scan_iter(time_prefix + "*"):
            pip.get(key)
            keys.append(key)
        key_times = pip.execute()
        for i in range(len(keys)):
            key_time = pickle.loads(key_times[i])
            key = get_key(str(keys[i])[2:-1])
            #print(key, " - ", key_time)
            #print((current_time - key_time).total_seconds())
            if ((current_time - key_time).total_seconds() >= max_lifetime):
                #print("Expired")
                redis_connection.delete(key)
        time.sleep(checking_interval)
