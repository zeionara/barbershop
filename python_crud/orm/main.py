from pony.orm import *
import configparser
import cx_Oracle
import pickle

db = Database()

class Positions(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)

class Qualifications(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    rendered_services = Optional(str, sql_type = "services_table__")


def establish_connection(ip, port, sid):

    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    dbs = db.bind(provider="oracle", user=config['helios']['login'], password=config['helios']['password'],
                  dsn=dsn_tns, encoding = "UTF-8")
    x = "1"
    db.generate_mapping(create_tables=True)

    return (dbs, db)


if __name__ == '__main__':
    result = establish_connection('127.0.0.1',1521,'orbis')
    cursor = result[0]
    conn = result[1]
    with db_session:
        print(Qualifications.select().filter(raw_sql("name = 'цирюльник'"))[:])
