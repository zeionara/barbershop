

CREATE or replace PACKAGE barbershop AS
   function get_clients_list(master_id int, date_ date) return clients_table__;
END barbershop;
/

CREATE or replace PACKAGE BODY barbershop AS
   FUNCTION get_clients_list(master_id int, date_ date) return clients_table__ IS
   clients clients_table__;
   cc client__;
   cnt int;
   cursor clients_ is select name, patronymic, contact, cast(visit_date_time as date) vdate from (requests r join clients c on r.client_id = c.id) join 
        (
            select * from contacts where id in 
            (
                select min(id) from contacts group by person_id, person_status
            ) 
            and person_status = 'client' and type = 'phone'
        ) 
        on person_id = client_id
        where trunc(cast(visit_date_time as date)) = date_ and worker_id = master_id
        order by visit_date_time;
   BEGIN
        cnt := 0;
        clients := clients_table__(null);
        --clients.extend(100);
        delete from opop;
        FOR client_ IN clients_ LOOP
            cc := client__(client_.name, client_.patronymic, client_.contact, client_.vdate);
            clients.extend();
            clients(clients.count) := cc;
            --cnt := cnt + 1;
            
            insert into opop values(client__(client_.name, client_.patronymic, client_.contact, client_.vdate));
            dbms_output.put_line('---' || client_.name);
        END LOOP;
        return clients;
   END;
END barbershop;
/
select min(id) from contacts group by person_id, person_status;
select * from contacts where id in (select min(id) from contacts group by person_id) and person_status = 'client' and type = 'phone';
select * from contacts where id in (select min(id) from contacts group by person_id);

--to_char(visit_date_time,'HH24:MI')

create table opop of client__;
drop table opop;
select * from opop;
set serveroutput on;
declare
vv boolean;
clients clients_table__;
begin
    --clients := clients_table__(null);
    --clients.extend(100);
    --declare local temporary table opop of client__;
    --delete from opop;
    --insert into opop values (client__('a', 'a', 'a', TO_DATE('2002/11/10', 'yyyy/mm/dd')));
    clients := barbershop.get_clients_list(2, TO_DATE('2002/11/10', 'yyyy/mm/dd'));
    dbms_output.put_line('hio');
end;
select * from opop;