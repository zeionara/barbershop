import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "salaries"
columns = (("id", "-i", "int", 10), ("worker_id","-w", "int", 10), ("common","-c", "int", 15), ("vacation","-v", "int", 10), ("sick", "-s", "int", 10))


def create(command, cursor, connection):
    if len(command) >= 5:
        args = cursor.callproc('SALARIES_tapi.ins', (int(command[1]), int(command[3]), int(command[4]), int(command[2]), 0))
        res = int(args[4])
        connection.commit()
    notifiers.notify_insert(res)

def update(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('SALARIES_tapi.upd', (int(parameter_getters.get_parameter(command, "-i")),
                                                     int(parameter_getters.get_parameter(command, "-v")),
                                                     int(parameter_getters.get_parameter(command, "-s")),
                                                     int(parameter_getters.get_parameter(command, "-c")),
                                                     int(command[1])))
        res = int(args[4])
        connection.commit()
    notifiers.notify_update(res)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, 'SALARIES_tapi.del')

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)
