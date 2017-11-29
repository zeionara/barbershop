import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = "NESTED_STATES_tapi"
table_name = "table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = "
columns = (("date_","-d", "date",20,0,1), ("state_code", "-s", "int",10,1,2))

def create(command, cursor, connection):
    parent_id = command[1]
    command = command[:1] + command[2:]
    commons.create(command, cursor, connection, columns, table_name + str(parent_id) + ")", tapi_name)

def delete(command, cursor, connection):
    parent_id = command[1]
    command = command[:1] + command[2:]
    commons.delete_e(command, cursor, connection, tapi_name, parent_id, "date")

def read(command, cursor, connection):
    field_size = 15
    commons.read_e(table_name, columns, field_size, command, cursor, command[1])
