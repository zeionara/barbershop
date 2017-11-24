import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

table_name = "table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = "
columns = (("date_","-d", "date",20), ("state_code", "-c", "int",10))

def create(command, cursor, connection):
    if len(command) == 4:
        args = cursor.callproc('WORKERS_DATE_STATES_tapi.ins_ins', (int(command[1]),commons.get_date(command[2]),int(command[3])))
        res = int(args[0])
        connection.commit()
    notifiers.notify_insert(res)

def delete(command, cursor, connection):
    if len(command) == 3:
        args = cursor.callproc('WORKERS_DATE_STATES_tapi.del_del', (int(command[1]),commons.get_date(command[2])))
        res = int(args[0])
        connection.commit()
    notifiers.notify_delete(res)

def read(command, cursor, connection):
    field_size = 15
    commons.read_e(table_name, columns, field_size, command, cursor, command[1])
