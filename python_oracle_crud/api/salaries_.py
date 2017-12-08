import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')

import salaries
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("id", "worker_id", "common", "vacation", "sick")
field_widths = (30,30,20,20,20)
field_shorts = ("-i","-w","-c","-v","-s")
field_descriptions = ("(int)", "(string)", "(float)", "(float)", "(float)")
field_modifiers = (get, get, get_float, get_float, get_float)
field_status = (0, 2, 2, 2, 2)
base_class = salaries.Salaries

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
