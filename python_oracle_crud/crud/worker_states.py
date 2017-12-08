from pony.orm import *
import cx_Oracle

import configparser
import connection

db = connection.establish_default()[1]

class WorkerStates(db.Entity):
    _table_ = "WORKERS_STATES"

    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
