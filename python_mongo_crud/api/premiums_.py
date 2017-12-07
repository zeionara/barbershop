import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import premiums
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_date

field_names = ("_id", "premium_id", "worker_id", "earning_date", "size", "note")
field_widths = (30,30,30,30,20,50)
field_shorts = ("-i","-p","-w", "-d", "-s", "-n")
field_descriptions = ("last n symbols", "(string)", "(string)", "in format 17.12.2017", "(float)", "(string)")
field_modifiers = (get, get, get, get_date, get_float, get)
field_status = (0, 2, 2, 2, 2, 1)
base_class = premiums.Premium
session = premiums.session

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
