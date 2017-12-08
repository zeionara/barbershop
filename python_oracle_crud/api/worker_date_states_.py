import sys
import re
import datetime
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')
import connection
import cx_Oracle
import worker_date_states
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_worker_date_state_list

field_names = ("id", "worker_id")
field_widths = (30,30)
field_shorts = ("-i","-w")
field_descriptions = ("(int)", "(string)")
field_modifiers = (get, get)
field_status = (0, 2)

base_class = worker_date_states.WorkerDateStates

extra_field_names = ["date_states"]
extra_field_widths = [100]
extra_field_shorts = ["-d"]
extra_field_descriptions = ["dates and ids of related states in format : 12.12.2017,e88 ; 12.11.2017, e89 "]
extra_field_modifiers = [get_worker_date_state_list]
extra_field_status = [1]

upd_field_names = ["append_date_states", "delete_date_states"]
upd_field_widths = [100, 100]
upd_field_short = ["--ad", "--dd"]
upd_field_descriptions = ["dates and ids of related states to append in format : 12.12.2017,e88 ; 12.11.2017, e89 ",
                          "dates and ids of related states to delete in format : 12.12.2017,e88 ; 12.11.2017, e89 "]
upd_field_modifiers = [get_worker_date_state_list]
upd_field_status = [1]

def set_date_states(id, date_states):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    dates = cursor.arrayvar(cx_Oracle.DATETIME, [date_state[0] for date_state in date_states])
    states = cursor.arrayvar(cx_Oracle.NUMBER, [int(date_state[1]) for date_state in date_states])
    #print(date_states)
    cursor.callproc('worker_date_states_tapi.ins', [states, dates, id])
    db.commit()

def append_date_states(id, date_states):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    dates = cursor.arrayvar(cx_Oracle.DATETIME, [date_state[0] for date_state in date_states])
    states = cursor.arrayvar(cx_Oracle.NUMBER, [int(date_state[1]) for date_state in date_states])
    #print(date_states)
    cursor.callproc('worker_date_states_tapi.app', [states, dates, id])
    db.commit()

def delete_date_states(id, date_states):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    dates = cursor.arrayvar(cx_Oracle.DATETIME, [date_state[0] for date_state in date_states])
    states = cursor.arrayvar(cx_Oracle.NUMBER, [int(date_state[1]) for date_state in date_states])
    #print(date_states)
    cursor.callproc('worker_date_states_tapi.del', [states, dates, id])
    db.commit()

def get_date_states(id):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, [-1 for i in range(10)])
    dates = cursor.arrayvar(cx_Oracle.DATETIME, [datetime.datetime(2006,6,6) for i in range(10)])
    res = cursor.callproc('worker_date_states_tapi.get', [ids, dates, id])
    #print(res)
    #print(res[0])
    ret = []
    #print(res)
    for i in range(len(res[0])):
        ret.append([res[0][i], res[1][i].strftime('%d.%m.%Y')])
    return ret

def create(command):
    new_ds = cms.create(command, base_class, field_shorts, field_names, field_modifiers)
    if cms.get_parameter_cmd(command, extra_field_shorts[0]) != None:
        set_date_states(new_ds.id, extra_field_modifiers[0](" ".join(cms.get_parameter_cmd(command, extra_field_shorts[0]) ) ) )

def read(command):
    #cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)
    stre = cms.get_stre(list(field_widths) + list(extra_field_widths))
    fn = tuple(list(field_names) + list(extra_field_names))
    print(stre % fn)
    for item in cms.get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        prop_list = list(cms.get_properties_tuple(item, field_widths, field_names))
        prop_list.append(get_date_states(item.id))
        print(stre % tuple(prop_list))

def update(command):
    ids = cms.update(command, base_class, field_shorts, field_names, field_modifiers)
    deletings = cms.get_parameter_cmd(command, upd_field_shorts[1])
    appendings = cms.get_parameter_cmd(command, upd_field_shorts[0])
    if deletings != None:
        delete_date_states(new_ds.id, extra_field_modifiers[1](" ".join(deletings ) ) )
    if appendings != None:
        append_date_states(new_ds.id, extra_field_modifiers[0](" ".join(appendings ) ) )

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
