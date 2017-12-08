from pony.orm import *
import cx_Oracle
import datetime
import configparser
import connection

db = connection.establish_default()[1]

class Premiums(db.Entity):
    id = PrimaryKey(int, auto=True)
    premium_id = Required(int)
    worker_id = Required(int)
    earning_date = Required(datetime.datetime)
    premium_size = Required(float)
    note = Optional(str)
