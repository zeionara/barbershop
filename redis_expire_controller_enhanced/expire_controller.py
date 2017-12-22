import re
import datetime
import configparser
import redis
import pickle
import time
import sys

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')
redis_key_delimiter = "_"
prefix = "sql"
time_prefix = "timemong"
max_lifetime = 3600
max_memory = 1000
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
            print(key, " - ", key_time)
            print((current_time - key_time).total_seconds())
            if ((current_time - key_time).total_seconds() >= max_lifetime):
                print("Expired")
                #redis_connection.delete(key)
        time.sleep(checking_interval)


class cached_object_:
     def __init__(self, key, seconds_after_access, size):
         self.key = key
         self.seconds_after_access = seconds_after_access
         self.size = size

def print_cached_objects(cached_objects):
    for cached_object in cached_objects:
        print(cached_object.key," ",cached_object.seconds_after_access," ",cached_object.size)

def inspect_enhanced(arg):
    while(executing):
        current_time = datetime.datetime.now()
        pip = redis_connection.pipeline()
        pip_entries = redis_connection.pipeline()
        keys = []

        for key in redis_connection.scan_iter(time_prefix + "*"):
            pip.get(key)
            pip_entries.get(get_key(str(key)[2:-1]))
            keys.append(key)

        key_times = pip.execute()
        entries = pip_entries.execute()
        cached_objects = []

        for i in range(len(keys)):
            key_time = pickle.loads(key_times[i])
            key = get_key(str(keys[i])[2:-1])
            cached_objects.append(cached_object_(key, (current_time - key_time).total_seconds(), sys.getsizeof(entries[i])))

        cached_objects.sort(key = lambda cached_object: cached_object.seconds_after_access)
        #print_cached_objects(cached_objects)

        quantity_to_save = 0
        whole_size = 0

        for cached_object in cached_objects:
            whole_size += cached_object.size
            if (whole_size > max_memory):
                break
            quantity_to_save += 1

        for cached_object in cached_objects[quantity_to_save:]:
            redis_connection.delete(cached_object.key)
            #print("delete ",cached_object.key)
            redis_connection.delete(time_prefix + redis_key_delimiter + cached_object.key)
            #print("delete ",time_prefix + redis_key_delimiter + cached_object.key)
        time.sleep(checking_interval)

inspect_enhanced((10,))
