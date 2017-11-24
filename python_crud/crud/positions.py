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
    if (len(command) == 4) and (command[2] == '-n'):
        args = cursor.callproc('POSITIONS_tapi.upd', (None, int(command[1]), command[3]))
        connection.commit()
        res = int(args[1])
    elif (len(command) > 4) and (command[2] == '-n'):
        args = cursor.callproc('POSITIONS_tapi.upd', (" ".join(command[4:]), int(command[1]), command[3]))
        connection.commit()
        res = int(args[1])
    elif (len(command) > 4):
        args = cursor.callproc('POSITIONS_tapi.upd', (" ".join(command[2:]), int(command[1]), None))
        connection.commit()
        res = int(args[1])
    notifiers.notify_update(res)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)



