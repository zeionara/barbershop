import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import commons
import parameter_getters

table_name = "workers_states"
columns = (("id", "-i", "int", 10), ("name","-n", "str", 20), ("description","-d", "str", 50))

def create(command, cursor, connection):
    if len(command) == 2:
        res = cursor.callfunc('WORKERS_STATES_tapi.ins_f', cx_Oracle.NUMBER, (None, command[1]))
        connection.commit()
    elif len(command) > 2:
        res = cursor.callfunc('WORKERS_STATES_tapi.ins_f', cx_Oracle.NUMBER, (" ".join(command[2:]), command[1]))
        connection.commit()
    notifiers.notify_insert(res)

def delete(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('WORKERS_STATES_tapi.del', [command[1]])
        res = args[0]
        connection.commit()
    notifiers.notify_delete(res)

def update(command, cursor, connection):
    col = commons.get_unset_fields(command, columns, table_name, cursor)
    res = cursor.callproc('WORKERS_STATES_tapi.upd', (parameter_getters.get_parameter_col(command, "-d", col), int(command[1]),
                                                      parameter_getters.get_parameter_col(command, "-n", col)))
    connection.commit()
    res = int(command[1])
    notifiers.notify_update(res)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)
