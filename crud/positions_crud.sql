create or replace package POSITIONS_tapi
is

type POSITIONS_tapi_rec is record (
DESCRIPTION  POSITIONS.DESCRIPTION%type
,ID  POSITIONS.ID%type
,NAME  POSITIONS.NAME%type
);
type POSITIONS_tapi_tab is table of POSITIONS_tapi_rec;

-- insert
procedure ins (
p_DESCRIPTION in POSITIONS.DESCRIPTION%type default null 
,p_ID out POSITIONS.ID%type
,p_NAME in POSITIONS.NAME%type
);
-- update
procedure upd (
p_DESCRIPTION in POSITIONS.DESCRIPTION%type default null 
,p_ID in POSITIONS.ID%type
,p_NAME in POSITIONS.NAME%type
);
-- delete
procedure del (
p_ID in POSITIONS.ID%type
);
end POSITIONS_tapi;

/
create or replace package body POSITIONS_tapi
is
-- insert
procedure ins (
p_DESCRIPTION in POSITIONS.DESCRIPTION%type default null 
,p_ID out POSITIONS.ID%type
,p_NAME in POSITIONS.NAME%type
) is
begin
insert into POSITIONS(
DESCRIPTION
,NAME
) values (
p_DESCRIPTION
,p_NAME
)returning ID into p_ID;end;
-- update
procedure upd (
p_DESCRIPTION in POSITIONS.DESCRIPTION%type default null 
,p_ID in POSITIONS.ID%type
,p_NAME in POSITIONS.NAME%type
) is
begin
update POSITIONS set
DESCRIPTION = p_DESCRIPTION
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in POSITIONS.ID%type
) is
begin
delete from POSITIONS
where ID = p_ID;
end;
end POSITIONS_tapi;
-------------------------------------------
/
 declare
    insert_id  POSITIONS.ID%TYPE;
begin
    POSITIONS_TAPI.INS(
    P_DESCRIPTION => 'no description',
    P_ID => insert_id,
    P_NAME => 'парикмахер'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;
