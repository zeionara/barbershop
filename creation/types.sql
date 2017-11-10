create or replace type day_state__ as object (
    date_ date,
    state_code int
);

create or replace type day_state_table__ as table of day_state__;

create or replace type day_states__ as object (
    day_state_table day_state_table__,
    member function get_state(required_date date) return int
);

create or replace type body day_states__ as 
    member function get_state(required_date date) return int is 
    state_ int;
    begin 
        for i in day_state_table.first .. day_state_table.last loop
            if (day_state_table(i).date_ = required_date) then
                state_ := day_state_table(i).state_code;
                exit;
            end if;
        end loop;
        if state_ is null then state_ := 0;
        end if;
        return state_; 
    end get_state; 
end;

create or replace type holding__ as object (
    id int,
    quantity int
);

create or replace type holdings_table__ as table of holding__;

create or replace type service__ as object (
    id int
);

create or replace type services_table__ as table of service__;

/*create or replace type worker_status_type as object(
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
*/