from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class Services(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(float)
    description = Optional(str)
    avg_duration = Required(float)
