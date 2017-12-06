import re

def get(value):
    return value

def get_float(value):
    return float(value)
##
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

def show_entities(command, base_class, field_shorts, field_names, field_widths, field_modifiers):
    full_set = get_full_set(base_class)
    result = parse(command, field_shorts)

    params = get_params(result, field_shorts)

    for i in range(len(params)):
        if (params[i] != None):
            intermediate_set = []
            for item in full_set:
                if ((getattr(item, field_names[i]) == field_modifiers[i](params[i])) and (i > 0)) or \
                    ((str(getattr(item, field_names[i]))[-len(params[i]):] == params[i]) and (i == 0)):
                    intermediate_set.append(item)
            full_set = intermediate_set

    stre = get_stre(field_widths)
    print(field_names)
    print(stre % field_names)
    for item in full_set:
        print(stre % tuple([str(getattr(item, field_name)) for field_name in field_names]))

def get_entities(command, base_class, field_shorts, field_names, field_modifiers):
    full_set = get_full_set(base_class)
    result = parse(command, field_shorts)

    params = get_params(result, field_shorts)

    for i in range(len(params)):
        print(full_set)
        if (params[i] != None):
            intermediate_set = []
            for item in full_set:
                if ((getattr(item, field_names[i]) == field_modifiers[i](params[i])) and (i > 0)) or \
                    ((str(getattr(item, field_names[i]))[-len(params[i]):] == params[i]) and (i == 0)):
                    intermediate_set.append(item)
            full_set = intermediate_set
        print(full_set)

    return full_set

##

def delete(command, base_class, field_shorts, field_names, field_modifiers, session):
    for item in get_entities(command, base_class, field_shorts, field_names, field_modifiers):
        item.delete()

    session.flush_all()

def update(command, base_class, field_shorts, field_names, field_modifiers, session):
    entities = get_entities(command, base_class, field_shorts, field_names, field_modifiers)
    result = parse(command, ["-"+field_short for field_short in field_shorts[1:]])

    params = get_params(result,["-"+field_short for field_short in field_shorts[1:]])
    print("-"*40)
    print(params)
    print(entities)

    for i in range(len(params)):
        if (params[i] != None):
            for item in entities:
                setattr(item, field_names[i + 1], field_modifiers[ i + 1 ](params[i]))

    session.flush_all()

def create(command, base_class, field_shorts, field_names, field_modifiers, session):
    result = parse(command, field_shorts)
    args = {}
    for i in range(len(field_names) - 1):
        args[field_names[i + 1]] = field_modifiers[ i + 1](get_joined_value(result, field_shorts[ i + 1], " "))
    print(args)
    base_class(**args)
    session.flush_all()

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
