from pony.orm import *
import cx_Oracle

import configparser
import connection

#config = configparser.ConfigParser()
#config.read('C://Users//Zerbs//accounts.sec')

db = connection.establish_default()[1]

#db = result[1]

class Positions(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)


#db.generate_mapping(create_tables=True)

#position = Position(name = "General hairdresser")

#session.flush_all()
