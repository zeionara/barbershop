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