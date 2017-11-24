import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "contacts"
columns = (("id", "-ci", "int", 10), ("person_id","-i", "int", 10), ("person_status","-s", "str", 15), ("type","-t", "str", 10), ("contact", "-c", "str", 30))

def create(command, cursor, connection):
    args = cursor.callproc('CONTACTS_tapi.ins', (" ".join(command[4:]), command[2], command[1], 0, command[3]))
    res = args[3]
    connection.commit()
    notifiers.notify_insert(res)

def delete(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('CONTACTS_tapi.del', [command[1]])
        res = int(args[0])
        connection.commit()
    notifiers.notify_delete(res)

def update(command, cursor, connection):
    col = commons.get_unset_fields(command, columns, table_name, cursor)
    args = cursor.callproc('CONTACTS_tapi.upd', (parameter_getters.get_parameter_col(command, "-c", col), parameter_getters.get_parameter_col(command, "-s", col),
           parameter_getters.get_parameter_col(command, "-i", col), command[1],
           parameter_getters.get_parameter_col(command, "-t", col)))
    res = int(args[3])
    connection.commit()
    notifiers.notify_update(res)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)
    
def fake(command, cursor, connection):
    col = get_unset_fields(command, columns, table_name, cursor)
    print((parameter_getters.get_parameter_col(command, "-c", col), parameter_getters.get_parameter_col(command, "-s", col),
           parameter_getters.get_parameter_col(command, "-i", col), command[1],
           parameter_getters.get_parameter_col(command, "-t", col)))
