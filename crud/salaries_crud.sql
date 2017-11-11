create or replace package SALARIES_tapi
is

type SALARIES_tapi_rec is record (
WORKER_ID  SALARIES.WORKER_ID%type
,VACATION  SALARIES.VACATION%type
,SICK  SALARIES.SICK%type
,COMMON  SALARIES.COMMON%type
,ID  SALARIES.ID%type
);
type SALARIES_tapi_tab is table of SALARIES_tapi_rec;

-- insert
procedure ins (
p_WORKER_ID in SALARIES.WORKER_ID%type
,p_VACATION in SALARIES.VACATION%type
,p_SICK in SALARIES.SICK%type
,p_COMMON in SALARIES.COMMON%type
,p_ID out SALARIES.ID%type
);
-- update
procedure upd (
p_WORKER_ID in SALARIES.WORKER_ID%type
,p_VACATION in SALARIES.VACATION%type
,p_SICK in SALARIES.SICK%type
,p_COMMON in SALARIES.COMMON%type
,p_ID in SALARIES.ID%type
);
-- delete
procedure del (
p_ID in SALARIES.ID%type
);
end SALARIES_tapi;

/
create or replace package body SALARIES_tapi
is
-- insert
procedure ins (
p_WORKER_ID in SALARIES.WORKER_ID%type
,p_VACATION in SALARIES.VACATION%type
,p_SICK in SALARIES.SICK%type
,p_COMMON in SALARIES.COMMON%type
,p_ID out SALARIES.ID%type
) is
begin
insert into SALARIES(
WORKER_ID
,VACATION
,SICK
,COMMON
) values (
p_WORKER_ID
,p_VACATION
,p_SICK
,p_COMMON
)returning ID into p_ID;end;
-- update
procedure upd (
p_WORKER_ID in SALARIES.WORKER_ID%type
,p_VACATION in SALARIES.VACATION%type
,p_SICK in SALARIES.SICK%type
,p_COMMON in SALARIES.COMMON%type
,p_ID in SALARIES.ID%type
) is
begin
update SALARIES set
WORKER_ID = p_WORKER_ID
,VACATION = p_VACATION
,SICK = p_SICK
,COMMON = p_COMMON
where ID = p_ID;
end;
-- del
procedure del (
p_ID in SALARIES.ID%type
) is
begin
delete from SALARIES
where ID = p_ID;
end;
end SALARIES_tapi;
