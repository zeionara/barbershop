create or replace package QUALIFICATIONS_tapi
is

type QUALIFICATIONS_tapi_rec is record (
RENDERED_SERVICES  QUALIFICATIONS.RENDERED_SERVICES%type
,DESCRIPTION  QUALIFICATIONS.DESCRIPTION%type
,ID  QUALIFICATIONS.ID%type
,NAME  QUALIFICATIONS.NAME%type
);
type QUALIFICATIONS_tapi_tab is table of QUALIFICATIONS_tapi_rec;

-- insert
procedure ins (
p_RENDERED_SERVICES in QUALIFICATIONS.RENDERED_SERVICES%type default null 
,p_DESCRIPTION in QUALIFICATIONS.DESCRIPTION%type default null 
,p_ID out QUALIFICATIONS.ID%type
,p_NAME in QUALIFICATIONS.NAME%type
);
-- update
procedure upd (
p_RENDERED_SERVICES in QUALIFICATIONS.RENDERED_SERVICES%type default null 
,p_DESCRIPTION in QUALIFICATIONS.DESCRIPTION%type default null 
,p_ID in QUALIFICATIONS.ID%type
,p_NAME in QUALIFICATIONS.NAME%type
);
-- delete
procedure del (
p_ID in QUALIFICATIONS.ID%type
);
end QUALIFICATIONS_tapi;

/
create or replace package body QUALIFICATIONS_tapi
is
-- insert
procedure ins (
p_RENDERED_SERVICES in QUALIFICATIONS.RENDERED_SERVICES%type default null 
,p_DESCRIPTION in QUALIFICATIONS.DESCRIPTION%type default null 
,p_ID out QUALIFICATIONS.ID%type
,p_NAME in QUALIFICATIONS.NAME%type
) is
begin
insert into QUALIFICATIONS(
RENDERED_SERVICES
,DESCRIPTION
,NAME
) values (
p_RENDERED_SERVICES
,p_DESCRIPTION
,p_NAME
) returning ID into p_ID;
end;
-- update
procedure upd (
p_RENDERED_SERVICES in QUALIFICATIONS.RENDERED_SERVICES%type default null 
,p_DESCRIPTION in QUALIFICATIONS.DESCRIPTION%type default null 
,p_ID in QUALIFICATIONS.ID%type
,p_NAME in QUALIFICATIONS.NAME%type
) is
begin
update QUALIFICATIONS set
RENDERED_SERVICES = p_RENDERED_SERVICES
,DESCRIPTION = p_DESCRIPTION
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in QUALIFICATIONS.ID%type
) is
begin
delete from QUALIFICATIONS
where ID = p_ID;
end;
end QUALIFICATIONS_tapi;


--------------------------------------------------------------
declare
    insert_id QUALIFICATIONS.ID%TYPE;
begin
 QUALIFICATIONS_TAPI.INS(
    P_RENDERED_SERVICES => null,
    P_DESCRIPTION => '',
    P_ID => insert_id,
    P_NAME => 'Алекс'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;