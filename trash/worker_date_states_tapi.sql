create or replace package worker_date_states_tapi
is

type num_arr IS TABLE OF NUMBER INDEX BY PLS_INTEGER;

type date_arr IS TABLE OF DATE INDEX BY PLS_INTEGER;

procedure ins (
ids in num_arr,
dates in date_arr,
iid in number
);

procedure get(
ids out num_arr,
dates out date_arr,
iid in number
);

end worker_date_states_tapi;
/
create or replace package body worker_date_states_tapi
is
-- insert
procedure ins (
ids in num_arr,
dates in date_arr,
iid in number
) is
ds day_states__;
begin
    ds := day_states__(day_state_table__());
    for i in ids.first .. ids.last loop
        dbms_output.put_line('ok');
        ds.day_state_table.extend;
        ds.day_state_table(ds.day_state_table.count) := new_day_state(dates(i), ids(i));
    end loop;
    update workers_date_states set states = ds where id = iid;
    dbms_output.put_line('ok');
end;

procedure get (
ids out num_arr,
dates out date_arr,
iid in number
) is
ds day_states__;
begin
    --parr := num_arr();
    ds := day_states__(day_state_table__());
    select states into ds from workers_date_states where id = iid;
    if ds is not null then
        for i in ds.day_state_table.first .. ds.day_state_table.last loop
            dbms_output.put_line('ok');
            --parr.extend;
            ids(i) := ds.day_state_table(i).state_code;
            dates(i) := ds.day_state_table(i).date_;
        end loop;
    end if;
    dbms_output.put_line('ok');
end;

end worker_date_states_tapi;
/