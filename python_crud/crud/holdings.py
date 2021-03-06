import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'HOLDINGS_tapi'
table_name = "holdings"
columns = (("id", "-i", "int", 10, 2, -2), ("name","-n", "str", 100, 3, 1), ("price","-p","int", 15, 0, 2), ("quantity","-q","int", 15, 1, 3))

def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

