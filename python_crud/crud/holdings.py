import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "holdings"
columns = (("id", "-i", "int", 10), ("name","-n", "str", 100), ("price","-p","int", 15), ("quantity","-q","int", 15))

def create(command, cursor, connection):
    if len(command) >= 4:
        args = cursor.callproc('HOLDINGS_tapi.ins', (int(command[2]), int(command[3]), 0, command[1]))
        res = int(args[2])
        connection.commit()
    notifiers.notify_insert(res)

def update(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('HOLDINGS_tapi.upd', (int(parameter_getters.get_parameter(command,"-p")),
                                                     int(parameter_getters.get_parameter(command,"-q")),
                                                     int(command[1]),
                                                     parameter_getters.get_parameter(command,"-n")))
        res = int(args[2])
        connection.commit()
    notifiers.notify_update(res)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, 'HOLDINGS_tapi.del')


def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

