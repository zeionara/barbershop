from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class Salaries(db.Entity):
    id = PrimaryKey(int, auto=True)
    worker_id = Required(int)
    common = Required(float)
    vacation = Required(float)
    sick = Required(float)
