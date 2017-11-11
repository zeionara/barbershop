create or replace package PREMIUMS_SIZES_tapi
is

type PREMIUMS_SIZES_tapi_rec is record (
MIN  PREMIUMS_SIZES.MIN%type
,MAX  PREMIUMS_SIZES.MAX%type
,DESCRIPTION  PREMIUMS_SIZES.DESCRIPTION%type
,ID  PREMIUMS_SIZES.ID%type
,NAME  PREMIUMS_SIZES.NAME%type
);
type PREMIUMS_SIZES_tapi_tab is table of PREMIUMS_SIZES_tapi_rec;

-- insert
procedure ins (
p_MIN in PREMIUMS_SIZES.MIN%type
,p_MAX in PREMIUMS_SIZES.MAX%type
,p_DESCRIPTION in PREMIUMS_SIZES.DESCRIPTION%type default null 
,p_ID out PREMIUMS_SIZES.ID%type
,p_NAME in PREMIUMS_SIZES.NAME%type
);
-- update
procedure upd (
p_MIN in PREMIUMS_SIZES.MIN%type
,p_MAX in PREMIUMS_SIZES.MAX%type
,p_DESCRIPTION in PREMIUMS_SIZES.DESCRIPTION%type default null 
,p_ID in PREMIUMS_SIZES.ID%type
,p_NAME in PREMIUMS_SIZES.NAME%type
);
-- delete
procedure del (
p_ID in PREMIUMS_SIZES.ID%type
);
end PREMIUMS_SIZES_tapi;

/
create or replace package body PREMIUMS_SIZES_tapi
is
-- insert
procedure ins (
p_MIN in PREMIUMS_SIZES.MIN%type
,p_MAX in PREMIUMS_SIZES.MAX%type
,p_DESCRIPTION in PREMIUMS_SIZES.DESCRIPTION%type default null 
,p_ID out PREMIUMS_SIZES.ID%type
,p_NAME in PREMIUMS_SIZES.NAME%type
) is
begin
insert into PREMIUMS_SIZES(
MIN
,MAX
,DESCRIPTION
,NAME
) values (
p_MIN
,p_MAX
,p_DESCRIPTION
,p_NAME
)returning ID into p_ID;
end;
-- update
procedure upd (
p_MIN in PREMIUMS_SIZES.MIN%type
,p_MAX in PREMIUMS_SIZES.MAX%type
,p_DESCRIPTION in PREMIUMS_SIZES.DESCRIPTION%type default null 
,p_ID in PREMIUMS_SIZES.ID%type
,p_NAME in PREMIUMS_SIZES.NAME%type
) is
begin
update PREMIUMS_SIZES set
MIN = p_MIN
,MAX = p_MAX
,DESCRIPTION = p_DESCRIPTION
,NAME = p_NAME
where ID = p_ID;
end;
-- del
procedure del (
p_ID in PREMIUMS_SIZES.ID%type
) is
begin
delete from PREMIUMS_SIZES
where ID = p_ID;
end;
end PREMIUMS_SIZES_tapi;
---------------------------------------------

declare
    insert_id PREMIUMS_SIZES.ID%TYPE;
begin
  PREMIUMS_SIZES_TAPI.INS(
    P_MIN => 100000,
    P_MAX => 150000,
    P_DESCRIPTION => 'за перевыполнения плана',
    P_ID => insert_id,
    P_NAME => 'премия 1'
  );

    dbms_output.put_line('Generated id: ' || insert_id);

end;