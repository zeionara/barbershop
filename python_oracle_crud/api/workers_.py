import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')
from pony.orm import *
import workers
import contacts_
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_bytes

field_names = ("id", "name", "surname", "sex", "address", "login", "passwd", "patronymic", "avatar", "position", "qualification")
field_widths = (30,15,30,10,50,20,20,50,50,20,20)
field_shorts = ("-i","-n","-s","-se","-a","-l","-p","-pat", "-av", "-pos", "-q")
field_descriptions = ("(int)", "(string)", "(string)", "m or w", "(string)" , "(string)", "(string)",
                    "(string)", "path to file", "(int)", "(int)")
field_modifiers = (get, get, get, get, get, get, get, get, get_bytes, get, get)
field_status = (0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2)
base_class = workers.Workers

def create(command):
    worker = cms.create(command, base_class, field_shorts, field_names, field_modifiers)
    phone = " ".join(cms.get_parameter_cmd(command, "-ph"))
    #print(phone)
    cmd = ("cc -ps worker -pi "+str(worker.id)+" -t phone -c "+phone).split(' ');
    #print(cmd)
    try:
        contacts_.create(cmd)
    except:
        print("Error adding worker! Message: %s. Please, check your input." % sys.exc_info()[1])
        with db_session:
            worker.delete()

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
