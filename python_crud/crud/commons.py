import parameter_getters
import sys
sys.path.insert(0, '../')

import notifiers
import datetime


def handle_delete(command, cursor, connection, tapi_name):
    if len(command) >= 2:
        args = cursor.callproc(tapi_name+".del", [command[1]])
        res = int(args[0])
        connection.commit()
    notifiers.notify_delete(res)

def get_date(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y').date()

def select(cursor, table_name, columns_to_show, columns_to_check, values_to_check):
    checking_chain = ""
    showing_chain = ""
    if (len(columns_to_show) == 0):
        columns_to_show.append("*")
    for i in range(len(columns_to_show)):
        if showing_chain == "":    
            showing_chain = showing_chain + columns_to_show[i]
        else:
            showing_chain = showing_chain + ", " + columns_to_show[i]
    if (len(columns_to_check) == 0):
        return cursor.execute("select %s from %s" % (showing_chain, table_name))
    for i in range(len(columns_to_check)):
        if checking_chain == "":    
            checking_chain = checking_chain + columns_to_check[i] + " = " + values_to_check[i]
        else:
            checking_chain = checking_chain + " and " + columns_to_check[i] + " = " + values_to_check[i]
    print("select %s from %s where %s" % (showing_chain, table_name, checking_chain))
    return cursor.execute("select %s from %s where %s" % (showing_chain, table_name, checking_chain))

def get_solid_format_string(number_of_entries, length_of_entry):
    format_string = ""
    for i in range(number_of_entries):
        format_string = format_string + "%-" + str(length_of_entry) + "s "
    print(format_string)

def align(x, l):
    xs = str(x)
    if (len(xs) < l):
        xs = xs + " "*(l - len(xs))
    elif (len(xs) > l):
        xs = xs[:l-5] + "...  "
    return xs

def strow(row, l, sizes):
    stro = ""
    index = 0
    #print(sizes)
    #print(row)
    for item in row:
        #print(index)
        stro = stro + align(item, sizes[index])
        index = index + 1
    return stro

def read_e(table_name, columns, field_size, command, cursor, parent_id):
    table_name = table_name + str(parent_id) + ")"
    read(table_name, columns, field_size, command, cursor)


def read(table_name, columns, field_size, command, cursor):
    column_names = [column[0] for column in columns]
    column_shorts = [column[1] for column in columns]
    column_types = [column[2] for column in columns]
    column_sizes = [column[3] for column in columns]
    if parameter_getters.check_flag(command, "-a"):
        print(strow(column_names, field_size))
        for row in select(cursor, table_name,["*"],[],[]).fetchall():
            print(strow(row, field_size))
    else:
        columns_to_show = []
        columns_to_check = []
        values_to_check = []
        sizes_to_show = []
        index = 0
        for column_short in column_shorts:
            if parameter_getters.check_flag(command, column_short):
                parameter = parameter_getters.get_long_parameter_e(command, column_short)
                if (parameter != None):
                    columns_to_check.append(column_names[index])
                    if (column_types[index] == "date"):
                        values_to_check.append("TO_DATE('"+str(parameter)+"', 'dd.mm.yyyy')")
                    elif (column_types[index] == "str") or (column_types[index] == "strs"):
                        values_to_check.append("'"+str(parameter)+"'")
                    else:
                        values_to_check.append(parameter)
                else:
                    columns_to_show.append(column_names[index])
                    sizes_to_show.append(column_sizes[index])
            index += 1
        if (len(columns_to_show) == 0):
            for size in column_sizes:
                sizes_to_show.append(size)
            #print(column_sizes)
            print(strow(column_names, field_size, column_sizes))
        else:
            print(strow(columns_to_show, field_size, sizes_to_show))
        for row in select(cursor, table_name,columns_to_show,columns_to_check,values_to_check).fetchall():
            #print(sizes_to_show)
            print(strow(row, field_size, sizes_to_show))

def get_ent(column):
    return "[ "+column[1]+" [ "+column[0]+" ] ]"

def get_column_shorts(columns):
    return " ".join([get_ent(column) for column in columns]) + " [-a]"

def get_ent_update(column):
    return "[ "+column[1]+" "+column[0]+" ]"

def get_column_shorts_update(columns):
    return columns[0][0] + " " + " ".join([get_ent_update(column) for column in columns[1:]])

def get_columns_lists(command, columns):
    columns_long_names = []
    columns_short_names = []
    for column in columns:
        if (parameter_getters.check_flag(command,column[1]) == False) and (column[0] != "id"):
            columns_long_names.append(column[0])
            columns_short_names.append(column[1])
    return columns_long_names, columns_short_names

def get_unset_fields(command, columns, table_name, cursor):
    columns_long_names, columns_short_names = get_columns_lists(command, columns)
    actual_data = select(cursor, table_name, columns_long_names, ["id"], [str(command[1])]).fetchall()[0]
    print(actual_data)
    unset_fields = []
    for i in range(len(columns_long_names)):
        unset_fields.append((columns_short_names[i], actual_data[i]))
    print(unset_fields)
    return unset_fields

#############
def get_column_by_index(columns, index):
    for column in columns:
        if (column[4] == index):
            return column

def parameter_filter(command, col, short_name, long_name, column_type):
    if long_name == "id":
        return command[1]
    elif column_type == "int":
        return int(parameter_getters.get_parameter_col(command, short_name, col))
    elif column_type == "date":
        return get_date(parameter_getters.get_parameter_col(command,short_name, col))
    else:
        return parameter_getters.get_parameter_col(command,short_name, col)

def get_parameters_for_update(columns, command, col):
    parameters = []
    for i in range(len(columns)):
        column = get_column_by_index(columns, i)
        parameters.append(parameter_filter(command, col, column[1], column[0], column[2]))
    return(tuple(parameters))

def update(command, cursor, connection, columns, table_name, tapi_name):
    if len(command) >= 2:
        col = get_unset_fields(command, columns, table_name, cursor)
        args = cursor.callproc(tapi_name+'.upd', get_parameters_for_update(columns, command, col))
        res = int(args[columns[0][4]])
        connection.commit()
    notifiers.notify_update(res)

#################
def get_column_by_insert_index_cmd(columns, index):
    for column in columns:
        if (column[5] == index):
            return column[0]
    return None

def get_column_shorts_insert(columns):
    seq = []
    for i in range(1,len(columns)):
        long_name = get_column_by_insert_index_cmd(columns, i)
        if long_name == None:
            break;
        seq.append(long_name)
    for column in columns:
        if column[5] == -1:
            seq.append("[ "+column[1]+" "+column[0]+" ]");
    return " ".join(seq)

##

def get_parameters_for_insert(columns, command):
    parameters = []
    for i in range(len(columns)):
        column = get_column_by_index(columns, i)
        parameters.append(parameter_filter_insert(command, column[1], column[0], column[2], column[5]))
    return(tuple(parameters))

def parameter_filter_insert(command, short_name, long_name, column_type, insert_index):
    if long_name == "id":
        return 0
    
    if insert_index > 0:
        pre_parameter = command[insert_index]
    else:
        pre_parameter = parameter_getters.get_parameter_cmd(command, short_name)

    if pre_parameter == None:
        return pre_parameter
    
    if column_type == "int":
        return int(pre_parameter)
    elif column_type == "date":
        return commons.get_date(pre_parameter)
    else:
        return pre_parameter

def create(command, cursor, connection, columns, table_name, tapi_name):
    args = cursor.callproc(tapi_name+'.ins', get_parameters_for_insert(columns, command))
    res = int(args[columns[0][4]])
    connection.commit()
    notifiers.notify_insert(res)
