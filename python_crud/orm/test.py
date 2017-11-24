from pony.orm import *
import configparser
import cx_Oracle
import pickle

db = Database()
class service_table__(object):
    def __init__(self, states_list):
        self.states_list = states_list

class service__(object):
    def __init__(self, id):
        self.id = id

def notify(operation, ident):
    print("%s item with id %i" % (operation, ident))

def notify_insert(ident):
    notify("Inserted",ident)

def notify_delete(ident):
    notify("Deleted",ident)

def notify_update(ident):
    notify("Updated",ident)

def get_parameter(command, code):
    try:
        return command[command.index(code) + 1]
    except ValueError:
        return None

def list_all_commands():
    print('%-20s %-10s %-50s' % ('name','short name','arguments'))
    for command in commands:
        print('%-20s %-10s %-50s' % command[:3])

def get_services_list(services_str):
    services = []
    for service_code in services_str.split(','):
        services.append(service__(int(service_code)))
    return services


class ss():
    id = 0

class Positions(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)

class Qualifications(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    rendered_services = Optional(str, sql_type = "services_table__")

    
def establish_connection(ip, port, sid):

    config = configparser.ConfigParser()
    config.read('C://Users//Zerbs//accounts.sec')

    dsn_tns = cx_Oracle.makedsn(ip, port, sid)

    dbs = db.bind(provider="oracle", user=config['helios']['login'], password=config['helios']['password'],
                  dsn=dsn_tns, encoding = "UTF-8")
    x = "1"
    db.generate_mapping(create_tables=True)

    #print(dir(cx_Oracle.Object))

    return (dbs, db)
        
def handle_create_qualification(command, cursor, conn):
    if (len(command) == 2):
        with db_session:
            qualification = Qualifications(name=command[1])
    elif (len(command) == 3):
        with db_session:
            qualification = Qualifications(name=command[1], rendered_services=service_table__(get_services_list(command[2])))
    notify_insert(qualification.id)

def handle_update_qualification(command, cursor, conn):
    if (len(command) == 2):
        with db_session:
            qualification = Qualifications(name=command[1])
    notify_insert(qualification.id)

def handle_delete_qualification(command, cursor, conn):
    if (len(command) == 2):
        with db_session:
            qualification = Qualifications(name=command[1])
    notify_insert(qualification.id)

def get_handler(typed_command):
    for command in commands:
        if (typed_command == command[0]) or (typed_command == command[1]):
            return command[3]

commands = (('create_qualification','cql','name [rendered_services_in_format_1,2,3,4] [description]', handle_create_qualification),
            ('update_qualification','uql','id [-n name] [-s rendered_services_in_format_1,2,3,4] [-d description]', handle_update_qualification),
            ('delete_qualification','dql','id', handle_delete_qualification))

if __name__ == '__main__':
    result = establish_connection('127.0.0.1',1521,'orbis')
    cursor = result[0]
    conn = result[1]
    print(get_services_list("1,22,22,33"))
    with db_session:
        print(db.select("select * from qualifications"))
        #position1 = Positions(id=12, name="pony",description="My little pony")
        
        print(Qualifications.get(name="цирюльникс").rendered_services.aslist()[0].ID)
        #print(pickle.dumps(service_table__(get_services_list("1,2"))))
        vk = Qualifications.get(name="цирюльник").rendered_services
        #qualification = Qualifications(name = "cow", rendered_services = vk)
    
    while(True):
        command = input('\nType a command (\'list\' to get available commands or \'exit\' to exit): \n\n').split(' ');
        
        if command[0] == 'list':
            list_all_commands()
        elif command[0] == 'exit':
            break;
        else:
            print('\n\nresult:\n\n');
            get_handler(command[0])(command, cursor, conn)



