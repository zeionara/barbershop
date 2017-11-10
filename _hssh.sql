--
--functions
--

CREATE OR REPLACE FUNCTION is_person_id_valid(person_status varchar, person_id_ int) RETURN boolean is
cnt number;
BEGIN
    if person_status = 'worker' then select count(*) into cnt from contacts where person_id_ in (select id from workers);
    else select count(*) into cnt from contacts where person_id_ in (select id from clients);
    end if;
    return cnt > 0;
END;

CREATE OR REPLACE FUNCTION is_contact_valid(contact_type varchar, contact_value varchar) RETURN boolean is
pattern_ varchar(100);
BEGIN
    if contact_type = 'phone' then pattern_ := '(\+7|8) (\()([0-9]){3}(\)) ([0-9]){3}-([0-9]){2}-([0-9]){2}';
    elsif contact_type = 'e-mail' then pattern_ := '[0-9a-zA-Z_.]*@[0-9a-zA-Z]*\.[0-9a-zA-Z_]{2,}';
    elsif contact_type = 'vk' then pattern_ := '[a-zA-Z_]{5,}';
    end if;
    return regexp_like(contact_value,pattern_);
END;

CREATE OR REPLACE FUNCTION is_master_unbusy(requested_date_time_begin timestamp, service_id int, master_id int) RETURN boolean is
pattern_ varchar(100);
service_duration int;
intersection_degree int;
requested_date_time_end timestamp;
BEGIN
    --get time of end serving
    select avg_duration into service_duration from services where id = service_id;
    if service_duration is null then service_duration := 60;
    end if;
    requested_date_time_end := requested_date_time_begin + service_duration/1440;
    --check if a master is available in that time
    select count(*) into intersection_degree from requests rs
    where worker_id = master_id and
    (
        (
            visit_date_time between (requested_date_time_begin - 1/144) and (requested_date_time_end + 1/144)
        ) or
        (
            visit_date_time + 
            (
                case (select avg_duration from services where id = rs.service_id)
                when null then 60
                else (select avg_duration from services where id = rs.service_id) end
            ) between (requested_date_time_begin - 1/144) and (requested_date_time_end + 1/144)
        ) or
        (
            requested_date_time_begin between (visit_date_time - 1/144) and 
            (
                visit_date_time + 
                (
                    case (select avg_duration from services where id = rs.service_id)
                    when null then 60
                    else (select avg_duration from services where id = rs.service_id) end
                ) + 1/144
            )
        ) or
        (
            requested_date_time_end between (visit_date_time - 1/144) and 
            (
                visit_date_time + 
                (
                    case (select avg_duration from services where id = rs.service_id)
                    when null then 60
                    else (select avg_duration from services where id = rs.service_id) end
                ) + 1/144
            )
        )
    );
    return intersection_degree = 0;
END;
/*
insert into requests (visit_date_time, worker_id, client_id, service_id) 
values (to_timestamp ('10-11-02 13:30', 'DD-MM-RR HH24:MI'), 2, 1, 2);

declare
vv boolean;
begin
    vv := is_master_unbusy(to_timestamp ('10-11-02 13:30', 'DD-MM-RR HH24:MI'), 2, 2);
    if vv then dbms_output.put_line('Master is unbusy:');
    end if;
end;

select * from requests;
*/

CREATE OR REPLACE FUNCTION is_premium_valid(premium_size numeric, premium_id int) RETURN boolean is
cnt number;
min_p numeric;
max_p numeric;
BEGIN
    select min into min_p from premiums_sizes where id = premium_id;
    select max into max_p from premiums_sizes where id = premium_id;
    return (premium_size > min_p) and (premium_size < max_p);
END;

--
--triggers and sequences
--

create sequence clients_id_seq START WITH 1;

create or replace trigger clients_id_bir 
before insert on clients 
for each row
begin
  select clients_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence workers_id_seq START WITH 1;

create or replace trigger workers_id_bir 
before insert on workers 
for each row
begin
  select workers_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence clients_id_seq START WITH 1;

create or replace trigger clients_id_bir 
before insert on clients 
for each row
begin
  select clients_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence contacts_id_seq START WITH 1;

create or replace trigger contacts_id_bir 
before insert on contacts 
for each row
begin
  select contacts_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence services_id_seq START WITH 1;

create or replace trigger services_id_bir 
before insert on services 
for each row
begin
  select services_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence requests_id_seq START WITH 1;

create or replace trigger requests_id_bir 
before insert on requests 
for each row
begin
  select requests_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence holdings_id_seq START WITH 1;

create or replace trigger holdings_id_bir 
before insert on holdings 
for each row
begin
  select holdings_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence salaries_id_seq START WITH 1;

create or replace trigger salaries_id_bir 
before insert on salaries 
for each row
begin
  select salaries_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence premiums_sizes_id_seq START WITH 1;

create or replace trigger premiums_sizes_id_bir 
before insert on premiums_sizes 
for each row
begin
  select premiums_sizes_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence premiums_id_seq START WITH 1;

create or replace trigger premiums_id_bir 
before insert on premiums 
for each row
begin
  select premiums_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence workers_statuses_id_seq START WITH 1;

create or replace trigger workers_statuses_id_bir 
before insert on workers_statuses 
for each row
begin
  select workers_statuses_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence accounts_id_seq START WITH 1;

create or replace trigger accounts_id_bir 
before insert on accounts 
for each row
begin
  select accounts_id_seq.nextval
  into   :new.id
  from   dual;
end;

CREATE OR REPLACE TRIGGER contacts_before_insert
BEFORE INSERT
   ON contacts
   FOR EACH ROW
BEGIN
    --checking person id
    if (not is_person_id_valid(:new.person_status,:new.person_id)) then 
    begin
        RAISE_APPLICATION_ERROR(-20101, 'There is no such ' || :new.person_status);
        ROLLBACK;
    end;
    end if;
    
    --checking content of contact
    if (not is_contact_valid(:new.type,:new.contact)) then 
    begin
        RAISE_APPLICATION_ERROR(-20101, 'It is invalid ' || :new.type);
        ROLLBACK;
    end;
    end if;
    
END;

create or replace trigger accounts_before_insert
before insert
   on accounts
   for each row
begin
    if (not is_person_id_valid(:new.person_status,:new.person_id)) then 
    begin
        raise_application_error(-20101, 'There is no such ' || :new.person_status);
        rollback;
    end;
    end if;
end;

create or replace trigger requests_before_insert
before insert
   on requests
   for each row
begin
    if (not is_master_unbusy(:new.visit_date_time,:new.service_id,:new.worker_id)) then 
    begin
        raise_application_error(-20101, 'The master is busy at that time');
        rollback;
    end;
    end if;
end;

create or replace trigger premiums_before_insert
before insert
   on premiums
   for each row
begin
    if (not is_premium_valid(:new.premium_size,:new.premium_id)) then 
    begin
        raise_application_error(-20101, 'The premium is appointed unfairly');
        rollback;
    end;
    end if;
end;

--
--tables
--

create table clients( 
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,

    constraint clients_pk primary key (id)
);

create table workers(
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,
    position varchar(20) not null,
    qualification varchar(20) not null,

    constraint workers_pk primary key (id)
);

create table contacts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    type varchar(10) not null check(type in ('phone','e-mail','vk')),
    contact varchar(20) not null,

    constraint contacts_pk primary key (id),
    constraint person_id_clients_workers_fk check(is_person_id_valid(person_status));
);

create table services(
    id int not null,
    name varchar(20) not null,
    price numeric not null,
    description varchar(100),
    avg_duration int,
    
    constraint services_pk primary key (id)
);
--alter table services add avg_duration int;

create table requests(
    id int not null,
    visit_date_time timestamp not null,
    worker_id int not null,
    client_id int not null,
    service_id int not null,
    note varchar(100),
    factical_durability numeric,
    
    constraint requests_pk primary key (id),
    constraint requests_workers_fk foreign key(worker_id) references workers(id),
    constraint requests_clients_fk foreign key(client_id) references clients(id),
    constraint requests_services_fk foreign key(service_id) references services(id)
);

create table holdings(
    id int not null,
    name varchar(100) not null,
    price numeric not null,
    quantity numeric not null,
    
    constraint holdings_pk primary key (id)
);

create table salaries(
    id int not null,
    worker_id int not null,
    common numeric not null,
    vacation numeric not null,
    sick numeric not null,
    
    constraint salaries_pk primary key(id),
    constraint salaries_workers_fk foreign key(worker_id) references workers(id),
    constraint salaries_workers_unique unique(worker_id)
);

create table premiums_sizes(
    id int not null,
    name varchar(20) not null,
    min numeric not null,
    max numeric not null,
    description varchar(200),
    
    constraint premiums_sizes_pk primary key(id)
);

create table premiums(
    id int not null,
    premium_id int not null,
    worker_id int not null,
    earning_date date not null,
    premium_size numeric not null,
    note varchar(150),
    
    constraint premiums_pk primary key(id),
    constraint premiums_workers_fk foreign key(worker_id) references workers(id),
    constraint premiums_premiums_sizes_fk foreign key(premium_id) references premiums_sizes(id)
);

create table accounts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    login varchar(20) not null,
    passwd varchar(20) not null,
    avatar blob,
    
    constraint accounts_pk primary key(id)
);
    

create table workers_statuses(
    id int not null,
    name varchar(20) not null,
    description varchar(100),
    
    constraint workers_statuses_pk primary key(id)
);

--
--types
--

create or replace type worker_status_type as object(
    the_date date,
    status_code int
);

create or replace type worker_status_varray_type as varray(365) of worker_status_type;

create or replace type worker_status_collection as object(
    worker_status_varray worker_status_varray_type,
    member function get_status(ide numeric) return int
);

create or replace type body worker_status_collection as
    member function get_status(ide numeric) return int is
    begin
        dbms_output.put_line('searching...');
        for s in 1..self.worker_status_varray.count loop
            dbms_output.put_line(s || '--');
        end loop;
    end;
end;

set serveroutput on;
declare
    worker_stats worker_status_collection;
begin
    worker_stats := worker_status_collection(worker_status_varray_type(worker_status_type(to_date('10-02-02','DD-MM-RR'),1)));
    worker_status_collection.get_status(12);
end;
/

worker_status_type(to_date('10-02-02','DD-MM-RR'), 2);

select user from dual;
create directory image_dir as '/home/s207602/himgs';

--
--others
--

insert into workers_statuses (name) values ('базовый');
insert into workers_statuses (name) values ('больничный');
insert into workers_statuses (name) values ('отпуск');
select * from workers_statuses;

select * from premiums_sizes;

set serveroutput on;
insert into contacts (person_id, person_status, type, contact) values (1,'client','phone','+7 (973) 122-3304');
select * from workers;

insert into premiums (premium_id, worker_id, earning_date, premium_size)
values(1, 2, to_date('10-03-02','DD-MM-RR'), 1000);
select * from premiums;
drop table premiums_sizes;
drop table holdings;
insert into clients (name, surname, patronymic, sex, address) values ('Александр','Александров','Александрович','m','Альпийский пер. 15/2 комната 1306');
insert into workers (name, surname, sex, address, position, qualification) 
values ('Суини','Тодд','m','Флит-стрит 13 корпус 6 квартира 666','Демон-парикмахер','цирюльник');
insert into contacts (person_id, person_status, type, contact) values (1,'client','vk','do_odd');
insert into services (name, price) values ('Бритье налысо',100);
insert into services (name, price) values ('Хипстерская стрижка',300);
insert into requests (visit_date_time, worker_id, client_id, service_id) 
values (to_timestamp ('10-11-02 14:10', 'DD-MM-RR HH24:MI'), 2, 1, 2);
insert into holdings (name, price, quantity) values ('Refectocil краска д.бровей и ресниц св.-коричневaя №3.1 15мл', 331, 10);
drop table requests;
insert into premiums_sizes (name, min, max) values ('За хороший отзыв', 500, 2000);
select * from premiums_sizes;
insert into salaries (worker_id, common, vacation, sick) values (2, 6666.66, 6666.66, 6666.66);

select * from workers;
select surname, c.name, patronymic, s.name, visit_date_time 
from (requests r join clients c on r.client_id = c.id) join services s on s.id = r.service_id;

SELECT TO_TIMESTAMP ('10-09-02 14:10:10.123000', 'DD-MM-RR HH24:MI:SS.FF')
   FROM DUAL;

drop table clients;
select * from clients;
select * from workers;