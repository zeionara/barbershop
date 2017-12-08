import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')

import services
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("id", "name", "description", "price", "avg_duration")
field_widths = (30,50,50,20,20)
field_shorts = ("-i","-n","-d","-p","-a")
field_descriptions = ("(int)", "(string)", "(string)", "(float)", "(float)")
field_modifiers = (get, get, get, get_float, get_float)
field_status = (0, 2, 1, 2, 1)
base_class = services.Services

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
