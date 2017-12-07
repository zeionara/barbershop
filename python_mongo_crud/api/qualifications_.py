import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import qualifications
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_list

field_names = ("_id", "name", "description", "rendered_services")
field_widths = (30,30,50,70)
field_shorts = ("-i","-n","-d","-r")
field_descriptions = ("last n symbols", "(string)", "(string)", "set of last n symbols of ids separated by comma")
field_modifiers = (get, get, get, get_list)
field_status = (0, 2, 1, 2)
base_class = qualifications.Qualification
session = qualifications.session


def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
