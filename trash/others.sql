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
select * from clients;
insert into workers (name, surname, sex, address, position, qualification) 
values ('Суини','Тодд','m','Флит-стрит 13 корпус 6 квартира 666','Демон-парикмахер','цирюльник');
insert into contacts (person_id, person_status, type, contact) values (2,'client','phone','+7 (911) 934-33-63');
select * from contacts;
select * from services;
insert into services (name, price) values ('Бритье налысо с',100);
insert into services (name, price) values ('Хипстерская стрижка',300);
insert into requests (visit_date_time, worker_id, client_id, service_id) 
values (to_timestamp ('10-11-02 16:10', 'DD-MM-RR HH24:MI'), 2, 2, 2);
select * from requests;
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

insert into workers_date_states (worker_id, states) values (2, day_states__(day_state_table__(new_day_state(TO_DATE('2003/07/09', 'yyyy/mm/dd'), 1),
                                                 new_day_state(TO_DATE('2003/07/10', 'yyyy/mm/dd'), 2))));
select * from workers_date_states;
--select from inner table

insert into table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = 2) (DATE_, STATE_CODE) 
values (TO_DATE('2004/07/10', 'yyyy/mm/dd'), 1);
select person_id, person_status, type, contact from contacts where id = 5;
select * from table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = 2);
--insert to inner table
delete from workers_date_states;
select * from services;
select table_name, nested from all_tables where nested like 'YES';
select * from services;
commit();
insert into qualifications (name, rendered_services) values ('цирюльникс',services_table__(new_service(22)));
select * from nested_rendered_services;
select * from table(select rendered_services from qualifications where id = (select qualification from workers where id = 2));

select id, person_id, person_status, login, passwd, dbms_lob.getlength(avatar) size_of_avatar_in_bytes from accounts;