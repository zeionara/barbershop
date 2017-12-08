from pony.orm import *
import cx_Oracle
import configparser

db = None
dbs = None

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')

def establish(login, password, ip, port, sid):
    global db
    global dbs
    if db == None:
        db = Database()
        dsn_tns = cx_Oracle.makedsn(ip, port, sid)
        dbs = db.bind(provider="oracle", user=login, password=password,
                      dsn=dsn_tns, encoding = "UTF-8")
        x = "1"
    return (dbs, db)

def establish_default():
    global config
    global db
    global dbs
    if db == None:
        return establish(config['helios']['login'], config['helios']['password'], config['helios']['ip'],
                                int(config['helios']['port']), config['helios']['sid'])
    return (dbs, db)
