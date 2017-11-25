import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'CLIENTS_tapi'
table_name = "clients"
#column = (column_name, short_name, type, field_size, parameter_index, insert_index)

def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

