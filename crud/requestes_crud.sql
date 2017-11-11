create or replace package REQUESTS_tapi
is

type REQUESTS_tapi_rec is record (
WORKER_ID  REQUESTS.WORKER_ID%type
,HOLDINGS  REQUESTS.HOLDINGS%type
,VISIT_DATE_TIME  REQUESTS.VISIT_DATE_TIME%type
,CLIENT_ID  REQUESTS.CLIENT_ID%type
,NOTE  REQUESTS.NOTE%type
,SERVICE_ID  REQUESTS.SERVICE_ID%type
,ID  REQUESTS.ID%type
,FACTICAL_DURABILITY  REQUESTS.FACTICAL_DURABILITY%type
);
type REQUESTS_tapi_tab is table of REQUESTS_tapi_rec;

-- insert
procedure ins (
p_WORKER_ID in REQUESTS.WORKER_ID%type
,p_HOLDINGS in REQUESTS.HOLDINGS%type default null 
,p_VISIT_DATE_TIME in REQUESTS.VISIT_DATE_TIME%type
,p_CLIENT_ID in REQUESTS.CLIENT_ID%type
,p_NOTE in REQUESTS.NOTE%type default null 
,p_SERVICE_ID in REQUESTS.SERVICE_ID%type
,p_ID out REQUESTS.ID%type
,p_FACTICAL_DURABILITY in REQUESTS.FACTICAL_DURABILITY%type default null 
);
-- update
procedure upd (
p_WORKER_ID in REQUESTS.WORKER_ID%type
,p_HOLDINGS in REQUESTS.HOLDINGS%type default null 
,p_VISIT_DATE_TIME in REQUESTS.VISIT_DATE_TIME%type
,p_CLIENT_ID in REQUESTS.CLIENT_ID%type
,p_NOTE in REQUESTS.NOTE%type default null 
,p_SERVICE_ID in REQUESTS.SERVICE_ID%type
,p_ID in REQUESTS.ID%type
,p_FACTICAL_DURABILITY in REQUESTS.FACTICAL_DURABILITY%type default null 
);
-- delete
procedure del (
p_ID in REQUESTS.ID%type
);
end REQUESTS_tapi;

/
create or replace package body REQUESTS_tapi
is
-- insert
procedure ins (
p_WORKER_ID in REQUESTS.WORKER_ID%type
,p_HOLDINGS in REQUESTS.HOLDINGS%type default null 
,p_VISIT_DATE_TIME in REQUESTS.VISIT_DATE_TIME%type
,p_CLIENT_ID in REQUESTS.CLIENT_ID%type
,p_NOTE in REQUESTS.NOTE%type default null 
,p_SERVICE_ID in REQUESTS.SERVICE_ID%type
,p_ID out REQUESTS.ID%type
,p_FACTICAL_DURABILITY in REQUESTS.FACTICAL_DURABILITY%type default null 
) is
begin
insert into REQUESTS(
WORKER_ID
,HOLDINGS
,VISIT_DATE_TIME
,CLIENT_ID
,NOTE
,SERVICE_ID
,FACTICAL_DURABILITY
) values (
p_WORKER_ID
,p_HOLDINGS
,p_VISIT_DATE_TIME
,p_CLIENT_ID
,p_NOTE
,p_SERVICE_ID
,p_FACTICAL_DURABILITY
)returning ID into p_ID;
end;
-- update
procedure upd (
p_WORKER_ID in REQUESTS.WORKER_ID%type
,p_HOLDINGS in REQUESTS.HOLDINGS%type default null 
,p_VISIT_DATE_TIME in REQUESTS.VISIT_DATE_TIME%type
,p_CLIENT_ID in REQUESTS.CLIENT_ID%type
,p_NOTE in REQUESTS.NOTE%type default null 
,p_SERVICE_ID in REQUESTS.SERVICE_ID%type
,p_ID in REQUESTS.ID%type
,p_FACTICAL_DURABILITY in REQUESTS.FACTICAL_DURABILITY%type default null 
) is
begin
update REQUESTS set
WORKER_ID = p_WORKER_ID
,HOLDINGS = p_HOLDINGS
,VISIT_DATE_TIME = p_VISIT_DATE_TIME
,CLIENT_ID = p_CLIENT_ID
,NOTE = p_NOTE
,SERVICE_ID = p_SERVICE_ID
,FACTICAL_DURABILITY = p_FACTICAL_DURABILITY
where ID = p_ID;
end;
-- del
procedure del (
p_ID in REQUESTS.ID%type
) is
begin
delete from REQUESTS
where ID = p_ID;
end;
end REQUESTS_tapi;

--------------------------
/
 declare
    insert_id  REQUESTS.ID%TYPE;
begin
  REQUESTS_TAPI.INS(
    P_WORKER_ID => 1,
    P_HOLDINGS => 1,
    P_VISIT_DATE_TIME => to_date('10-02-02','DD-MM-RR'),
    P_CLIENT_ID => 1,
    P_NOTE => 'note',
    P_SERVICE_ID => 1,
    P_ID => insert_id,
    P_FACTICAL_DURABILITY => 30
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;