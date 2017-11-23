import cx_Oracle
import configparser
import datetime

commands = (('get_schedule','gs', 'master_id [date_of_visit_in_format_10.10.2010]'),
            ('create_worker_state','cws','state_name [state_description]'),
            ('delete_worker_state','dws','state_id'),
            ('update_worker_state','uws','state_id [-n new_name] [new_description]'),
            ('create_position','cp','position_name [position_description]'),
            ('delete_position','dp','state_id'),
            ('update_position','up','state_id [-n new_name] [new_description]'),
            ('create_contact','cc','person_id person_status contact_type contact'),
            ('delete_contact','dc','contact_id'),
            ('update_contact','uc','contact_id [-i person_id] [-s person_status] [-t contact_type] [-c contact]'),
            ('create_service','cs','service_name price [service_average_duration] [service_description]'),
            ('update_service','us','service_id [-n service_name] [-p price] [-a service_average_duration] [-d service_description]'),
            ('delete_service','ds','service_id'),
            ('create_holding','ch','holding_name price quantity'),
            ('update_holding','uh','holding_id [-n holding_name] [-p price] [-q quantity]'),
            ('delete_holding','dh','holding_id'),
            ('create_salary','csl','worker_id common vacation sick'),
            ('update_salary','usl','salary_id [-i worker_id] [-c common] [-v vacation] [-s sick]'),
            ('delete_salary','dsl','salary_id'),
            ('create_premium_size','cps','premium_name minimal_value maximal_value [description]'),
            ('update_premium_size','ups','premium_id [-n name] [-min minimal_value] [-max maximal_value] [-d description]'),
            ('delete_premium_size','dps','premium_id'),
            ('create_premium','cpr','worker_id premium_id earning_date_in_format_10.10.2010 premium_size [note]'),
            ('update_premium','upr','premium_id [-w worker_id] [-p preium_id] [-e earning_date in format 10.10.2010] [-s premium_size] [-d note]'),
            ('delete_premium','dpr','premium_id'),
            ('create_worker_day_state','cwds','worker_id date_in_format_10.10.2010 state_id'),
            ('delete_worker_day_state','dwds','worker_id date_in_format_10.10.2010'))

def get_actual(table_name, column_name, ident):
    return cursor.execute("select %s from %s where id = %s" % (column_name,table_name,ident)).fetchall()[0][0]

def get_date(string_date):
    return datetime.datetime.strptime(string_date, '%d.%m.%Y').date()

def establish_connection(ip, port, sid):
    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")
    return (db.cursor(), db)

def get_parameter(command, code):
    try:
        return command[command.index(code) + 1]
    except ValueError:
        return None

def get_parameter_def(command, code, table_name, column_name, ident):
    try:
        return command[command.index(code) + 1]
    except ValueError:
        return get_actual(table_name, column_name, ident)

def get_last_parameter(command, code):
    try:
        return " ".join(command[(command.index(code) + 1):])
    except ValueError:
        return None

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

def handle_delete(command, cursor, connection, proc_name):
    if len(command) >= 2:
        args = cursor.callproc(proc_name, [command[1]])
        res = int(args[0])
        conn.commit()
    notify_delete(res)


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

def handle_delete_worker_state(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('WORKERS_STATES_tapi.del', [command[1]])
        res = args[0]
        conn.commit()
    notify_delete(res)

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

def handle_create_position(command, cursor, connection):
    if len(command) == 2:
        args = cursor.callproc('POSITIONS_tapi.ins', (None, 5, command[1]))
        res = args[1]
        conn.commit()
    elif len(command) > 2:
        args = cursor.callproc('POSITIONS_tapi.ins', (" ".join(command[2:]), command[1]))
        res = args[1]
        conn.commit()
    notify_insert(res)

def handle_delete_position(command, cursor, connection):
    if len(command) >= 2:
        print("del...")
        res = cursor.callproc('POSITIONS_tapi.del', [command[1]])
        print("del...")
        conn.commit()
    notify_delete(res)

def handle_update_position(command, cursor, connection):
    if (len(command) == 4) and (command[2] == '-n'):
        args = cursor.callproc('POSITIONS_tapi.upd', (None, int(command[1]), command[3]))
        conn.commit()
        res = int(args[1])
    elif (len(command) > 4) and (command[2] == '-n'):
        args = cursor.callproc('POSITIONS_tapi.upd', (" ".join(command[4:]), int(command[1]), command[3]))
        conn.commit()
        res = int(args[1])
    elif (len(command) > 4):
        args = cursor.callproc('POSITIONS_tapi.upd', (" ".join(command[2:]), int(command[1]), None))
        conn.commit()
        res = int(args[1])
    notify_update(res)

def handle_create_contact(command, cursor, connection):
    #print(command)
    args = cursor.callproc('CONTACTS_tapi.ins', (" ".join(command[4:]), command[2], command[1], 0, command[3]))
    res = args[3]
    conn.commit()
    notify_insert(res)

def handle_delete_contact(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('CONTACTS_tapi.del', [command[1]])
        res = int(args[0])
        conn.commit()
    notify_delete(res)

def handle_update_contact(command, cursor, connection):
    args = cursor.callproc('CONTACTS_tapi.upd', (get_parameter_def(command, "-c", "contacts", "contact", str(command[1])),
                                                 get_parameter_def(command, "-s", "contacts", "person_status", str(command[1])),
                                                 get_parameter_def(command, "-i", "contacts", "person_id", str(command[1])),
                                                 command[1],
                                                 get_parameter_def(command, "-t", "contacts", "type", str(command[1]))))
    res = int(args[3])
    conn.commit()
    notify_update(res)

def handle_create_service(command, cursor, connection):
    if len(command) == 3:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], None, 0, None, command[1]))
        res = int(args[2])
        conn.commit()
    elif len(command) == 4:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], None, 0, command[3], command[1]))
        res = int(args[2])
        conn.commit()
    elif len(command) >= 4:
        args = cursor.callproc('SERVICES_tapi.ins', (command[2], command[4:], 0, command[3], command[1]))
        res = int(args[2])
        conn.commit()
    notify_insert(res)


def handle_update_service(command, cursor, connection):
    args = cursor.callproc('SERVICES_tapi.upd', (get_parameter(command, "-p"), get_last_parameter(command, "-d"),
                                                     command[1], get_parameter(command, "-a"), get_parameter(command, "-n")))
    res = int(args[2])
    conn.commit()
        
    notify_insert(res)

def handle_delete_service(command, cursor, connection):
    handle_delete(command, cursor, connection, 'SERVICES_tapi.del')

def handle_create_holding(command, cursor, connection):
    if len(command) >= 4:
        args = cursor.callproc('HOLDINGS_tapi.ins', (int(command[2]), int(command[3]), 0, command[1]))
        res = int(args[2])
        conn.commit()
    notify_insert(res)

def handle_update_holding(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('HOLDINGS_tapi.upd', (int(get_parameter(command,"-p")), int(get_parameter(command,"-q")),
                                                     int(command[1]), get_parameter(command,"-n")))
        res = int(args[2])
        conn.commit()
    notify_update(res)

def handle_delete_holding(command, cursor, connection):
    handle_delete(command, cursor, connection, 'HOLDINGS_tapi.del')

def handle_create_salary(command, cursor, connection):
    if len(command) >= 5:
        args = cursor.callproc('SALARIES_tapi.ins', (int(command[1]), int(command[3]), int(command[4]), int(command[2]), 0))
        res = int(args[4])
        conn.commit()
    notify_insert(res)

def handle_update_salary(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('SALARIES_tapi.upd', (int(get_parameter(command, "-i")), int(get_parameter(command, "-v")),
                                                     int(get_parameter(command, "-s")), int(get_parameter(command, "-c")), int(command[1])))
        res = int(args[4])
        conn.commit()
    notify_update(res)

def handle_delete_salary(command, cursor, connection):
    handle_delete(command, cursor, connection, 'SALARIES_tapi.del')

def handle_create_premium_size(command, cursor, connection):
    if len(command) >= 5:
        args = cursor.callproc('PREMIUMS_SIZES_tapi.ins', (int(command[2]), int(command[3]), " ".join(command[4:]), 0, command[1]))
        res = int(args[3])
        conn.commit()
    notify_insert(res)

def handle_update_premium_size(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('PREMIUMS_SIZES_tapi.upd', (int(get_parameter(command, "-min")), int(get_parameter(command, "-max")),
                                                           get_last_parameter(command, "-d"), command[1], get_parameter(command, "-n")))
        res = int(args[3])
        conn.commit()
    notify_update(res)

def handle_delete_premium_size(command, cursor, connection):
    handle_delete(command, cursor, connection, 'PREMIUMS_SIZES_tapi.del')

    #worker_id premium_id earning_date premium_size [note]

def handle_create_premium(command, cursor, connection):
    if len(command) == 5:
        args = cursor.callproc('PREMIUMS_tapi.ins', (int(command[2]),int(command[1]),get_date(command[3]),None,0,command[4]))
        res = int(args[4])
        conn.commit()
    elif len(command) >= 6:
        args = cursor.callproc('PREMIUMS_tapi.ins', (int(command[2]),int(command[1]),get_date(command[3])," ".join(command[5:]),0,command[4]))
        res = int(args[4])
        conn.commit()
    notify_insert(res)

def handle_update_premium(command, cursor, connection):
    if len(command) >= 2:
        args = cursor.callproc('PREMIUMS_tapi.upd', (int(get_parameter(command,"-p")),int(get_parameter(command,"-w")),
                                                     get_date(get_parameter(command,"-e")),get_last_parameter(command,"-d"),
                                                     command[1],get_parameter(command,"-s")))
        res = int(args[4])
        conn.commit()
    notify_update(res)

def handle_delete_premium(command, cursor, connection):
    handle_delete(command, cursor, connection, 'PREMIUMS_tapi.del')

#worker_id date_in_format_10.10.2010 state_id
def handle_create_worker_date_state(command, cursor, connection):
    if len(command) == 4:
        args = cursor.callproc('WORKERS_DATE_STATES_tapi.ins_ins', (int(command[1]),get_date(command[2]),int(command[3])))
        res = int(args[0])
        conn.commit()
    notify_insert(res)

def handle_delete_worker_date_state(command, cursor, connection):
    if len(command) == 3:
        args = cursor.callproc('WORKERS_DATE_STATES_tapi.del_del', (int(command[1]),get_date(command[2])))
        res = int(args[0])
        conn.commit()
    notify_delete(res)

#main

if __name__ == '__main__':
    result = establish_connection('127.0.0.1',1521,'orbis')
    cursor = result[0]
    
    conn = result[1]
    print(get_actual("workers_states","name","1"));
    print(cursor.execute("select name from workers_states where id = 1").fetchall()[0][0])
    for row in cursor:
        print(row)
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');
        print(get_parameter(command, "-i"))
        print('\n\nresult:\n\n');
        if command[0] == 'list':
            list_all_commands()
        elif command[0] == 'gs':
            handle_get_schedule(command, cursor)
        #worker_states
        elif command[0] == 'cws':
            handle_create_worker_state(command, cursor, conn)
        elif command[0] == 'dws':
            handle_delete_worker_state(command, cursor, conn)
        elif command[0] == 'uws':
            handle_update_worker_state(command, cursor, conn)
        #positions
        elif command[0] == 'cp':
            handle_create_position(command, cursor, conn)
        elif command[0] == 'dp':
            handle_delete_position(command, cursor, conn)
        elif command[0] == 'up':
            handle_update_position(command, cursor, conn)
        #contacts
        elif command[0] == 'cc':
            handle_create_contact(command, cursor, conn)
        elif command[0] == 'dc':
            handle_delete_contact(command, cursor, conn)
        elif command[0] == 'uc':
            handle_update_contact(command, cursor, conn)
        #services
        elif command[0] == 'cs':
            handle_create_service(command, cursor, conn)
        elif command[0] == 'us':
            handle_update_service(command, cursor, conn)
        elif command[0] == 'ds':
            handle_delete_service(command, cursor, conn)
        #holdings
        elif command[0] == 'ch':
            handle_create_holding(command, cursor, conn)
        elif command[0] == 'uh':
            handle_update_holding(command, cursor, conn)
        elif command[0] == 'dh':
            handle_delete_holding(command, cursor, conn)
        #salaries
        elif command[0] == 'csl':
            handle_create_salary(command, cursor, conn)
        elif command[0] == 'usl':
            handle_update_salary(command, cursor, conn)
        elif command[0] == 'dsl':
            handle_delete_salary(command, cursor, conn)
        #premiums_sizes
        elif command[0] == 'cps':
            handle_create_premium_size(command, cursor, conn)
        elif command[0] == 'ups':
            handle_update_premium_size(command, cursor, conn)
        elif command[0] == 'dps':
            handle_delete_premium_size(command, cursor, conn)
        #premiums
        elif command[0] == 'cpr':
            handle_create_premium(command, cursor, conn)
        elif command[0] == 'upr':
            handle_update_premium(command, cursor, conn)
        elif command[0] == 'dpr':
            handle_delete_premium(command, cursor, conn)
        #worker_date_states
        elif command[0] == 'cwds':
            handle_create_worker_date_state(command, cursor, conn)
        elif command[0] == 'dwds':
            handle_delete_worker_date_state(command, cursor, conn)
        elif command[0] == 'exit':
            break;
        
    
