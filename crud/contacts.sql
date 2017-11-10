create or replace package CONTACTS_tapi
is

type CONTACTS_tapi_rec is record (
CONTACT  CONTACTS.CONTACT%type
,PERSON_STATUS  CONTACTS.PERSON_STATUS%type
,PERSON_ID  CONTACTS.PERSON_ID%type
,ID  CONTACTS.ID%type
,TYPE  CONTACTS.TYPE%type
);
type CONTACTS_tapi_tab is table of CONTACTS_tapi_rec;

-- insert
procedure ins (
p_CONTACT in CONTACTS.CONTACT%type
,p_PERSON_STATUS in CONTACTS.PERSON_STATUS%type
,p_PERSON_ID in CONTACTS.PERSON_ID%type
,p_ID out CONTACTS.ID%type
,p_TYPE in CONTACTS.TYPE%type
);
-- update
procedure upd (
p_CONTACT in CONTACTS.CONTACT%type
,p_PERSON_STATUS in CONTACTS.PERSON_STATUS%type
,p_PERSON_ID in CONTACTS.PERSON_ID%type
,p_ID in CONTACTS.ID%type
,p_TYPE in CONTACTS.TYPE%type
);
-- delete
procedure del (
p_ID in CONTACTS.ID%type
);
end CONTACTS_tapi;

/
create or replace package body CONTACTS_tapi
is
-- insert
procedure ins (
p_CONTACT in CONTACTS.CONTACT%type
,p_PERSON_STATUS in CONTACTS.PERSON_STATUS%type
,p_PERSON_ID in CONTACTS.PERSON_ID%type
,p_ID out CONTACTS.ID%type
,p_TYPE in CONTACTS.TYPE%type
) is
begin
insert into CONTACTS(
CONTACT
,PERSON_STATUS
,PERSON_ID
,TYPE
) values (
p_CONTACT
,p_PERSON_STATUS
,p_PERSON_ID
,p_TYPE
)returning ID into p_ID;
end;
-- update
procedure upd (
p_CONTACT in CONTACTS.CONTACT%type
,p_PERSON_STATUS in CONTACTS.PERSON_STATUS%type
,p_PERSON_ID in CONTACTS.PERSON_ID%type
,p_ID in CONTACTS.ID%type
,p_TYPE in CONTACTS.TYPE%type
) is
begin
update CONTACTS set
CONTACT = p_CONTACT
,PERSON_STATUS = p_PERSON_STATUS
,PERSON_ID = p_PERSON_ID
,TYPE = p_TYPE
where ID = p_ID;
end;
-- del
procedure del (
p_ID in CONTACTS.ID%type
) is
begin
delete from CONTACTS
where ID = p_ID;
end;
end CONTACTS_tapi;

---------------------------------

declare
    insert_id CONTACTS.ID%TYPE;
begin
 CONTACTS_TAPI.INS(
    P_CONTACT => '89811633903',
    P_PERSON_STATUS => 'client',
    P_PERSON_ID => 1,
    P_ID => insert_id,
    P_TYPE => 'phone'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;

