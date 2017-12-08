import re
import datetime
import configparser
import redis
import pickle
from pony.orm import *
from bson.objectid import ObjectId

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')
prefix = "sql_"

redis_connection = redis.StrictRedis(host=config['redis']['host'], port=int(config['redis']['port']), db=0)

def get_date(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y')

def get_date_time(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y %H:%M')

def get_bytes(path):
    if path == None:
        return None
    in_file = open(path, "rb")
    data = in_file.read()
    in_file.close()
    return data

def get(value):
    return value

def get_str(value):
    return "'"+str(value)+"'"

def get_list(value):
    return value.replace(" ","").split(",")

def get_float(value):
    if value == None:
        return None
    return float(value)

def get_worker_date_state_list(value):
    #value = '12.12.2017,e88 ; 12.11.2017, e89 '
    #print(">>>>" + value)
    result = []
    pre_result = value.replace(" ","").split(";")
    for item in pre_result:
        pair = item.split(",")
        result.append([get_date(pair[0]), pair[1]])
    return result

def get_holdings_list(value):
    #value = 'e88, 100 ;e89, 200 '
    #print(">>>>" + value)
    result = []
    pre_result = value.replace(" ","").split(";")
    for item in pre_result:
        pair = item.split(",")
        result.append([pair[0], get_float(pair[1])])
    return result


##
def find_next_flag(begin_index, command):
    #print(command)
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

def get_params(result, shorts):
    returned = []
    for short in shorts:
        returned.append(get_joined_value(result, short, " "))
    return returned

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

def get_full_set(base_class):
    return base_class.query.find().all()

def get_properties_tuple(item, field_widths, field_names):
    result = []
    for i in range(len(field_widths)):
        if len(str(getattr(item, field_names[i]))) > field_widths[i]:
            result.append(str(getattr(item, field_names[i]))[:field_widths[i]-5] + "...")
        else:
            result.append(str(getattr(item, field_names[i])))
    return tuple(result)

def get_filter(params, field_names):
    filter = ""
    for i in range(len(params)):
        if (params[i] == None):
            continue
        if filter != "":
            filter += " AND "
        filter += field_names[i] + " = " + get_str(params[i])
    return filter

def get_entities(command, base_class, field_shorts, field_names, field_modifiers):
    global prefix
    global redis_connection
    collection_name = prefix+str(base_class).split("'")[1].split(".")[0]

    result = parse(command, field_shorts)
    params = get_params(result, field_shorts)
    redis_key = collection_name+"_"+"_".join([str(param) for param in params])

    got_from_redis = str(redis_connection.get(redis_key+"_valid")) == "b'1'"

    if (got_from_redis):
        print("got from redis")
        with db_session:
            result = pickle.loads(redis_connection.get(redis_key))
    else:
        filter = get_filter(params, field_names)
        with db_session:
            if filter == "":
                result = base_class.select()[:]
            else:
                result = base_class.select().filter(raw_sql(filter))[:]
        redis_connection.set(redis_key, pickle.dumps(result))
        redis_connection.set(redis_key+"_valid", "1")
    return result

def show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers):
    stre = get_stre(field_widths)
    print(stre % field_names)
    for item in get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        print(stre % get_properties_tuple(item, field_widths, field_names))

def mark_redis_invalid(base_class):
    global redis_connection
    global prefix
    collection_name = prefix + str(base_class).split("'")[1].split(".")[0]
    for key in redis_connection.scan_iter(collection_name+'_*valid'):
        redis_connection.delete(key)
##

def delete(command, base_class, field_shorts, field_names, field_modifiers):
    with db_session:
        for item in get_entities(command, base_class, field_shorts, field_names, field_modifiers):
            item.delete()
    mark_redis_invalid(base_class)

@db_session
def update(command, base_class, field_shorts, field_names, field_modifiers):
    entities = get_entities(command, base_class, field_shorts, field_names, field_modifiers)
    result = parse(command, ["-"+field_short for field_short in field_shorts[1:]])
    params = get_params(result,["-"+field_short for field_short in field_shorts[1:]])

    for i in range(len(params)):
        if (params[i] != None):
            for item in entities:
                setattr(item, field_names[i + 1], field_modifiers[ i + 1 ](params[i]))

    mark_redis_invalid(base_class)

def create(command, base_class, field_shorts, field_names, field_modifiers):
    result = parse(command, field_shorts)
    args = {}
    #print(result)
    for i in range(len(field_names) - 1):
        if field_modifiers[ i + 1](get_joined_value(result, field_shorts[ i + 1], " ")) == None:
            continue;
        args[field_names[i + 1]] = field_modifiers[ i + 1](get_joined_value(result, field_shorts[ i + 1], " "))
    #print(args)
    with db_session:
        new_object = base_class(**args)
    mark_redis_invalid(base_class)
    return new_object

##

def get_create_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    cmd = ""
    for i in range(len(field_status)):
        if field_status[i] == 1:
            opening_brace = " [ "
            closing_brace = " ] "
        elif field_status[i] == 2:
            opening_brace = " "
            closing_brace = " "
        else:
            continue
        cmd += "\n\t"
        cmd += opening_brace + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + closing_brace
    return cmd

def get_read_delete_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    cmd = ""
    for i in range(len(field_status)):
        cmd += "\n\t"
        cmd += " [ " + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + " ] "
    return cmd

def get_update_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    cmd = ""
    for i in range(len(field_status)):
        if field_status[i] == 0:
            continue
        cmd += "\n\t"
        cmd += " [ " + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + " ] "
        cmd += "\n\t"
        cmd += " [ " + "-" + field_shorts[i] + " " + field_names[i] + " " + "new value" + " ] "
    return cmd
