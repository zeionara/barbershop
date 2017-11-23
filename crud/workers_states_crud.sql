create or replace package WORKERS_STATES_tapi
as

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
--
function ins_f (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_NAME in WORKERS_STATES.NAME%type
) return WORKERS_STATES.ID%type;
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
end;

/
create or replace package body WORKERS_STATES_tapi
as
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
-----
function ins_f (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_NAME in WORKERS_STATES.NAME%type
) return WORKERS_STATES.ID%type is
ide WORKERS_STATES.ID%type;
begin
WORKERS_STATES_TAPI.ins(p_DESCRIPTION, ide, p_NAME);
return ide;
end;
-- update
procedure upd (
p_DESCRIPTION in WORKERS_STATES.DESCRIPTION%type default null 
,p_ID in WORKERS_STATES.ID%type
,p_NAME in WORKERS_STATES.NAME%type
) is
begin
if p_DESCRIPTION is null then
update WORKERS_STATES set
NAME = p_NAME
where ID = p_ID;
else if p_NAME is null then
update WORKERS_STATES set
DESCRIPTION = p_DESCRIPTION
where ID = p_ID;
else
update WORKERS_STATES set
DESCRIPTION = p_DESCRIPTION
,NAME = p_NAME
where ID = p_ID;
end if;
end;
-- del
procedure del (
p_ID in WORKERS_STATES.ID%type
) is
begin
delete from WORKERS_STATES
where ID = p_ID;
end;
end;
