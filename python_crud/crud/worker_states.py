import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers

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
    if (len(command) == 4) and (command[2] == '-n'):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (None, int(command[1]), command[3]))
        connection.commit()
        res = int(command[1])
    elif (len(command) > 4) and (command[2] == '-n'):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (" ".join(command[4:]), int(command[1]), command[3]))
        connection.commit()
        res = int(command[1])
    elif (len(command) > 4):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (" ".join(command[2:]), int(command[1]), None))
        connection.commit()
        res = int(command[1])
    notifiers.notify_update(res)
