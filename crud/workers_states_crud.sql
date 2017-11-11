create or replace package WORKERS_STATES_tapi
is

type WORKERS_STATES_tapi_rec is record (
DESCRIPTION  WORKERS_STATES.DESCRIPTION%type
,ID  WORKERS_STATES.ID%type
,NAME  WORKERS_STATES.NAME%type
);
type WORKERS_STATES_tapi_tab is table of WORKERS_STATES_tapi_rec;

-- insert
procedure ins (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_ID out WORKERS_STATES.ID%type
,p_NAME in WORKERS_STATES.NAME%type
);
-- update
procedure upd (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_ID in WORKERS_STATES.ID%type
,p_NAME in WORKERS_STATES.NAME%type
);
-- delete
procedure del (
p_ID in WORKERS_STATES.ID%type
);
end WORKERS_STATES_tapi;

/
create or replace package body WORKERS_STATES_tapi
is
-- insert
procedure ins (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_ID out WORKERS_STATES.ID%type
,p_NAME in WORKERS_STATES.NAME%type
) is
begin
insert into WORKERS_STATES(
DESCRIPTION
,NAME
) values (
p_DESCRIPTION
,p_NAME
)returning ID into p_ID;end;
-- update
procedure upd (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_ID in WORKERS_STATES.ID%type
,p_NAME in WORKERS_STATES.NAME%type
) is
begin
update WORKERS_STATES set
DESCRIPTION = p_DESCRIPTION
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in WORKERS_STATES.ID%type
) is
begin
delete from WORKERS_STATES
where ID = p_ID;
end;
end WORKERS_STATES_tapi;
