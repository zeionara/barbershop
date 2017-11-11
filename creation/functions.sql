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
cnt int;
state_ int;
pattern_ varchar(100);
service_duration int;
intersection_degree int;
requested_date_time_end timestamp;
BEGIN
    --check if a master works in that day
    begin
        select state_code into state_ 
        from table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = master_id)
        where date_ = trunc(cast(requested_date_time_begin as date));
    exception
      WHEN NO_DATA_FOUND THEN
        state_ := null;
    END;
    if (state_ <> 1) and (state_ is not null) then
        return false;
    end if;
    --check if time can provide this service
    select count(*) into cnt
    from table(select rendered_services from qualifications where id = (select qualification from workers where id = master_id))
    where id = service_id;
    if (cnt = 0) then
        return false;
    end if;
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

CREATE OR REPLACE FUNCTION is_premium_valid(premium_size numeric, premium_id int) RETURN boolean is
cnt number;
min_p numeric;
max_p numeric;
BEGIN
    select min into min_p from premiums_sizes where id = premium_id;
    select max into max_p from premiums_sizes where id = premium_id;
    return (premium_size > min_p) and (premium_size < max_p);
END;

--check is the set of states contains duplicated date of incorrect ids of state
CREATE OR REPLACE FUNCTION is_states_valid(states day_states__) RETURN boolean is
cnt int;
day_state_table day_state_table__;
BEGIN
    day_state_table := states.day_state_table;
    for i in day_state_table.first .. day_state_table.last loop
        select count(*) into cnt from workers_states where id = day_state_table(i).state_code;
        if (cnt = 0) then
            return false;
        end if;
    end loop;
    for i in day_state_table.first .. day_state_table.last loop
        for j in day_state_table.first .. day_state_table.last loop
            if ((day_state_table(i).date_ = day_state_table(j).date_) and (i <> j)) then
                return false;
            end if;
        end loop;
    end loop;
    return true;
END;

---
---constructors
---

CREATE OR REPLACE FUNCTION new_day_state(date_ date, state_code int) RETURN day_state__ is
cnt int;
day_state_tmp day_state__;
BEGIN
    select count(*) into cnt from workers_states where id = state_code;
    if (cnt = 0) then
        raise_application_error(-20101, 'The state code is invalid');
        rollback;
    end if;
    day_state_tmp := day_state__(date_, state_code);
    return day_state_tmp;
END;

CREATE OR REPLACE FUNCTION new_holding(id_ int, quantity int) RETURN holding__ is
cnt int;
holding_tmp holding__;
BEGIN
    select count(*) into cnt from holdings where id = id_;
    if (cnt = 0) then
        raise_application_error(-20101, 'The holding id is invalid');
        rollback;
    end if;
    holding_tmp := holding__(id_, quantity);
    return holding_tmp;
END;

CREATE OR REPLACE FUNCTION new_service(id_ int) RETURN service__ is
cnt int;
service_tmp service__;
BEGIN
    select count(*) into cnt from services where id = id_;
    if (cnt = 0) then
        raise_application_error(-20101, 'The service id is invalid');
        rollback;
    end if;
    service_tmp := service__(id_);
    return service_tmp;
END;
