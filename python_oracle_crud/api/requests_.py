import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')
import datetime
import connection
import cx_Oracle
import requests
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_list
from commons_ import get_date_time
from commons_ import get_holdings_list

field_names = ("id", "worker_id", "client_id", "service_id", "visit_date_time", "note", "factical_durability")
field_widths = (10,10,10,10,30,20,20)
field_shorts = ("-i","-w","-c","-s","-d","-n","-f")
field_descriptions = ("last n symbols", "list of items separated by comma",
    "list","list", "in format 10.10.2017 09:05", "(string)","(float)")
field_modifiers = (get, get, get, get, get_date_time, get, get_float)
field_status = (0, 2, 2, 2, 2, 1, 1)

base_class = requests.Requests

extra_field_names = [ "holdings"]
extra_field_widths = [50]
extra_field_shorts = ["-h"]
extra_field_descriptions = ["list of holdings with quantity in format 1, 100; 4, 200; 8, 500"]
extra_field_modifiers = [get_holdings_list]
extra_field_status = [2]

def set_holdings(id, holdings):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, [int(holding[0]) for holding in holdings])
    quantity = cursor.arrayvar(cx_Oracle.NUMBER, [int(holding[1]) for holding in holdings])
    cursor.callproc('requests_holdings_tapi.ins', [ids, quantity, id])
    db.commit()

def get_holdings(id):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, [-1 for i in range(10)])
    quantities = cursor.arrayvar(cx_Oracle.NUMBER, [-1 for i in range(10)])
    res = cursor.callproc('requests_holdings_tapi.get', [ids, quantities, id])
    #print(res)
    #print(res[0])
    ret = []
    for i in range(len(res[0])):
        ret.append([res[0][i], res[1][i]])
    return ret

    #db.commit()

def create(command):
    new_request = cms.create(command, base_class, field_shorts, field_names, field_modifiers)
    set_holdings(new_request.id, extra_field_modifiers[0](" ".join(cms.get_parameter_cmd(command, extra_field_shorts[0]) ) ) )

def read(command):
    #cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)
    stre = cms.get_stre(list(field_widths) + list(extra_field_widths))
    fn = tuple(list(field_names) + list(extra_field_names))
    print(stre % fn)
    for item in cms.get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        prop_list = list(cms.get_properties_tuple(item, field_widths, field_names))
        prop_list.append(get_holdings(item.id))
        print(stre % tuple(prop_list))

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
