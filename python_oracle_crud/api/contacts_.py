import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')

import contacts
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float

field_names = ("id", "person_status", "person_id", "type", "contact")
field_widths = (30,10,30,10,30)
field_shorts = ("-i","-ps","-pi","-t", "-c")
field_descriptions = ("(int)", "(client or worker)", "(int)", "(e-mail, phone or vk)", "(string)")
field_modifiers = (get, get, get, get, get)
field_status = (0, 2, 2, 2, 2)
base_class = contacts.Contacts

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
