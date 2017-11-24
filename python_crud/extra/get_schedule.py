import datetime

def execute(command, cursor, connection):
    if len(command) == 3:
        cursor.execute("select * from table(select barbershop.get_clients_list_as_strings(%s, TO_DATE('%s', 'dd.mm.yyyy')) from dual)" % (command[1], command[2]))
    else:
        now = datetime.datetime.now()
        cursor.execute("select * from table(select barbershop.get_clients_list_as_strings(%s, TO_DATE('%s', 'dd.mm.yyyy')) from dual)"
                       % (command[1], (str(now.day)+'.'+str(now.month)+'.'+str(now.year))))
    print("%-10s %-20s %-20s %-20s" % ('имя','отчество','телефон','время записи'));
    for row in cursor:
        print("%-10s %-20s %-20s %-20s" % row);
