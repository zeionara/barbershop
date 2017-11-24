import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "premiums_sizes"
columns = (("id", "-i", "int", 10), ("name","-n", "str", 20), ("min","-min", "int", 15), ("max","-max", "int", 15), ("description", "-d", "str", 50))


def create(command, cursor, connection):
    if len(command) >= 5:
        args = cursor.callproc('PREMIUMS_SIZES_tapi.ins', (int(command[2]), int(command[3]), " ".join(command[4:]), 0, command[1]))
        res = int(args[3])
        connection.commit()
    notifiers.notify_insert(res)

def update(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('PREMIUMS_SIZES_tapi.upd', (int(parameter_getters.get_parameter(command, "-min")),
                                                           int(parameter_getters.get_parameter(command, "-max")),
                                                           parameter_getters.get_last_parameter(command, "-d"),
                                                           command[1],
                                                           parameter_getters.get_parameter(command, "-n")))
        res = int(args[3])
        connection.commit()
    notifiers.notify_update(res)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, 'PREMIUMS_SIZES_tapi.del')

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)
