create or replace package HOLDINGS_tapi
is

type HOLDINGS_tapi_rec is record (
PRICE  HOLDINGS.PRICE%type
,QUANTITY  HOLDINGS.QUANTITY%type
,ID  HOLDINGS.ID%type
,NAME  HOLDINGS.NAME%type
);
type HOLDINGS_tapi_tab is table of HOLDINGS_tapi_rec;

-- insert
procedure ins (
p_PRICE in HOLDINGS.PRICE%type
,p_QUANTITY in HOLDINGS.QUANTITY%type
,p_ID out HOLDINGS.ID%type
,p_NAME in HOLDINGS.NAME%type
);
-- update
procedure upd (
p_PRICE in HOLDINGS.PRICE%type
,p_QUANTITY in HOLDINGS.QUANTITY%type
,p_ID in HOLDINGS.ID%type
,p_NAME in HOLDINGS.NAME%type
);
-- delete
procedure del (
p_ID in HOLDINGS.ID%type
);
end HOLDINGS_tapi;

/
create or replace package body HOLDINGS_tapi
is
-- insert
procedure ins (
p_PRICE in HOLDINGS.PRICE%type
,p_QUANTITY in HOLDINGS.QUANTITY%type
,p_ID out HOLDINGS.ID%type
,p_NAME in HOLDINGS.NAME%type
) is
begin
insert into HOLDINGS(
PRICE
,QUANTITY
,NAME
) values (
p_PRICE
,p_QUANTITY
,p_NAME
)returning ID into p_ID;
end;
-- update
procedure upd (
p_PRICE in HOLDINGS.PRICE%type
,p_QUANTITY in HOLDINGS.QUANTITY%type
,p_ID in HOLDINGS.ID%type
,p_NAME in HOLDINGS.NAME%type
) is
begin
update HOLDINGS set
PRICE = p_PRICE
,QUANTITY = p_QUANTITY
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in HOLDINGS.ID%type
) is
begin
delete from HOLDINGS
where ID = p_ID;
end;
end HOLDINGS_tapi;
-----------------------
/

 declare
    insert_id  HOLDINGS.ID%TYPE;
begin
	HOLDINGS_TAPI.INS(
    P_PRICE => 30,
    P_QUANTITY => 3,
    P_ID => insert_id,
    P_NAME => 'заколка'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;
