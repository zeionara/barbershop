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
end WORKERS_DATE_STATES_tapi;
