import cx_Oracle
import configparser
import datetime

commands = (('get_schedule','master id, date of visit in format 10.10.2010'),
            ('get_schedule','master id'))

def establish_connection(ip, port, sid):
    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    db = cx_Oracle.connect(config['helios']['login'], config['helios']['password'], dsn_tns, encoding = "UTF-8")
    return db.cursor()

def list_all_commands():
    print('%-20s %-50s' % ('name','arguments'))
    for command in commands:
        print('%-20s %-50s' % command)

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


#main

if __name__ == '__main__':

    cursor = establish_connection('127.0.0.1',1521,'orbis')

    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');
        print('\n\nresult:\n\n');
        if command[0] == 'list':
            list_all_commands()
        elif command[0] == 'get_schedule':
            handle_get_schedule(command, cursor)
        elif command[0] == 'exit':
            break;
