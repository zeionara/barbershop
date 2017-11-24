import configparser
import cx_Oracle


def establish(ip, port, sid):
    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")
    return (db.cursor(), db)
