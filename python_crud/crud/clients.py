import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'CLIENTS_tapi'
table_name = "clients"
#column = (column_name, short_name, type, field_size, parameter_index, insert_index)
#-1 not required
#-2 identifier
#-3 required but need a flag
columns = (('id', '-i', 'int', 10, 4, -2), ('name', '-n', 'str', 15, 5, 0),
           ('surname', '-s', 'str', 20, 0, 1), ('patronymic', '-p', 'str', 20, 1, -1),
           ('sex', '-sx', 'str', 3, 2, 2), ('address', '-a', 'str', 30, 3, 3),
           ('login', '-l', 'str', 20, 6, 4), ('passwd', '-ps', 'str', 20, 7, 5))

columns_ins = (('id', '-i', 'int', 10, 4, -2), ('name', '-n', 'str', 15, 5, 1),
               ('surname', '-s', 'str', 20, 0, 2), ('patronymic', '-p', 'str', 20, 1, -1),
               ('sex', '-sx', 'str', 3, 2, 3), ('address', '-a', 'str', 30, 3, -3),
               ('login', '-l', 'str', 20, 6, 4), ('passwd', '-ps', 'str', 20, 7, 5), ('phone','-ph','str',20, 8, -3))


def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns_ins, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

