import sys
sys.path.insert(0, '../')

import cx_Oracle
import notifiers
import parameter_getters
import commons

tapi_name = 'WORKERS_tapi'
table_name = "workers"
#column = (column_name, short_name, type, field_size, parameter_index, insert_index)
#-1 not required
#-2 identifier
#-3 required but need a flag
columns = (('id', '-i', 'int', 10, 6, -2), ('name', '-n', 'str', 15, 7, 1),
           ('surname', '-s', 'str', 20, 1, 2), ('patronymic', '-p', 'str', 20, 3, -1),
           ('sex', '-sx', 'str', 3, 4, 3), ('address', '-a', 'str', 30, 5, -3),
           ('position', '-po', 'int', 20, 0, 4), ('qualification', '-q', 'int', 15, 2, 5),
           ('login', '-l', 'str', 20, 8, 6), ('passwd', '-ps', 'str', 20, 9, 7))

columns_ins = (('id', '-i', 'int', 10, 6, -2), ('name', '-n', 'str', 15, 9, 1),
           ('surname', '-s', 'str', 20, 1, 2), ('patronymic', '-p', 'str', 20, 3, -1),
           ('sex', '-sx', 'str', 3, 4, 3), ('address', '-a', 'str', 30, 5, -3),
           ('position', '-po', 'int', 20, 0, 4), ('qualification', '-q', 'int', 15, 2, 5),
           ('login', '-l', 'str', 20, 7, 6), ('passwd', '-ps', 'str', 20, 8, 7), ('phone','-ph','str',20, 10, -3))


def create(command, cursor, connection):
    commons.create(command, cursor, connection, columns_ins, table_name, tapi_name)

def update(command, cursor, connection):
    commons.update(command, cursor, connection, columns, table_name, tapi_name)

def delete(command, cursor, connection):
    commons.handle_delete(command, cursor, connection, tapi_name)

def read(command, cursor, connection):
    field_size = 15
    commons.read(table_name, columns, field_size, command, cursor)

