import parameter_getters
import sys
sys.path.insert(0, '../')

import notifiers
import datetime
import connection

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

def get_datetime(string_date):
    if (isinstance(string_date,datetime.datetime)):
        return string_date
    return datetime.datetime.strptime(string_date, '%d.%m.%Y_%H:%M')

def select(cursor, table_name, columns_to_show, columns_to_check, values_to_check):
    #print(connection.redis_connector.get("foo"))
    key = "_".join([table_name,"_".join(columns_to_show),"_".join(columns_to_check),"_".join(values_to_check)])
    redis_response = connection.redis_connector.get(key)
    try:
        is_relevant = str(connection.redis_connector.get(table_name+"_is_relevant"),"utf-8").replace('\'','')
    except TypeError:
        is_relevant = "False"
    #print(is_relevant)
    if (redis_response != None) and (is_relevant == "True"):
        #print("Got from redis!")
        return rebuild_list(str(redis_response,"utf-8"))
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
        result = cursor.execute("select %s from %s" % (showing_chain, table_name))
        connection.redis_connector.set(key, [row for row in result])
        connection.redis_connector.set(table_name+"_is_relevant","True")
        return cursor.execute("select %s from %s" % (showing_chain, table_name)).fetchall()
    for i in range(len(columns_to_check)):
        if checking_chain == "":    
            checking_chain = checking_chain + columns_to_check[i] + " = " + values_to_check[i]
        else:
            checking_chain = checking_chain + " and " + columns_to_check[i] + " = " + values_to_check[i]
    result = cursor.execute("select %s from %s where %s" % (showing_chain, table_name, checking_chain))
    connection.redis_connector.set(key, [row for row in result])
    connection.redis_connector.set(table_name+"_is_relevant","True")
    #print("select %s from %s where %s" % (showing_chain, table_name, checking_chain))
    return cursor.execute("select %s from %s where %s" % (showing_chain, table_name, checking_chain)).fetchall()

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
    row = row[:len(sizes)]
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
        for row in select(cursor, table_name,["*"],[],[]):
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
        for row in select(cursor, table_name,columns_to_show,columns_to_check,values_to_check):
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
    actual_data = select(cursor, table_name, columns_long_names, ["id"], [str(command[1])])[0]
    print(actual_data)
    unset_fields = []
    for i in range(len(columns_long_names)):
        unset_fields.append((columns_short_names[i], actual_data[i]))
    print(unset_fields)
    return unset_fields

#############
def get_column_by_index(columns, index):
    print("search for %s" % str(index))
    for column in columns:
        print(column)
        if (column[4] == index):
            return column

def parameter_filter(command, col, short_name, long_name, column_type):
    if long_name == "id":
        return command[1]
    elif column_type == "int":
        return int(parameter_getters.get_parameter_col(command, short_name, col))
    elif column_type == "date":
        return get_date(parameter_getters.get_parameter_col(command,short_name, col))
    elif column_type == "time":
        return get_datetime(parameter_getters.get_parameter_col(command,short_name, col))
    else:
        return parameter_getters.get_parameter_col(command,short_name, col)

def get_parameters_for_update(columns, command, col):
    parameters = []
    for i in range(len(columns)):
        column = get_column_by_index(columns, i)
        parameters.append(parameter_filter(command, col, column[1], column[0], column[2]))
    return(tuple(parameters))

def update(command, cursor, conn, columns, table_name, tapi_name):
    if len(command) >= 2:
        col = get_unset_fields(command, columns, table_name, cursor)
        args = cursor.callproc(tapi_name+'.upd', get_parameters_for_update(columns, command, col))
        res = int(args[columns[0][4]])
        conn.commit()
    notifiers.notify_update(res)
    connection.redis_connector.set(table_name+"_is_relevant","False")

def update_e(command, cursor, conn, columns, table_name, tapi_name, parent_id):
    table_name = table_name + str(parent_id) + ")"
    update(command, cursor, conn, columns, table_name, tapi_name)

def delete_e(command, cursor, connection, tapi_name, parent_id, id_type):
    if (id_type == "date"):
        command[1] = get_date(command[1])
    print((parent_id,command[1]))
    args = cursor.callproc(tapi_name+".del", (parent_id,command[1]))
    res = int(args[0])
    connection.commit()
    notifiers.notify_delete(res)

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
        if column[5] == -3:
            seq.append("< "+column[1]+" "+column[0]+" >");
    return " ".join(seq)

##

def get_parameters_for_insert(columns, command):
    parameters = []
    print(columns)
    for i in range(len(columns)):
        column = get_column_by_index(columns, i)
        print(column)
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
        return get_date(pre_parameter)
    elif column_type == "time":
        print("time")
        print(get_datetime(pre_parameter))
        return get_datetime(pre_parameter)
    else:
        return pre_parameter

def create(command, cursor, conn, columns, table_name, tapi_name):
    print(get_parameters_for_insert(columns, command))
    argss = get_parameters_for_insert(columns, command)
    ss = [2]
    for arg in argss:
        ss.append(arg)
    
    args = cursor.callproc(tapi_name+'.ins', ss)
    res = int(args[columns[0][4]])
    conn.commit()
    notifiers.notify_insert(res)
    connection.redis_connector.set(table_name+"_is_relevant","False")

###REDIS

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_float(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False
def parse_type(string):
    if string == "None":
        return None
    if is_int(string):
        return int(string)
    if is_float(string):
        return float(string)
    if (str.find(string,"DATETIME") != -1):
        #print(string)
        arr = [int(elem.rstrip().lstrip()) for elem in string[string.index("<")+1:string.index(">")].split("#")]
        return datetime.datetime(arr[0],arr[1],arr[2],arr[3],arr[4])
    return string

def replace(string, index, character):
    return string[:index] + character + string[index+1:]

def rebuild_list(fi):
    result = []
    #print(fi)
    while (str.find(fi,"datetime.datetime") != -1):
        #print(fi)
        
        beg = str.find(fi,"datetime.datetime")
        #print(beg)
        #print(fi.find("(",beg))
        start = fi.find("(",beg)
        fi = replace(fi, fi.find("(",beg), "<")
        end = fi.find(")",beg)
        fi = replace(fi, fi.find(")",beg), ">")
        ind = fi.find(",",start, end)
        while (ind != -1):
            fi = replace(fi, ind, "#")
            ind = fi.find(",",start, end)

        fi = fi.replace("datetime.datetime","DATETIME",1)
        #print(fi)
    #print(fi)
    for row in str.split(fi,"),"):
        row_splitted = row.replace("[","").replace("(","").replace("]","").replace(")","").split(",")
        row_rebuilt = [parse_type(row_el.lstrip().rstrip().replace("\'","").replace("\"","")) for row_el in row_splitted]
        result.append(tuple(row_rebuilt))
    return result
    
