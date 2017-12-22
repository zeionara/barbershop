import re
import datetime
import configparser
import redis
import pickle
import pymongo
from bson.objectid import ObjectId
from serializer import MappedClassJSONEncoder
from connection import create_db_connection

config = configparser.ConfigParser()
config.read('C://Users//Zerbs//accounts.sec')
time_prefix = "timemong"

redis_key_delimiter = "_"
client = create_db_connection(config["mongo"]["login"], config["mongo"]["password"], config["mongo"]["path"])

redis_connection = redis.StrictRedis(host=config['redis']['host'], port=int(config['redis']['port']), db=0)

def write_time_to_redis(key):
    global time_prefix
    global redis_key_delimiter
    str_key = str(key)
    if (str_key[:2] == "b'"):
        str_key = str_key[2:-1]
    print(str_key)
    redis_connection.set(time_prefix + redis_key_delimiter + str_key, pickle.dumps(datetime.datetime.now()))

def get_date(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y')

def get_date_time(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y %H:%M')

def get(value):
    return value

def get_list(value):
    return value.replace(" ","").split(",")

def get_float(value):
    if value == None:
        return None
    return float(value)

def get_worker_date_state_list(value):
    #value = '12.12.2017,e88 ; 12.11.2017, e89 '
    print(">>>>" + value)
    result = []
    pre_result = value.replace(" ","").split(";")
    for item in pre_result:
        pair = item.split(",")
        result.append([get_date(pair[0]), pair[1]])
    return result

def get_holdings_list(value):
    #value = 'e88, 100 ;e89, 200 '
    print(">>>>" + value)
    result = []
    pre_result = value.replace(" ","").split(";")
    for item in pre_result:
        pair = item.split(",")
        result.append([pair[0], get_float(pair[1])])
    return result


##
def find_next_flag(begin_index, command):
    print(command)
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

def get_ids_set(base_class, field_names, field_modifiers, params):

    #client = pymongo.MongoClient('mongodb://%s:%s@%s' % (config["mongo"]["login"],
    #                                               config["mongo"]["password"],
    #                                               config["mongo"]["path"]))

    db = client.barbershopdb

    args = {}
    for i in range(len(field_names)):
        if (params[i] != None):
            if i == 0:
                args[field_names[i]] = params[i]
            else:
                args[field_names[i]] = field_modifiers[i](params[i])

    return [str(item["_id"]) for item in db['holdings'].find(args, {"_id":1})]
    #print(base_class.query.get(**args))
    #return [str(item._id) for item in base_class.query.find(args).all()]

    #return base_class.query.find().all()

def get_properties_tuple(item, field_widths, field_names):
    result = []
    for i in range(len(field_widths)):
        if len(str(getattr(item, field_names[i]))) > field_widths[i]:
            result.append(str(getattr(item, field_names[i]))[:field_widths[i]-5] + "...")
        else:
            result.append(str(getattr(item, field_names[i])))
    return tuple(result)

def get_full_properties_tuple(item, field_names):
    result = []
    for i in range(len(field_names)):
        result.append(str(getattr(item, field_names[i])))
    return tuple(result)

def get_object(field_names, field_values, field_modifiers, base_class):
    args = {}
    for i in range(len(field_names)):
        args[field_names[i]] = field_modifiers[i](field_values[i])
    return base_class.query.get(_id = ObjectId(field_values[0]))
    #return base_class(**args)

def get_entities(command, base_class, field_shorts, field_names, field_modifiers):
    global redis_connection

    collection_name = str(base_class).split("'")[1].split(".")[0]

    full_set = []
    result = parse(command, field_shorts)
    ids = []
    params = get_params(result, field_shorts)
    redis_key = collection_name + redis_key_delimiter + redis_key_delimiter.join([str(param) for param in params])
    get_ids_set(base_class, field_names, field_modifiers, params)
    got_from_redis = redis_connection.get(redis_key)

    if (got_from_redis != None):
        result = [];
        print("got from redis")
        unpacked = pickle.loads(got_from_redis)
    else:
        unpacked = get_ids_set(base_class, field_names, field_modifiers, params)
        redis_connection.set(redis_key, pickle.dumps(unpacked))
        write_time_to_redis(redis_key)
    pipe = redis_connection.pipeline()
    item_keys = []
    for item_id in unpacked:
        item_key = collection_name + redis_key_delimiter + item_id
        item_keys.append(item_key)
        pipe.get(item_key)
        write_time_to_redis(item_key)
    item_params_set = pipe.execute()
    for i in range(len(unpacked)):
        if (item_params_set[i] != None):
            new_objectss = get_object(field_names, pickle.loads(item_params_set[i]), field_modifiers, base_class)
            full_set.append(new_objectss)
        else:
            right_item = base_class.query.get(_id = ObjectId(unpacked[i]))
            full_set.append(right_item)
            redis_connection.set(item_keys[i], pickle.dumps(get_full_properties_tuple(right_item, field_names)))
            write_time_to_redis(item_keys[i])
    #print([str(item,"utf-8") for item in pipe.execute()])
    return full_set

def show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers):
    stre = get_stre(field_widths)
    print(stre % field_names)
    for item in get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        print(stre % get_properties_tuple(item, field_widths, field_names))

def mark_redis_invalid(base_class):
    global redis_connection
    collection_name = str(base_class).split("'")[1].split(".")[0]
    for key in redis_connection.scan_iter(collection_name+"*"):
        print(key)
        redis_connection.delete(key)

##

def check_universal(params):
    for param in params:
        if param != "None":
            return False
    return True

def revise_redis_keys_update(redis_keys, modified_key_params_before, modified_key_params_after, item_id):
    for key in redis_keys:
        current_key_params = str(key)[1:-1].split(redis_key_delimiter)[1:]
        #print(current_key_params)
        #print(modified_key_params_before)
        #print(modified_key_params_after)
        contained = True
        for i in range(len(modified_key_params_before)):
            if (current_key_params[i+1] != "None") and (current_key_params[i+1] != modified_key_params_before[i]):
                contained = False
                break

        contains = True
        for i in range(len(modified_key_params_after)):
            if (current_key_params[i+1] != "None") and (current_key_params[i+1] != modified_key_params_after[i]):
                contains = False
                break

        if contained and not contains:
            old_list = pickle.loads(redis_connection.get(key))
            #print(key," +++ ",old_list," --- ",item_id)
            old_list.remove(item_id)
            redis_connection.set(key, pickle.dumps(old_list))
            write_time_to_redis(key)
        elif not contained and contains:
            redis_connection.set(key, pickle.dumps(pickle.loads(redis_connection.get(key)) + [item_id]))
            write_time_to_redis(key)


def mark_redis_invalid_after_update_enhanced(base_class, modified_key_params_before_set, modified_key_params_after_set, identifiers, collection_name, field_names):
    global redis_connection
    global prefix


    #print(modified_key_params_after_set)
    for i in range(len(modified_key_params_after_set)):
        redis_keys = redis_connection.scan_iter(collection_name+"*" + redis_key_delimiter + "*" + redis_key_delimiter + "*")
        #print("revise for ",identifiers[i])
        revise_redis_keys_update(redis_keys, modified_key_params_before_set[i], modified_key_params_after_set[i], identifiers[i])

def mark_redis_invalid_after_update(base_class, modified_key_params, entities, collection_name, field_names):
    global redis_connection
    global prefix

    if not check_universal(modified_key_params):
        item_keys = []
        pipe = redis_connection.pipeline()
        for item in entities:
            item_id = get_properties_tuple(item, [10 for i in range(len(field_names))], field_names)[0]
            item_key = collection_name + redis_key_delimiter + item_id
            item_keys.append(item_key)
            pipe.get(item_key)
            write_time_to_redis(item_key)

        item_params_set = pipe.execute()
        for i in range(len(entities)):
            if (item_params_set != None):
                redis_connection.set(item_keys[i], pickle.dumps(get_full_properties_tuple(entities[i], field_names)))
                write_time_to_redis(item_keys[i])
            #redis_connection.delete(item_key)

    for key in redis_connection.scan_iter(collection_name+"*" + redis_key_delimiter + "*" + redis_key_delimiter + "*"):
        current_key_params = str(key)[2:-1].split(redis_key_delimiter)[1:]
        #if check_universal(current_key_params) and not check_universal(modified_key_params):
        #    redis_connection.delete(key)
        #    continue
        for i in range(len(modified_key_params)):
            if (modified_key_params[i] != "None") and (current_key_params[i+1] != "None"):
                redis_connection.delete(key)
                break

def revise_redis_keys(redis_keys, modified_key_params, append, item_id):
    for key in redis_keys:
        current_key_params = str(key)[1:-1].split(redis_key_delimiter)[1:]
        #if check_universal(current_key_params):
        #    redis_connection.delete(key)
        #    continue
        broken = False
        for i in range(len(modified_key_params)):
            if (current_key_params[i+1] != "None") and (current_key_params[i+1] != modified_key_params[i]):
                broken = True
                break
        if not broken:
            if append:
                redis_connection.set(key, pickle.dumps(pickle.loads(redis_connection.get(key)) + [item_id]))
                write_time_to_redis(key)
            else:
                old_list = pickle.loads(redis_connection.get(key))
                old_list.remove(item_id)
                redis_connection.set(key, pickle.dumps(old_list))
                write_time_to_redis(key)
            #redis_connection.delete(key)

def mark_redis_invalid_after_create(base_class, modified_key_params, collection_name, field_names, item_id):
    global redis_connection
    global prefix

    redis_keys = redis_connection.scan_iter(collection_name+"*" + redis_key_delimiter + "*" + redis_key_delimiter + "*")
    revise_redis_keys(redis_keys, modified_key_params, True, item_id)

def mark_redis_invalid_after_delete(base_class, deleted_items, collection_name, field_names):
    global redis_connection
    global prefix

    for item in deleted_items:
        redis_keys = redis_connection.scan_iter(collection_name+"*" + redis_key_delimiter + "*" + redis_key_delimiter + "*")
        redis_connection.delete(collection_name + redis_key_delimiter + str(item._id))
        modified_key_params = get_full_properties_tuple(item, field_names)[1:]
        revise_redis_keys(redis_keys, modified_key_params, False, str(item._id))

##

def delete(command, base_class, field_shorts, field_names, field_modifiers, session):
    collection_name = str(base_class).split("'")[1].split(".")[0]
    entities = get_entities(command, base_class, field_shorts, field_names, field_modifiers)
    for item in entities:
        item.delete()
    session.flush_all()
    mark_redis_invalid_after_delete(base_class, entities, collection_name, field_names)
    #mark_redis_invalid(base_class)

def update(command, base_class, field_shorts, field_names, field_modifiers, session):
    entities = get_entities(command, base_class, field_shorts, field_names, field_modifiers)
    result = parse(command, ["-"+field_short for field_short in field_shorts[1:]])
    params = get_params(result,["-"+field_short for field_short in field_shorts[1:]])

    collection_name = str(base_class).split("'")[1].split(".")[0]
    modified_key_params_before_set = []
    modified_key_params_after_set = []
    identifiers = []

    for item in entities:
        modified_key_params_before_set.append(get_full_properties_tuple(item, field_names)[1:])

    for i in range(len(params)):
        if (params[i] != None):
            for item in entities:
                setattr(item, field_names[i + 1], field_modifiers[ i + 1 ](params[i]))

    session.flush_all()

    for item in entities:
        identifiers.append(str(item._id))
        modified_key_params_after_set.append(get_full_properties_tuple(item, field_names)[1:])


    if not check_universal([str(param) for param in params]):
        item_keys = []
        pipe = redis_connection.pipeline()
        for item in entities:
            item_id = get_full_properties_tuple(item, field_names)[0]
            item_key = collection_name + redis_key_delimiter + item_id
            item_keys.append(item_key)
            pipe.get(item_key)
            write_time_to_redis(item_key)
        item_params_set = pipe.execute()
        for i in range(len(entities)):
            if (item_params_set != None):
                redis_connection.set(item_keys[i], pickle.dumps(get_full_properties_tuple(entities[i], field_names)))
                write_time_to_redis(item_keys[i])

    mark_redis_invalid_after_update_enhanced(base_class, modified_key_params_before_set, modified_key_params_after_set, identifiers, collection_name, field_names)
    #mark_redis_invalid(base_class)

def create(command, base_class, field_shorts, field_names, field_modifiers, session):
    result = parse(command, field_shorts)
    args = {}
    collection_name = str(base_class).split("'")[1].split(".")[0]
    params = []

    for i in range(len(field_names) - 1):
        params.append(str(get_joined_value(result, field_shorts[ i + 1], " ")))
        if field_modifiers[ i + 1](get_joined_value(result, field_shorts[ i + 1], " ")) == None:
            continue;
        args[field_names[i + 1]] = field_modifiers[ i + 1](get_joined_value(result, field_shorts[ i + 1], " "))

    new_object = base_class(**args)
    session.flush_all()

    item_key = collection_name + redis_key_delimiter + str(new_object._id)
    redis_connection.set(item_key, pickle.dumps(get_full_properties_tuple(new_object, field_names)))

    mark_redis_invalid_after_create(base_class, params, collection_name, field_names, str(new_object._id))
    return new_object

##

def get_create_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    for i in range(len(field_status)):
        if field_status[i] == 1:
            opening_brace = " [ "
            closing_brace = " ] "
        elif field_status[i] == 2:
            opening_brace = " "
            closing_brace = " "
        else:
            continue
        cmd += opening_brace + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + closing_brace
    return cmd

def get_read_delete_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    for i in range(len(field_status)):
        cmd += " [ " + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + " ] "
    return cmd

def get_update_rules(cmd, field_status, field_shorts, field_names, field_descriptions):
    for i in range(len(field_status)):
        if field_status[i] == 0:
            continue
        cmd += " [ " + field_shorts[i] + " " + field_names[i] + " " + field_descriptions[i] + " ] "
        cmd += " [ " + "-" + field_shorts[i] + " " + field_names[i] + " " + "new value" + " ] "
    return cmd
