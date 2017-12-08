from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class PremiumSizes(db.Entity):
    _table_ = "PREMIUMS_SIZES"

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    min = Required(float)
    max = Required(float)
    description = Optional(str)
