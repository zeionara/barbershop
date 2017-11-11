create or replace package ACCOUNTS_tapi
is

type ACCOUNTS_tapi_rec is record (
PASSWD  ACCOUNTS.PASSWD%type
,PERSON_STATUS  ACCOUNTS.PERSON_STATUS%type
,PERSON_ID  ACCOUNTS.PERSON_ID%type
,LOGIN  ACCOUNTS.LOGIN%type
,ID  ACCOUNTS.ID%type
,AVATAR  ACCOUNTS.AVATAR%type
);
type ACCOUNTS_tapi_tab is table of ACCOUNTS_tapi_rec;

-- insert
procedure ins (
p_PASSWD in ACCOUNTS.PASSWD%type
,p_PERSON_STATUS in ACCOUNTS.PERSON_STATUS%type
,p_PERSON_ID in ACCOUNTS.PERSON_ID%type
,p_LOGIN in ACCOUNTS.LOGIN%type
,p_ID out ACCOUNTS.ID%type
,p_AVATAR in ACCOUNTS.AVATAR%type default null 
);
-- update
procedure upd (
p_PASSWD in ACCOUNTS.PASSWD%type
,p_PERSON_STATUS in ACCOUNTS.PERSON_STATUS%type
,p_PERSON_ID in ACCOUNTS.PERSON_ID%type
,p_LOGIN in ACCOUNTS.LOGIN%type
,p_ID in ACCOUNTS.ID%type
,p_AVATAR in ACCOUNTS.AVATAR%type default null 
);
-- delete
procedure del (
p_ID in ACCOUNTS.ID%type
);
end ACCOUNTS_tapi;

/
create or replace package body ACCOUNTS_tapi
is
-- insert
procedure ins (
p_PASSWD in ACCOUNTS.PASSWD%type
,p_PERSON_STATUS in ACCOUNTS.PERSON_STATUS%type
,p_PERSON_ID in ACCOUNTS.PERSON_ID%type
,p_LOGIN in ACCOUNTS.LOGIN%type
,p_ID out ACCOUNTS.ID%type
,p_AVATAR in ACCOUNTS.AVATAR%type default null 
) is
begin
insert into ACCOUNTS(
PASSWD
,PERSON_STATUS
,PERSON_ID
,LOGIN
,AVATAR
) values (
p_PASSWD
,p_PERSON_STATUS
,p_PERSON_ID
,p_LOGIN
,p_AVATAR
) returning ID into p_ID;
end;
-- update
procedure upd (
p_PASSWD in ACCOUNTS.PASSWD%type
,p_PERSON_STATUS in ACCOUNTS.PERSON_STATUS%type
,p_PERSON_ID in ACCOUNTS.PERSON_ID%type
,p_LOGIN in ACCOUNTS.LOGIN%type
,p_ID in ACCOUNTS.ID%type
,p_AVATAR in ACCOUNTS.AVATAR%type default null 
) is
begin
update ACCOUNTS set
PASSWD = p_PASSWD
,PERSON_STATUS = p_PERSON_STATUS
,PERSON_ID = p_PERSON_ID
,LOGIN = p_LOGIN
,AVATAR = p_AVATAR
where ID = p_ID;
end;
-- del
procedure del (
p_ID in ACCOUNTS.ID%type
) is
begin
delete from ACCOUNTS
where ID = p_ID;
end;
end ACCOUNTS_tapi;
----------------------

declare
    insert_id ACCOUNTS.ID%TYPE;
begin
    ACCOUNTS_TAPI.INS(
    P_PASSWD => 'qwerty',
    P_PERSON_STATUS => 'client',
    P_PERSON_ID => 1,
    P_LOGIN => 'cli1',
    P_ID => insert_id,
    P_AVATAR => null
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;

