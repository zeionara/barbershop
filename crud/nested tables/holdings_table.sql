--необходимо проинициализировать поле holdings как таблицу HOLDINGS_TABLE__()
declare 
 data holdings_table__ := holdings_table__(holding__(1,3)); 
 begin 
 update requests 
 set holdings = data 
 where id = 1; 
end; 
--(https://asktom.oracle.com/pls/apex/asktom.search?tag=nested-table-20010812) 

/
create or replace package nest_holdings_tapi
is

-- insert
procedure ins (request_id REQUESTS.ID%type,  holdings_id HOLDINGS.ID%type, holdings_quantity HOLDINGS.QUANTITY%type);
--delete
procedure del (request_id REQUESTS.ID%type,  holdings_id HOLDINGS.ID%type);
--update
procedure upd(request_id REQUESTS.ID%type, old_holdings_id HOLDINGS.ID%type, new_holdings_id HOLDINGS.ID%type, new_holdings_quantity HOLDINGS.QUANTITY%type);

end nest_holdings_tapi;

/
create or replace package body nest_holdings_tapi
is
-- insert
procedure ins (request_id REQUESTS.ID%type, holdings_id HOLDINGS.ID%type, holdings_quantity HOLDINGS.QUANTITY%type) is
begin
  insert into table(select holdings from requests where id = request_id) values(holding__(holdings_id,holdings_quantity));
end;

--delete
procedure del (request_id REQUESTS.ID%type, holdings_id HOLDINGS.ID%type) is
begin
  delete from table(select holdings from requests where id = request_id) where id = holdings_id;
end;

--update
procedure upd(request_id REQUESTS.ID%type, old_holdings_id HOLDINGS.ID%type, new_holdings_id HOLDINGS.ID%type, new_holdings_quantity HOLDINGS.QUANTITY%type) is 
begin
	update table(select holdings from requests where id = request_id) 
	set id =  new_holdings_id, quantity =  new_holdings_quantity
	where id = old_holdings_id; 
end;

end nest_holdings_tapi;
/

------------
update table(select RENDERED_SERVICES from QUALIFICATIONS where id = qualification_id) set id = new_service_id where id = old_service_id;
------------

--usage
--insert
DECLARE
  REQUEST_ID NUMBER;
  HOLDINGS_ID NUMBER;
  HOLDINGS_QUANTITY NUMBER;
BEGIN
  REQUEST_ID := 1;
  HOLDINGS_ID := 1;
  HOLDINGS_QUANTITY := 3;

  NEST_HOLDINGS_TAPI.INS(
    REQUEST_ID => REQUEST_ID,
    HOLDINGS_ID => HOLDINGS_ID,
    HOLDINGS_QUANTITY => HOLDINGS_QUANTITY
  );
END;
--delete
DECLARE
  REQUEST_ID NUMBER;
  HOLDINGS_ID NUMBER;
BEGIN
  REQUEST_ID := 1;
  HOLDINGS_ID := 1;

  NEST_HOLDINGS_TAPI.DEL(
    REQUEST_ID => REQUEST_ID,
    HOLDINGS_ID => HOLDINGS_ID
  );
END;
--update
DECLARE
  REQUEST_ID NUMBER;
  OLD_HOLDINGS_ID NUMBER;
  NEW_HOLDINGS_ID NUMBER;
  NEW_HOLDINGS_QUANTITY NUMBER;
BEGIN
  REQUEST_ID := 1;
  OLD_HOLDINGS_ID := 7;
  NEW_HOLDINGS_ID := 10;
  NEW_HOLDINGS_QUANTITY := 100;

  NEST_HOLDINGS_TAPI.UPD(
    REQUEST_ID => REQUEST_ID,
    OLD_HOLDINGS_ID => OLD_HOLDINGS_ID,
    NEW_HOLDINGS_ID => NEW_HOLDINGS_ID,
    NEW_HOLDINGS_QUANTITY => NEW_HOLDINGS_QUANTITY
  );
--rollback; 
END;




