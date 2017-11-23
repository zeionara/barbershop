import cx_Oracle
import configparser
import datetime

commands = (('get_schedule','gs', 'master_id [date_of_visit_in_format_10.10.2010]'),
            ('create_worker_state','cws','state_name [state_description]'),
            ('delete_worker_state','dws','state_id'),
            ('update_worker_state','uws','state_id [-n new_name] [new_description]'))


def establish_connection(ip, port, sid):
    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")
    return (db.cursor(), db)

def notify(operation, ident):
    print("%s item with id %i" % (operation, ident))

def notify_insert(ident):
    notify("Inserted",ident)

def notify_delete(ident):
    notify("Deleted",ident)

def notify_update(ident):
    notify("Updated",ident)

def list_all_commands():
    print('%-20s %-10s %-50s' % ('name','short name','arguments'))
    for command in commands:
        print('%-20s %-10s %-50s' % command)

def handle_get_schedule(command, cursor):
    if len(command) == 3:
        cursor.execute("select * from table(select barbershop.get_clients_list_as_strings(%s, TO_DATE('%s', 'dd.mm.yyyy')) from dual)" % (command[1], command[2]))
    else:
        now = datetime.datetime.now()
        cursor.execute("select * from table(select barbershop.get_clients_list_as_strings(%s, TO_DATE('%s', 'dd.mm.yyyy')) from dual)"
                       % (command[1], (str(now.day)+'.'+str(now.month)+'.'+str(now.year))))
    print("%-10s %-20s %-20s %-20s" % ('имя','отчество','телефон','время записи'));
    for row in cursor:
        print("%-10s %-20s %-20s %-20s" % row);

def handle_create_worker_state(command, cursor, connection):
    if len(command) == 2:
        res = cursor.callfunc('WORKERS_STATES_tapi.ins_f', cx_Oracle.NUMBER, (None, command[1]))
        conn.commit()
    elif len(command) > 2:
        res = cursor.callfunc('WORKERS_STATES_tapi.ins_f', cx_Oracle.NUMBER, (" ".join(command[2:]), command[1]))
        conn.commit()
    notify_insert(res)
    #print("Inserted item with id %i" % res)

def handle_delete_worker_state(command, cursor, connection):
    if len(command) >= 2:
        res = cursor.callproc('WORKERS_STATES_tapi.del', [command[1]])
        conn.commit()
    notify_delete(res)
    #print("Deleted item with id %s" % res[0])

def handle_update_worker_state(command, cursor, connection):
    if (len(command) == 4) and (command[2] == '-n'):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (None, int(command[1]), command[3]))
        conn.commit()
        res = int(command[1])
    elif (len(command) > 4) and (command[2] == '-n'):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (" ".join(command[4:]), int(command[1]), command[3]))
        conn.commit()
        res = int(command[1])
    elif (len(command) > 4):
        res = cursor.callproc('WORKERS_STATES_tapi.upd', (" ".join(command[2:]), int(command[1]), None))
        conn.commit()
        res = int(command[1])
    notify_update(res)
    #print("Updated item with id %i" % res) 

#main

if __name__ == '__main__':
    result = establish_connection('127.0.0.1',1521,'orbis')
    cursor = result[0]
    
    conn = result[1]
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');
        print('\n\nresult:\n\n');
        if command[0] == 'list':
            list_all_commands()
        elif command[0] == 'gs':
            handle_get_schedule(command, cursor)
        elif command[0] == 'cws':
            handle_create_worker_state(command, cursor, conn)
        elif command[0] == 'dws':
            handle_delete_worker_state(command, cursor, conn)
        elif command[0] == 'uws':
            handle_update_worker_state(command, cursor, conn)
        elif command[0] == 'exit':
            break;
    
