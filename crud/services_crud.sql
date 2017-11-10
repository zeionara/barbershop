 create or replace package SERVICES_tapi
is

type SERVICES_tapi_rec is record (
PRICE  SERVICES.PRICE%type
,DESCRIPTION  SERVICES.DESCRIPTION%type
,ID  SERVICES.ID%type
,AVG_DURATION  SERVICES.AVG_DURATION%type
,NAME  SERVICES.NAME%type
);
type SERVICES_tapi_tab is table of SERVICES_tapi_rec;

-- insert
procedure ins (
p_PRICE in SERVICES.PRICE%type
,p_DESCRIPTION in SERVICES.DESCRIPTION%type default null 
,p_ID out SERVICES.ID%type
,p_AVG_DURATION in SERVICES.AVG_DURATION%type default null 
,p_NAME in SERVICES.NAME%type
);
-- update
procedure upd (
p_PRICE in SERVICES.PRICE%type
,p_DESCRIPTION in SERVICES.DESCRIPTION%type default null 
,p_ID in SERVICES.ID%type
,p_AVG_DURATION in SERVICES.AVG_DURATION%type default null 
,p_NAME in SERVICES.NAME%type
);
-- delete
procedure del (
p_ID in SERVICES.ID%type
);
end SERVICES_tapi;

/
create or replace package body SERVICES_tapi
is
-- insert
procedure ins (
p_PRICE in SERVICES.PRICE%type
,p_DESCRIPTION in SERVICES.DESCRIPTION%type default null 
,p_ID out SERVICES.ID%type
,p_AVG_DURATION in SERVICES.AVG_DURATION%type default null 
,p_NAME in SERVICES.NAME%type
) is
begin
insert into SERVICES(
PRICE
,DESCRIPTION
,AVG_DURATION
,NAME
) values (
p_PRICE
,p_DESCRIPTION
,p_AVG_DURATION
,p_NAME
)returning ID into p_ID;
end;
-- update
procedure upd (
p_PRICE in SERVICES.PRICE%type
,p_DESCRIPTION in SERVICES.DESCRIPTION%type default null 
,p_ID in SERVICES.ID%type
,p_AVG_DURATION in SERVICES.AVG_DURATION%type default null 
,p_NAME in SERVICES.NAME%type
) is
begin
update SERVICES set
PRICE = p_PRICE
,DESCRIPTION = p_DESCRIPTION
,AVG_DURATION = p_AVG_DURATION
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in SERVICES.ID%type
) is
begin
delete from SERVICES
where ID = p_ID;
end;
end SERVICES_tapi;

 -------------------------------------
 declare
    insert_id  SERVICES.ID%TYPE;
begin
 SERVICES_TAPI.INS(
    P_PRICE => 500,
    P_DESCRIPTION => 'прическа с укладкой',
    P_ID => insert_id,
    P_AVG_DURATION => 40,
    P_NAME => 'прическа'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;
 
