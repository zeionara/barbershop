import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')
import datetime

import requests
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_list
from commons_ import get_date_time
from commons_ import get_holdings_list


field_names = ("_id", "worker_ids", "client_ids", "service_ids", "holdings", "visit_date_time", "note", "factical_durability")
field_widths = (30,50,50,50,50,30,50,20)
field_shorts = ("-i","-w","-c","-s","-h","-d","-n","-f")
field_descriptions = ("last n symbols", "list of items separated by comma",
    "list","list","list of holdings with quantity in format 414f, 100; 3232, 200; ed, 500", "in format 10.10.2017 09:05", "(string)","(float)")
field_modifiers = (get, get_list, get_list, get_list, get_holdings_list, get_date_time, get, get_float)
field_status = (0, 2, 2, 2, 2, 2, 1, 1)
base_class = requests.Request
session = requests.session

def create(command):
    cms.create(command, base_class, field_shorts, field_names, field_modifiers, session)

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers, session)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers, session)
