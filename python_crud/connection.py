import configparser
import cx_Oracle
import redis
config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

redis_connector = redis.StrictRedis(host=config['redis']['host'], port=int(config['redis']['port']), db=0)

def establish(ip, port, sid):
    global config

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")
    return (db.cursor(), db)


