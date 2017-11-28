import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'REQUESTS_tapi'
table_name = "requests"
columns = (('id', '-i', 'int', 10, 5, -2), ('visit_date_time', '-v', 'time', 20, 1, 1),
           ('worker_id', '-w', 'int', 10, 0, 2), ('client_id', '-c', 'int', 10, 2, 3),
           ('service_id', '-s', 'int', 10, 4, 4), ('note', '-n', 'str', 50, 3, -1))

def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

