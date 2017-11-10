create sequence clients_id_seq START WITH 1;

create or replace trigger clients_id_bir 
before insert on clients 
for each row
begin
  select clients_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence workers_id_seq START WITH 1;

create or replace trigger workers_id_bir 
before insert on workers 
for each row
begin
  select workers_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence clients_id_seq START WITH 1;

create or replace trigger clients_id_bir 
before insert on clients 
for each row
begin
  select clients_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence contacts_id_seq START WITH 1;

create or replace trigger contacts_id_bir 
before insert on contacts 
for each row
begin
  select contacts_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence services_id_seq START WITH 1;

create or replace trigger services_id_bir 
before insert on services 
for each row
begin
  select services_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence requests_id_seq START WITH 1;

create or replace trigger requests_id_bir 
before insert on requests 
for each row
begin
  select requests_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence holdings_id_seq START WITH 1;

create or replace trigger holdings_id_bir 
before insert on holdings 
for each row
begin
  select holdings_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence salaries_id_seq START WITH 1;

create or replace trigger salaries_id_bir 
before insert on salaries 
for each row
begin
  select salaries_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence premiums_sizes_id_seq START WITH 1;

create or replace trigger premiums_sizes_id_bir 
before insert on premiums_sizes 
for each row
begin
  select premiums_sizes_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence premiums_id_seq START WITH 1;

create or replace trigger premiums_id_bir 
before insert on premiums 
for each row
begin
  select premiums_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence workers_statuses_id_seq START WITH 1;

create or replace trigger workers_statuses_id_bir 
before insert on workers_statuses 
for each row
begin
  select workers_statuses_id_seq.nextval
  into   :new.id
  from   dual;
end;

create sequence accounts_id_seq START WITH 1;

create or replace trigger accounts_id_bir 
before insert on accounts 
for each row
begin
  select accounts_id_seq.nextval
  into   :new.id
  from   dual;
end;

CREATE OR REPLACE TRIGGER contacts_before_insert
BEFORE INSERT
   ON contacts
   FOR EACH ROW
BEGIN
    --checking person id
    if (not is_person_id_valid(:new.person_status,:new.person_id)) then 
    begin
        RAISE_APPLICATION_ERROR(-20101, 'There is no such ' || :new.person_status);
        ROLLBACK;
    end;
    end if;
    
    --checking content of contact
    if (not is_contact_valid(:new.type,:new.contact)) then 
    begin
        RAISE_APPLICATION_ERROR(-20101, 'It is invalid ' || :new.type);
        ROLLBACK;
    end;
    end if;
    
END;

create or replace trigger accounts_before_insert
before insert
   on accounts
   for each row
begin
    if (not is_person_id_valid(:new.person_status,:new.person_id)) then 
    begin
        raise_application_error(-20101, 'There is no such ' || :new.person_status);
        rollback;
    end;
    end if;
end;

create or replace trigger requests_before_insert
before insert
   on requests
   for each row
begin
    if (not is_master_unbusy(:new.visit_date_time,:new.service_id,:new.worker_id)) then 
    begin
        raise_application_error(-20101, 'The master is busy at that time');
        rollback;
    end;
    end if;
end;

create or replace trigger premiums_before_insert
before insert
   on premiums
   for each row
begin
    if (not is_premium_valid(:new.premium_size,:new.premium_id)) then 
    begin
        raise_application_error(-20101, 'The premium is appointed unfairly');
        rollback;
    end;
    end if;
end;