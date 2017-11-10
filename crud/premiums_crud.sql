create or replace package PREMIUMS_tapi
is

type PREMIUMS_tapi_rec is record (
PREMIUM_ID  PREMIUMS.PREMIUM_ID%type
,WORKER_ID  PREMIUMS.WORKER_ID%type
,EARNING_DATE  PREMIUMS.EARNING_DATE%type
,NOTE  PREMIUMS.NOTE%type
,ID  PREMIUMS.ID%type
,PREMIUM_SIZE  PREMIUMS.PREMIUM_SIZE%type
);
type PREMIUMS_tapi_tab is table of PREMIUMS_tapi_rec;

-- insert
procedure ins (
p_PREMIUM_ID in PREMIUMS.PREMIUM_ID%type
,p_WORKER_ID in PREMIUMS.WORKER_ID%type
,p_EARNING_DATE in PREMIUMS.EARNING_DATE%type
,p_NOTE in PREMIUMS.NOTE%type default null 
,p_ID out PREMIUMS.ID%type
,p_PREMIUM_SIZE in PREMIUMS.PREMIUM_SIZE%type
);
-- update
procedure upd (
p_PREMIUM_ID in PREMIUMS.PREMIUM_ID%type
,p_WORKER_ID in PREMIUMS.WORKER_ID%type
,p_EARNING_DATE in PREMIUMS.EARNING_DATE%type
,p_NOTE in PREMIUMS.NOTE%type default null 
,p_ID in PREMIUMS.ID%type
,p_PREMIUM_SIZE in PREMIUMS.PREMIUM_SIZE%type
);
-- delete
procedure del (
p_ID in PREMIUMS.ID%type
);
end PREMIUMS_tapi;

/
create or replace package body PREMIUMS_tapi
is
-- insert
procedure ins (
p_PREMIUM_ID in PREMIUMS.PREMIUM_ID%type
,p_WORKER_ID in PREMIUMS.WORKER_ID%type
,p_EARNING_DATE in PREMIUMS.EARNING_DATE%type
,p_NOTE in PREMIUMS.NOTE%type default null 
,p_ID out PREMIUMS.ID%type
,p_PREMIUM_SIZE in PREMIUMS.PREMIUM_SIZE%type
) is
begin
insert into PREMIUMS(
PREMIUM_ID
,WORKER_ID
,EARNING_DATE
,NOTE
,PREMIUM_SIZE
) values (
p_PREMIUM_ID
,p_WORKER_ID
,p_EARNING_DATE
,p_NOTE
,p_PREMIUM_SIZE
)returning ID into p_ID;end;
-- update
procedure upd (
p_PREMIUM_ID in PREMIUMS.PREMIUM_ID%type
,p_WORKER_ID in PREMIUMS.WORKER_ID%type
,p_EARNING_DATE in PREMIUMS.EARNING_DATE%type
,p_NOTE in PREMIUMS.NOTE%type default null 
,p_ID in PREMIUMS.ID%type
,p_PREMIUM_SIZE in PREMIUMS.PREMIUM_SIZE%type
) is
begin
update PREMIUMS set
PREMIUM_ID = p_PREMIUM_ID
,WORKER_ID = p_WORKER_ID
,EARNING_DATE = p_EARNING_DATE
,NOTE = p_NOTE
,PREMIUM_SIZE = p_PREMIUM_SIZE
where ID = p_ID;
end;
-- del
procedure del (
p_ID in PREMIUMS.ID%type
) is
begin
delete from PREMIUMS
where ID = p_ID;
end;
end PREMIUMS_tapi;
--------------------------------------

declare
    insert_id PREMIUMS.ID%TYPE;
begin
   PREMIUMS_TAPI.INS(
    P_PREMIUM_ID => 1,
    P_WORKER_ID => 1,
    P_EARNING_DATE => to_date('10-02-02','DD-MM-RR'),
    P_NOTE => "",
    P_ID => insert_id,
    P_PREMIUM_SIZE => 120000
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;
