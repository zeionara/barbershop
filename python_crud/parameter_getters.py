def get_actual(table_name, column_name, ident, cursor):
    return cursor.execute("select %s from %s where id = %s" % (column_name,table_name,ident)).fetchall()[0][0]

def get_parameter(command, code):
    try:
        return command[command.index(code) + 1]
    except ValueError:
        return None

def get_parameter_col(command, code, col):
    try:
        index = command.index(code) + 1
        value = command[index]
        if value[0] != "-":
            return " ".join(command[index : find_next_flag(index + 1, command)])
        return None
    except ValueError:
        return get_parameter_from_collection(col, code)
    
def get_parameter_from_collection(collection, code):
    for item in collection:
        if item[0] == code:
            return item[1]

def get_parameter_def(command, code, table_name, column_name, ident, cursor):
    try:
        return command[command.index(code) + 1]
    except ValueError:
        return get_actual(table_name, column_name, ident, cursor)

def get_last_parameter(command, code):
    try:
        return " ".join(command[(command.index(code) + 1):])
    except ValueError:
        return None

def check_flag(command, code):
    try:
        index = command.index(code)
        return True
    except ValueError:
        return False

def get_parameter_e(command, code):
    try:
        value = command[command.index(code) + 1]
        if value[0] != "-":
            return value
        return None
    except ValueError:
        return None
    except IndexError:
        return None

def find_next_flag(begin_index, command):
    for i in range(begin_index, len(command)):
        if command[i][0] == "-":
            return i
    return len(command)

def get_long_parameter_e(command, code):
    try:
        index = command.index(code) + 1
        value = command[index]
        if value[0] != "-":
            return " ".join(command[index : find_next_flag(index + 1, command)])
        return None
    except ValueError:
        return None
    except IndexError:
        return None
