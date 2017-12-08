from pony.orm import *
import cx_Oracle
import datetime
import configparser
import connection

db = connection.establish_default()[1]

class Qualifications(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Required(str)
