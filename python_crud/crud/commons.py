import parameter_getters
import sys
sys.path.insert(0, '../')

import notifiers


def handle_delete(command, cursor, connection, proc_name):
    if len(command) >= 2:
        args = cursor.callproc(proc_name, [command[1]])
        res = int(args[0])
        connection.commit()
    notifiers.notify_delete(res)

def get_date(string_date):
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
