create or replace package WORKERS_DATE_STATES_tapi
is

type WORKERS_DATE_STATES_tapi_rec is record (
WORKER_ID  WORKERS_DATE_STATES.WORKER_ID%type
,STATES  WORKERS_DATE_STATES.STATES%type
,ID  WORKERS_DATE_STATES.ID%type
);
type WORKERS_DATE_STATES_tapi_tab is table of WORKERS_DATE_STATES_tapi_rec;

-- insert
procedure ins (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_STATES in WORKERS_DATE_STATES.STATES%type default null 
,p_ID out WORKERS_DATE_STATES.ID%type
);
--
procedure ins_ins (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_DATE in NESTED_STATES.DATE_%type
,p_STATE_CODE in NESTED_STATES.STATE_CODE%type
);
-- update
procedure upd (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_STATES in WORKERS_DATE_STATES.STATES%type default null 
,p_ID in WORKERS_DATE_STATES.ID%type
);
-- delete
procedure del (
p_ID in WORKERS_DATE_STATES.ID%type
);
--
procedure del_del (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_DATE in NESTED_STATES.DATE_%type
);
end WORKERS_DATE_STATES_tapi;

/
create or replace package body WORKERS_DATE_STATES_tapi
is
-- insert
procedure ins (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_STATES in WORKERS_DATE_STATES.STATES%type default null 
,p_ID out WORKERS_DATE_STATES.ID%type
) is
begin
insert into WORKERS_DATE_STATES(
WORKER_ID
,STATES
) values (
p_WORKER_ID
,p_STATES
)returning ID into p_ID;end;
--
procedure ins_ins (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_DATE in NESTED_STATES.DATE_%type
,p_STATE_CODE in NESTED_STATES.STATE_CODE%type
) is
begin
insert into table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = p_WORKER_ID) (DATE_, STATE_CODE) 
values (p_DATE, p_STATE_CODE);
end;
-- update
procedure upd (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_STATES in WORKERS_DATE_STATES.STATES%type default null 
,p_ID in WORKERS_DATE_STATES.ID%type
) is
begin
update WORKERS_DATE_STATES set
WORKER_ID = p_WORKER_ID
,STATES = p_STATES
where ID = p_ID;
end;
-- del
procedure del (
p_ID in WORKERS_DATE_STATES.ID%type
) is
begin
delete from WORKERS_DATE_STATES
where ID = p_ID;
end;
--
procedure del_del (
p_WORKER_ID in WORKERS_DATE_STATES.WORKER_ID%type
,p_DATE in NESTED_STATES.DATE_%type
) is
begin
delete from table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = p_WORKER_ID)
where DATE_ = p_DATE;
end;
end WORKERS_DATE_STATES_tapi;
