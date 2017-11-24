import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons
import datetime

table_name = "premiums"
columns = (("id", "-i","int",10), ("premium_id","-p","int",10), ("worker_id","-w","int",10),
           ("earning_date","-e","date",50), ("premium_size", "-s","int",15), ("note","-n","str",50))

def create(command, cursor, connection):
    if len(command) == 5:
        args = cursor.callproc('PREMIUMS_tapi.ins', (int(command[2]),int(command[1]),get_date(command[3]),None,0,command[4]))
        res = int(args[4])
        connection.commit()
    elif len(command) >= 6:
        args = cursor.callproc('PREMIUMS_tapi.ins', (int(command[2]),int(command[1]),get_date(command[3])," ".join(command[5:]),0,command[4]))
        res = int(args[4])
        connection.commit()
    notifiers.notify_insert(res)

def update(command, cursor, connection):
    if len(command) >= 2:
        col = commons.get_unset_fields(command, columns, table_name, cursor)
        
        args = cursor.callproc('PREMIUMS_tapi.upd', (int(parameter_getters.get_parameter_col(command,"-p",col)),
                                                     int(parameter_getters.get_parameter_col(command,"-w",col)),
                                                     commons.get_date(parameter_getters.get_parameter_col(command,"-e",col)),
                                                     parameter_getters.get_parameter_col(command,"-d",col),
                                                     command[1],
                                                     parameter_getters.get_parameter_col(command,"-s",col)))
        res = int(args[4])
        connection.commit()
    notifiers.notify_update(res)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, 'PREMIUMS_tapi.del')


def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

