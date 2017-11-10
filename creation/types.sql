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