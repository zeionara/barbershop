import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')
import cx_Oracle
import connection
import qualifications
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_list

field_names = ("id", "name", "description")
field_widths = (30,30,50)
field_shorts = ("-i","-n","-d")
field_descriptions = ("(int)", "(string)", "(string)")
field_modifiers = (get, get, get, get_list)
field_status = (0, 2, 1)

base_class = qualifications.Qualifications

extra_field_names = ["rendered_services"]
extra_field_widths = [50]
extra_field_shorts = ["-r"]
extra_field_descriptions = ["set of last n symbols of ids separated by comma"]
extra_field_modifiers = [get_list]
extra_field_status = [1]

def ins(id, qual):
    print("Inserting %s to %s..." % (str(qual), str(id)))

def set_rendered_services(id, services):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    print(services)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, [int(service) for service in services])
    cursor.callproc('array_test_tapi.ins', [ids, id])
    db.commit()

def get_rendered_services(id):
    db = connection.establish_default()[2]
    cursor = db.cursor()
    #print(services)
    ids = cursor.arrayvar(cx_Oracle.NUMBER, [1,2])
    res = cursor.callproc('array_test_tapi.get', [ids, id])
    print(res)
    #db.commit()

def create(command):
    new_qualification = cms.create(command, base_class, field_shorts, field_names, field_modifiers)
    set_rendered_services(new_qualification.id, extra_field_modifiers[0](" ".join(cms.get_parameter_cmd(command, extra_field_shorts[0]) ) ) )



def read(command):
    stre = cms.get_stre(list(field_widths) + list(extra_field_widths))
    fn = tuple(list(field_names) + list(extra_field_names))
    for item in cms.get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        prop_list = list(cms.get_properties_tuple(item, field_widths, field_names))
        prop_list.append(get_rendered_services(item.id) )
        print(stre % tuple(prop_list))

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
