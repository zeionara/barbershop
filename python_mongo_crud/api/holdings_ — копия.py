import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import holdings
from commons import get_by_id

def get(value):
    return value

def get_float(value):
    return float(value)

field_names = ("_id", "name", "quantity", "price")
field_widths = (30,50,10,10)
field_shorts = ("-i","-n","-q","-p")
field_shorts_n = ("--i","--n","--q","--p")
field_modifiers = (get, get, get_float, get_float)


def find_next_flag(begin_index, command):
    for i in range(begin_index, len(command)):
        if (command[i][0] == "-") and (re.match("[a-z/-]",command[i][1])):
            print("---%s" % command[i])
            return i
    return len(command)

def get_parameter_cmd(command, code):
    try:
        index = command.index(code) + 1
        value = command[index]
        if (value[0] != "-") or (re.match("[0-9]",value[1])):
            return command[index : find_next_flag(index + 1, command)]
        return None
    except ValueError:
        return None

def get_params(result):
    returned = []
    for short in field_shorts:
        returned.append(get_joined_value(result, short, " "))
    return returned

def get_params_with_shorts(result, shorts):
    returned = []
    for short in shorts:
        returned.append(get_joined_value(result, short, " "))
    return returned

command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ')
parameters_list = ["-a","-b","-c"]

def parse(command, parameters_list):
    result = []
    for parameter in parameters_list:
        values = get_parameter_cmd(command, parameter)
        if values != None:
            result.append([parameter, values])
    return result

def get_stre(widths):
    stre = ""
    for width in widths:
        stre += "%-"+str(width)+"s "
    return stre

def get_joined_value(parameters, code, delimiter):
    for parameter in parameters:
        if code == parameter[0]:
            return delimiter.join(parameter[1])

def get_full_set():
    return holdings.Holding.query.find().all()

def show_entities(command):
    full_set = get_full_set()
    result = parse(command, field_shorts)

    params = get_params(result)

    for i in range(len(params)):
        if (params[i] != None):
            intermediate_set = []
            for item in full_set:
                if ((str(getattr(item, field_names[i])) == params[i]) and (i > 0)) or \
                    ((str(getattr(item, field_names[i]))[-len(params[i]):] == params[i]) and (i == 0)):
                    intermediate_set.append(item)
            full_set = intermediate_set

    #print(full_set)

    stre = get_stre(field_widths)

    print(stre % field_names)
    for item in full_set:
        print(stre % tuple([str(getattr(item, field_name)) for field_name in field_names]))

def get_entities(command):
    full_set = get_full_set()
    result = parse(command, field_shorts)

    params = get_params(result)

    for i in range(len(params)):
        if (params[i] != None):
            intermediate_set = []
            for item in full_set:
                if ((str(getattr(item, field_names[i])) == params[i]) and (i > 0)) or \
                    ((str(getattr(item, field_names[i]))[-len(params[i]):] == params[i]) and (i == 0)):
                    intermediate_set.append(item)
            full_set = intermediate_set

    return full_set
##########

if command[0] == "ch":
    result = parse(command, field_shorts)
    holdings.Holding(name = field_modifiers[1](get_joined_value(result, field_shorts[1], " ")),
                     quantity = field_modifiers[2](get_joined_value(result, field_shorts[2], " ")),
                     price = field_modifiers[3](get_joined_value(result, field_shorts[3], " ")))
    holdings.session.flush_all()

if command[0] == "rh":
    show_entities(command)


if command[0] == "uh":
    entities = get_entities(command)
    result = parse(command, ["-"+field_short for field_short in field_shorts[1:]])

    params = get_params_with_shorts(result,["-"+field_short for field_short in field_shorts[1:]])
    print(params)

    for i in range(len(params)):
        if (params[i] != None):
            for item in entities:
                setattr(item, field_names[i + 1], field_modifiers[ i + 1 ](params[i]))

    holdings.session.flush_all()

if command[0] == "dh":

    for item in get_entities(command):
        item.delete()

    holdings.session.flush_all()
