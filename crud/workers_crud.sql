create or replace package WORKERS_tapi
is

type WORKERS_tapi_rec is record (
POSITION  WORKERS.POSITION%type
,SURNAME  WORKERS.SURNAME%type
,QUALIFICATION  WORKERS.QUALIFICATION%type
,PATRONYMIC  WORKERS.PATRONYMIC%type
,SEX  WORKERS.SEX%type
,ADDRESS  WORKERS.ADDRESS%type
,ID  WORKERS.ID%type
,NAME  WORKERS.NAME%type
);
type WORKERS_tapi_tab is table of WORKERS_tapi_rec;

-- insert
procedure ins (
p_POSITION in WORKERS.POSITION%type
,p_SURNAME in WORKERS.SURNAME%type
,p_QUALIFICATION in WORKERS.QUALIFICATION%type
,p_PATRONYMIC in WORKERS.PATRONYMIC%type default null 
,p_SEX in WORKERS.SEX%type
,p_ADDRESS in WORKERS.ADDRESS%type
,p_ID out WORKERS.ID%type
,p_NAME in WORKERS.NAME%type
,p_contact in CONTACTS.CONTACT%type
);
-- update
procedure upd (
p_POSITION in WORKERS.POSITION%type
,p_SURNAME in WORKERS.SURNAME%type
,p_QUALIFICATION in WORKERS.QUALIFICATION%type
,p_PATRONYMIC in WORKERS.PATRONYMIC%type default null 
,p_SEX in WORKERS.SEX%type
,p_ADDRESS in WORKERS.ADDRESS%type
,p_ID in WORKERS.ID%type
,p_NAME in WORKERS.NAME%type
);
-- delete
procedure del (
p_ID in WORKERS.ID%type
);
end WORKERS_tapi;

/
create or replace package body WORKERS_tapi
is
-- insert
procedure ins (
p_POSITION in WORKERS.POSITION%type
,p_SURNAME in WORKERS.SURNAME%type
,p_QUALIFICATION in WORKERS.QUALIFICATION%type
,p_PATRONYMIC in WORKERS.PATRONYMIC%type default null 
,p_SEX in WORKERS.SEX%type
,p_ADDRESS in WORKERS.ADDRESS%type
,p_ID out WORKERS.ID%type
,p_NAME in WORKERS.NAME%type
,p_contact in CONTACTS.CONTACT%type
) is
begin
insert into WORKERS(
POSITION
,SURNAME
,QUALIFICATION
,PATRONYMIC
,SEX
,ADDRESS
,NAME
) values (
p_POSITION
,p_SURNAME
,p_QUALIFICATION
,p_PATRONYMIC
,p_SEX
,p_ADDRESS
,p_NAME
)returning ID into p_ID;
insert into contacts(person_id, person_status, type, contact) values (p_ID,'worker','phone',p_contact);
end;
-- update
procedure upd (
p_POSITION in WORKERS.POSITION%type
,p_SURNAME in WORKERS.SURNAME%type
,p_QUALIFICATION in WORKERS.QUALIFICATION%type
,p_PATRONYMIC in WORKERS.PATRONYMIC%type default null 
,p_SEX in WORKERS.SEX%type
,p_ADDRESS in WORKERS.ADDRESS%type
,p_ID in WORKERS.ID%type
,p_NAME in WORKERS.NAME%type
) is
begin
update WORKERS set
POSITION = p_POSITION
,SURNAME = p_SURNAME
,QUALIFICATION = p_QUALIFICATION
,PATRONYMIC = p_PATRONYMIC
,SEX = p_SEX
,ADDRESS = p_ADDRESS
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in WORKERS.ID%type
) is
begin
delete from WORKERS
where ID = p_ID;
end;
end WORKERS_tapi;

-------------------------------------------
declare
    insert_id WORKERS.ID%TYPE;
begin
WORKERS_TAPI.INS(
    P_POSITION => 1,
    P_SURNAME => 'Оксанов',
    P_QUALIFICATION => 1,
    P_PATRONYMIC => 'Эдуардович',
    P_SEX => 'm',
    P_ADDRESS => 'Невский 67/1',
    P_ID => insert_id,
    P_NAME => 'Роман',
	p_contact => '+7 (909) 101-11-62'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;

