table = """create table qualifications(
    id int not null,
    name varchar(50) not null,
    description varchar(200),
    rendered_services services_table__
)nested table rendered_services store as nested_rendered_services;"""

upd = """create table requests(
    id int not null,
    visit_date_time timestamp not null,
    worker_id int not null,
    client_id int not null,
    service_id int not null,
    note varchar(100),
    factical_durability numeric,
    holdings holdings_table__
)nested table holdings store as nested_holdings;"""
upd_l = []
for st in str.split(upd,chr(10))[1:-1]:
    upd_l.append(str.lower(str.split(st," ")[0].replace(",","").replace("p_","")))

shorts = ["-i","-n","-s","-p","-sx","-a","-po","-q","-l","-ps"]
lengths = [10,15,20,20,3,30,20,15,20,20]
res = []
ind = 0
cmd_ind = 1
for st in str.split(table,chr(10))[1:-1]:
    arr = str.split(st.lstrip(), " ")
    nec = False
    if arr[1].find("int") != -1:
        typ = "int"
    elif arr[1].find("date") != -1:
        typ = "date"
    elif arr[1].find("char") != -1:
        typ = "str"
    else:
        continue
    name = str.split(st.lstrip(), " ")[0]
    cmd_order = 0
    print(arr)
    if name == "id":
        cmd_order = -2
    elif (len(arr) > 3) and (arr[3].find("null") != -1):
        print("%s not null!" % name)
        cmd_order = cmd_ind
        cmd_ind += 1
    else:
        cmd_order = -1
    res.append((name, shorts[ind], typ, lengths[ind], upd_l.index(name), cmd_order))
    ind += 1

print(res)
