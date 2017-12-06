declare 
 data day_state_table__ := day_state_table__(day_state__(TO_DATE('2003/07/09', 'yyyy/mm/dd'), 1)); 
 begin 
 update WORKERS_DATE_STATES 
 set states = day_states__(data)
 where id = 1; 
end;

select treat(states as day_states__).day_state_table from workers_date_states where worker_id = 2

insert into table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = 1) values (TO_DATE('2003/07/10', 'yyyy/mm/dd'), 1);




create or replace package nest_day_states_tapi
is
-- insert
procedure ins (workers_date_state_id WORKERS_DATE_STATES.ID%type, dateForState VARCHAR, newState int);

--delete
procedure del (workers_date_state_id WORKERS_DATE_STATES.ID%type, dateFordeDelete VARCHAR);

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

-- insert
procedure ins (workers_date_state_id WORKERS_DATE_STATES.ID%type, dateForState VARCHAR, newState int) is
begin
  insert into table(select treat(states as day_states__).day_state_table 
  from workers_date_states where id = workers_date_state_id) 
  values (TO_DATE(dateForState, 'yyyy/mm/dd'), newState);
end;


--delete
procedure del (workers_date_state_id WORKERS_DATE_STATES.ID%type, dateFordeDelete VARCHAR) is
begin
  delete from table(select treat(states as day_states__).day_state_table 
							from workers_date_states 
								where id = workers_date_state_id) 
  WHERE DATE_ = TO_DATE(dateFordeDelete, 'yyyy/mm/dd');
end;

end nest_day_states_tapi;

/

--USAGE
--insert 
DECLARE
  WORKERS_DATE_STATE_ID NUMBER;
  DATEFORSTATE VARCHAR2(200);
  NEWSTATE NUMBER;
BEGIN
  WORKERS_DATE_STATE_ID := 1;
  DATEFORSTATE := '2004/07/10';
  NEWSTATE := 1;

  NEST_DAY_STATES_TAPI.INS(
    WORKERS_DATE_STATE_ID => WORKERS_DATE_STATE_ID,
    DATEFORSTATE => DATEFORSTATE,
    NEWSTATE => NEWSTATE
  );
END;

--delete
 DECLARE
  WORKERS_DATE_STATE_ID NUMBER;
  DATEFORDEDELETE VARCHAR2(200);
BEGIN
  WORKERS_DATE_STATE_ID := 1;
  DATEFORDEDELETE := '2004/07/10';

  NEST_DAY_STATES_TAPI.DEL(
    WORKERS_DATE_STATE_ID => WORKERS_DATE_STATE_ID,
    DATEFORDEDELETE => DATEFORDEDELETE
  );
END;

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
