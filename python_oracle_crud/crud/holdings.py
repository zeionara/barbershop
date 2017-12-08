from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class Holdings(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(float)
    quantity = Required(float)
