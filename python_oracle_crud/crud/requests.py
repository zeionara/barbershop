from pony.orm import *
import cx_Oracle
import datetime
import configparser
import connection

db = connection.establish_default()[1]

class Requests(db.Entity):
    id = PrimaryKey(int, auto=True)
    visit_date_time = Required(datetime.datetime)
    worker_id = Required(int)
    client_id = Required(int)
    service_id = Required(int)
    note = Optional(str)
    factical_durability = Optional(float)
