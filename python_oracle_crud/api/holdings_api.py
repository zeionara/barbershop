import sys
import re
sys.path.insert(0, 'C:/Users/Zerbs/Desktop/databases_kursach/python_mongo_crud/crud/')

import holdings
from commons import get_by_id

field_names = ("id", "name", "quantity", "price")
field_widths = (30,50,10,10)
field_shorts = ("-n","-q","-p")

def find_next_flag(begin_index, command):
    for i in range(begin_index, len(command)):
        if (command[i][0] == "-") and (re.match("[a-z]",command[i][1])):
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

if command[0] == "ch":
    result = parse(command, field_shorts)
    holdings.Holding(name = get_joined_value(result, "-n", " "), 
                     quantity = float(get_joined_value(result, "-q", " ")),
                     price = float(get_joined_value(result, "-p", " ")))
    holdings.session.flush_all()
    
if command[0] == "rh":
    full_set = holdings.Holding.query.find().all()
    result = parse(command, field_shorts)
    
    params = get_params(result)
    
    name = params[0] 
    quantity = params[1]
    price = params[2]
    
    print(quantity)
    
    if (name != None):
        intermediate_set = []
        for item in full_set:
            if item.name == name:
                intermediate_set.append(item)
        full_set = intermediate_set
        
    if (quantity != None):
        intermediate_set = []
        for item in full_set:
            if item.quantity == float(quantity):
                intermediate_set.append(item)
        full_set = intermediate_set
    
    if (price != None):
        intermediate_set = []
        for item in full_set:
            if item.price == float(price):
                intermediate_set.append(item)
        full_set = intermediate_set
        
    print(full_set)
    
    stre = get_stre(field_widths)
    print(stre % field_names)
    for item in full_set:
        print(stre % (str(item._id), item.name, str(item.quantity), str(item.price)))
    
    
if command[0] == "uh":
    result = parse(command, field_shorts)
    holding = get_by_id(holdings.Holding, command[1])
    
    name = get_joined_value(result, "-n", " ") 
    quantity = get_joined_value(result, "-q", " ")
    price = get_joined_value(result, "-p", " ")
    
    
    if (name != None):
        holding.name = name
    if (quantity != None):
        holding.quantity = float(quantity)
    if (price != None):
        holding.price = float(price)

    holdings.session.flush_all()
    
if command[0] == "dh":
    get_by_id(holdings.Holding, command[1]).delete()
    holdings.session.flush_all()

    