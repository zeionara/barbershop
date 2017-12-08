import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_oracle_crud/crud/')
from pony.orm import *
import clients
import contacts_
from commons import get_by_id
import commons_ as cms
from commons_ import get
from commons_ import get_float
from commons_ import get_bytes

field_names = ("id", "name", "surname", "sex", "address", "login", "passwd", "patronymic", "avatar")
field_widths = (30,15,30,10,50,20,20,50,50)
field_shorts = ("-i","-n","-s","-se","-a","-l","-p","-pat", "-av")
field_descriptions = ("(int)", "(string)", "(string)", "m or w", "(string)" , "(string)", "(string)", "(string)", "path to file")
field_modifiers = (get, get, get, get, get, get, get, get, get_bytes)
field_status = (0, 2, 2, 2, 2, 2, 2, 1, 1)
base_class = clients.Clients

def create(command):
    client = cms.create(command, base_class, field_shorts, field_names, field_modifiers)
    phone = " ".join(cms.get_parameter_cmd(command, "-ph"))
    cmd = ("cc -ps client -pi "+str(client.id)+" -t phone -c "+phone).split(' ');
    try:
        print(cmd)
        contacts_.create(cmd)
    except:
        print("Error adding client! Message: %s. Please, check your input." % sys.exc_info()[1])
        with db_session:
            client.delete()

def read(command):
    cms.show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers)

def update(command):
    cms.update(command, base_class, field_shorts, field_names, field_modifiers)

def delete(command):
    cms.delete(command, base_class, field_shorts, field_names, field_modifiers)
