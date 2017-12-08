create or replace package NESTED_STATES_tapi
is

--type NESTED_STATES_tapi_rec is record (
--PRICE  HOLDINGS.PRICE%type
--,QUANTITY  HOLDINGS.QUANTITY%type
--,ID  HOLDINGS.ID%type
--,NAME  HOLDINGS.NAME%type
--);
--type HOLDINGS_tapi_tab is table of HOLDINGS_tapi_rec;
--
procedure ins (
master_id in int,
p_date_ in date,
p_state_code in int
);
---- update
--procedure upd (
--p_PRICE in HOLDINGS.PRICE%type
--,p_QUANTITY in HOLDINGS.QUANTITY%type
--,p_ID in HOLDINGS.ID%type
--,p_NAME in HOLDINGS.NAME%type
--);
-- delete
procedure del (
master_id in int,
p_date_ in date
);
end NESTED_STATES_tapi;

/
create or replace package body NESTED_STATES_tapi
is
-- insert
procedure ins (
master_id in int,
p_date_ in date,
p_state_code in int
) is
begin
insert into table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = master_id)(
DATE_
,STATE_CODE
) values (
p_date_
,p_state_code
);
end;
---- update
--procedure upd (
--p_PRICE in HOLDINGS.PRICE%type
--,p_QUANTITY in HOLDINGS.QUANTITY%type
--,p_ID in HOLDINGS.ID%type
--,p_NAME in HOLDINGS.NAME%type
--) is
--begin
--update HOLDINGS set
--PRICE = p_PRICE
--,QUANTITY = p_QUANTITY
--,NAME = p_NAME
--where ID = p_ID;
--end;
-- del
procedure del (
master_id in int,
p_date_ in date
) is
begin
delete from table(select treat(states as day_states__).day_state_table from workers_date_states where worker_id = master_id)
where DATE_ = p_date_;
end;
end NESTED_STATES_tapi;
-----------------------
/

-- declare
--    insert_id  HOLDINGS.ID%TYPE;
--begin
--	HOLDINGS_TAPI.INS(
--    P_PRICE => 30,
--    P_QUANTITY => 3,
--    P_ID => insert_id,
--    P_NAME => 'заколка'
--  );
--
--    dbms_output.put_line('Generated id: ' || insert_id);
--
--end;

---



-- declare
--    insert_id  HOLDINGS.ID%TYPE;
--begin
--	HOLDINGS_TAPI.INS(
--    P_PRICE => 30,
--    P_QUANTITY => 3,
--    P_ID => insert_id,
--    P_NAME => 'заколка'
--  );
--
--    dbms_output.put_line('Generated id: ' || insert_id);
--
--end;