import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import holdings
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("_id", "name", "quantity", "price")
field_widths = (30,50,10,10)
field_shorts = ("-i","-n","-q","-p")
field_descriptions = ("last n symbols", "(string)", "(float)", "(float)")
field_modifiers = (get, get, get_float, get_float)
field_status = (0, 2, 2, 2)
base_class = holdings.Holding
session = holdings.session

#cms.mark_redis_invalid(base_class)

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
