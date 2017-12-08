from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class Contacts(db.Entity):
    id = PrimaryKey(int, auto=True)
    person_status = Required(str)
    person_id = Required(int)
    type = Required(str)
    contact = Required(str)





#position = Position(name = "General hairdresser")

#session.flush_all()
