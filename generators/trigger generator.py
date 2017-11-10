def get_trigger(table_name):
    seq_name = table_name+"_id_seq"
    trigger_name = table_name+"_id_bir"
    
    print("create sequence "+seq_name+""" START WITH 1;

create or replace trigger """+trigger_name+""" 
before insert on """+table_name+""" 
for each row
begin
  select """+seq_name+""".nextval
  into   :new.id
  from   dual;
end;""")

get_trigger("accounts")
