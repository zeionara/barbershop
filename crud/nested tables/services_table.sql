create or replace package nest_ren_services_tapi
is

-- insert
procedure ins (qualification_id QUALIFICATIONS.ID%type,  service_id SERVICES.ID%type);
--delete
procedure del (qualification_id QUALIFICATIONS.ID%type,  service_id SERVICES.ID%type);
--update
procedure upd(qualification_id QUALIFICATIONS.ID%type,  old_service_id SERVICES.ID%type, new_service_id SERVICES.ID%type);

end nest_ren_services_tapi;

/
create or replace package body nest_ren_services_tapi
is
-- insert
procedure ins (qualification_id QUALIFICATIONS.ID%type, service_id SERVICES.ID%type) is
begin
 insert into table(select RENDERED_SERVICES from QUALIFICATIONS where id = qualification_id) values(service_id);
end;

--delete
procedure del (qualification_id QUALIFICATIONS.ID%type, service_id SERVICES.ID%type) is
begin
 delete from table(select RENDERED_SERVICES from QUALIFICATIONS where id = qualification_id) where id = service_id;
end;

--update
procedure upd(qualification_id QUALIFICATIONS.ID%type,  old_service_id SERVICES.ID%type, new_service_id SERVICES.ID%type) is 
begin
 update table(select RENDERED_SERVICES from QUALIFICATIONS where id = qualification_id) set id = new_service_id where id = old_service_id;
end;
 
end nest_ren_services_tapi;


--usage
--ins
 DECLARE
  QUALIFICATION_ID NUMBER;
  SERVICE_ID NUMBER;
BEGIN
  QUALIFICATION_ID := 2;
  SERVICE_ID := 22;

  NEST_REN_SERVICES_TAPI.INS(
    QUALIFICATION_ID => QUALIFICATION_ID,
    SERVICE_ID => SERVICE_ID
  );
END;
--del
DECLARE
  QUALIFICATION_ID NUMBER;
  SERVICE_ID NUMBER;
BEGIN
  QUALIFICATION_ID := 2;
  SERVICE_ID := 24;

  NEST_REN_SERVICES_TAPI.DEL(
    QUALIFICATION_ID => QUALIFICATION_ID,
    SERVICE_ID => SERVICE_ID
  );
END;
--upd
DECLARE
  QUALIFICATION_ID NUMBER;
  OLD_SERVICE_ID NUMBER;
  NEW_SERVICE_ID NUMBER;
BEGIN
  QUALIFICATION_ID := NULL;
  OLD_SERVICE_ID := NULL;
  NEW_SERVICE_ID := NULL;

  NEST_REN_SERVICES_TAPI.UPD(
    QUALIFICATION_ID => QUALIFICATION_ID,
    OLD_SERVICE_ID => OLD_SERVICE_ID,
    NEW_SERVICE_ID => NEW_SERVICE_ID
  );
END;

