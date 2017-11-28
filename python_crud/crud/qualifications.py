import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'QUALIFICATIONS_tapi'
table_name = "qualifications"
columns = (('id', '-i', 'int', 10, 1, -2), ('name', '-n', 'str', 15, 2, 1), ('description', '-d', 'str', 20, 0, -1))

def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

