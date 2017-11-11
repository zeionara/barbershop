import cx_Oracle

ip = '127.0.0.1'
port = 1521
SID = 'orbis'
dsn_tns = cx_Oracle.makedsn(ip, port, SID)

db = cx_Oracle.connect('lorem', 'ipsum', dsn_tns, encoding = "UTF-8")
cursor = db.cursor()
cursor.execute('select tpg.calc_smth(10) from dual')
#print(cursor)
print(cursor.description)
#print(db.encoding)
for row in cursor:
    print(row)

command = input('Type a command: ').split(' ');
print(command)
if command[0] == 'calc':
    cursor.execute('select tpg.calc_smth(%s) from dual' % command[1])
    print(cursor.description)
    #print(db.encoding)
    for row in cursor:
        print(row)
