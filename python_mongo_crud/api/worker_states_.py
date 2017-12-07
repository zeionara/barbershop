import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import worker_states
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("_id", "name", "description")
field_widths = (30,50,100)
field_shorts = ("-i","-n","-d")
field_descriptions = ("last n symbols", "(string)", "(string)")
field_modifiers = (get, get, get)
field_status = (0, 2, 1)
base_class = worker_states.WorkerState
session = worker_states.session

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
