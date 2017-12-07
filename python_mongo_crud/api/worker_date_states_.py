import sys
import re

sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import worker_date_states
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_worker_date_state_list

field_names = ("_id", "worker_id", "date_states")
field_widths = (30,30,100)
field_shorts = ("-i","-w","-d")
field_descriptions = ("last n symbols", "(string)", "dates and ids of related states in format : 12.12.2017,e88 ; 12.11.2017, e89 ")
field_modifiers = (get, get, get_worker_date_state_list)
field_status = (0, 2, 2)
base_class = worker_date_states.WorkerDateStates
session = worker_date_states.session


def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
