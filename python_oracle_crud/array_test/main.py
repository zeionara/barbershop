import configparser
import cx_Oracle
import redis
config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

dsn_tns = cx_Oracle.makedsn('127.0.0.1', 1521, 'orbis')

db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")

cursor = db.cursor()
ids = cursor.arrayvar(cx_Oracle.NUMBER, [22,23])
cursor.callproc('array_test_tapi.ins', [ids, 61])

db.commit()
