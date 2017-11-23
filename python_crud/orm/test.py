from pony.orm import *
import configparser
import cx_Oracle

db = Database()

class Positions(db.Entity):
    id = PrimaryKey(int)
    name = Required(str)
    description = Optional(str)


def establish_connection(ip, port, sid):

    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    dbs = db.bind(provider="oracle", user=config['helios']['login'], password=config['helios']['password'],
                  dsn=dsn_tns, encoding = "UTF-8")
    x = "1"
    db.generate_mapping(create_tables=True)
    
    with db_session:
        print(db.select("select * from workers"))
        #position1 = Positions(id=12, name="pony",description="My little pony")

        print(Positions[1].name)
    
establish_connection('127.0.0.1',1521,'orbis')



