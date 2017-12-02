import configparser
import pymongo

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

client = pymongo.MongoClient('mongodb://%s:%s@%s' % (config["mongo"]["login"], 
                                                   config["mongo"]["password"],
                                                   config["mongo"]["path"]))

db = client.barbershopdb
testcollection = db.testcollection

print(testcollection.insert_one({"name":"inserted from pymongo"}).inserted_id);