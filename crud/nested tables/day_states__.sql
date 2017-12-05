declare 
 data day_state_table__ := day_state_table__(day_state__(TO_DATE('2003/07/09', 'yyyy/mm/dd'), 1)); 
 begin 
 update WORKERS_DATE_STATES 
 set states = day_states__(data)
 where id = 1; 
end;

create or replace package nest_day_states_tapi
is

--update
procedure upd(workers_date_state_id WORKERS_DATE_STATES.ID%type, dateForState VARCHAR, newState int);

end nest_day_states_tapi;

/


create or replace package body nest_day_states_tapi
is

--update
procedure upd(workers_date_state_id WORKERS_DATE_STATES.ID%type, dateForState VARCHAR, newState int) is 
begin
update WORKERS_DATE_STATES 
 set states = day_states__(day_state_table__(day_state__(TO_DATE(dateForState, 'yyyy/mm/dd'), newState)))
 where id = workers_date_state_id;
end;

end nest_day_states_tapi;

/

--USAGE 
--update 
DECLARE
  WORKERS_DATE_STATE_ID NUMBER;
  DATEFORSTATE VARCHAR2(200);
  NEWSTATE NUMBER;
BEGIN
  WORKERS_DATE_STATE_ID := 1;
  DATEFORSTATE := '2003/07/09';
  NEWSTATE := 1;

  NEST_DAY_STATES_TAPI.UPD(
    WORKERS_DATE_STATE_ID => WORKERS_DATE_STATE_ID,
    DATEFORSTATE => DATEFORSTATE,
    NEWSTATE => NEWSTATE
  );
END;
