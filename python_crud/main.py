import cx_Oracle
import configparser
import datetime
import sys
import redis
sys.path.insert(0, 'crud/')
sys.path.insert(0, 'extra/')
sys.path.insert(0, 'sys/')

import notifiers
import parameter_getters
import connection


import worker_states
import positions
import contacts
import services
import holdings
import salaries
import premium_sizes
import premiums
import nested_states
import commons

import get_schedule

import list_all_commands

import command_storage

if __name__ == '__main__':
    result = connection.establish('127.0.0.1',1521,'orbis')
    cursor = result[0]
    conn = result[1]
    #print(cursor.execute("select * from table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = 2)").fetchall())
    print(parameter_getters.get_long_parameter_e(["a","b","-c","Hello","my","friend","!","op"],"-c"))
    print(commons.select(cursor, "services",["*"],["id"],["1"]))
    print(cursor.execute("select * from premiums").fetchall())
    #print(connection.redis_connector.get("foo"))
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');
        
        if command[0] == 'list':
            list_all_commands.execute()
        elif command[0] == 'exit':
            break;
        else:
            print('\n\nresult:\n\n');
            command_storage.get_handler(command[0])(command, cursor, conn)
        
    
