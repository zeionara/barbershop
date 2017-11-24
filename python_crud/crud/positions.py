import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import commons
import parameter_getters


table_name = "positions"
columns = (("id", "-i", "int", 10), ("name","-n", "str", 30), ("description","-d", "str", 50))

def create(command, cursor, connection):
    if len(command) == 2:
        args = cursor.callproc('POSITIONS_tapi.ins', (None, 5, command[1]))
        res = args[1]
        connection.commit()
    elif len(command) > 2:
        args = cursor.callproc('POSITIONS_tapi.ins', (" ".join(command[2:]), command[1]))
        res = args[1]
        connection.commit()
    notifiers.notify_insert(res)

def delete(command, cursor, connection):
    if len(command) >= 2:
        res = cursor.callproc('POSITIONS_tapi.del', [command[1]])
        connection.commit()
    notifiers.notify_delete(res)

def update(command, cursor, connection):
    col = commons.get_unset_fields(command, columns, table_name, cursor)
    args = cursor.callproc('POSITIONS_tapi.upd', (parameter_getters.get_parameter_col(command, "-d", col),
                                                  int(command[1]),
                                                  parameter_getters.get_parameter_col(command, "-n", col)))
    connection.commit()
    res = int(args[1])

    notifiers.notify_update(res)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)



