import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "services"
columns = (("id", "-i", "int", 10), ("name","-n", "str", 30), ("price","-p", "int", 15), ("description","-d", "str", 50), ("avg_duration", "-a", "int", 30))


def create(command, cursor, connection):
    if len(command) == 3:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], None, 0, None, command[1]))
        res = int(args[2])
        connection.commit()
    elif len(command) == 4:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], None, 0, command[3], command[1]))
        res = int(args[2])
        connection.commit()
    elif len(command) >= 4:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], command[4:], 0, command[3], command[1]))
        res = int(args[2])
        connection.commit()
    notifiers.notify_insert(res)


def update(command, cursor, connection):
    col = commons.get_unset_fields(command, columns, table_name, cursor)
    args = cursor.callproc('SERVICES_tapi.upd', (parameter_getters.get_parameter_col(command, "-p", col),
                                                 parameter_getters.get_parameter_col(command, "-d", col),
                                                 command[1],
                                                 parameter_getters.get_parameter_col(command, "-a", col),
                                                 parameter_getters.get_parameter_col(command, "-n", col)))
    res = int(args[2])
    connection.commit()
        
    notifiers.notify_update(res)

def delete(command, cursor, connection):
    handle_delete(command, cursor, connection, 'SERVICES_tapi.del')

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

