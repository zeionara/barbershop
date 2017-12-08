from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class Workers(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    surname = Required(str)
    patronymic = Optional(str)
    sex = Required(str)
    address = Required(str)
    login = Required(str)
    passwd = Required(str)
    avatar = Optional(bytes)
    position = Required(int)
    qualification = Required(int)
