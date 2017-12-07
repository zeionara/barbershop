import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import contacts
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("_id", "person_type", "person_id", "type", "contact")
field_widths = (30,10,30,10,30)
field_shorts = ("-i","-pt","-pi","-t", "-c")
field_descriptions = ("last n symbols", "(client or worker)", "(last n symbols)", "(e-mail, phone or vk)", "(string)")
field_modifiers = (get, get, get, get, get)
field_status = (0, 2, 2, 2, 2)
base_class = contacts.Contact
session = contacts.session

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
