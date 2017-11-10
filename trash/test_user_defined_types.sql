create or replace type day_state__ as object (
    date_ date,
    state_code int
);

create or replace type day_state_table__ as table of day_state__;

create or replace type day_states__ as object (
    day_state_table day_state_table__,
    member function get_state(required_date date) return int
);

create or replace type body day_states__ as 
    member function get_state(required_date date) return int is 
    state_ int;
    begin 
        for i in day_state_table.first .. day_state_table.last loop
            if (day_state_table(i).date_ = required_date) then
                state_ := day_state_table(i).state_code;
                exit;
            end if;
        end loop;
        if state_ is null then state_ := 0;
        end if;
        return state_; 
    end get_state; 
end;

set serveroutput on;
declare
foo int;
day_states day_states__;
begin
    --day_states__(null);
    day_states := day_states__(day_state_table__(day_state__(TO_DATE('2003/07/09', 'yyyy/mm/dd'), 1),
                                                 day_state__(TO_DATE('2003/07/10', 'yyyy/mm/dd'), 2)));
    foo := day_states.get_state(TO_DATE('2003/07/11', 'yyyy/mm/dd'));
    dbms_output.put_line('ok' || to_char(foo));
end;


CREATE TYPE external_person AS OBJECT (
  name        VARCHAR2(30),
  phone       VARCHAR2(20) );
  
CREATE TYPE lineitem AS OBJECT (
  item_name   VARCHAR2(30),
  quantity    NUMBER,
  unit_price  NUMBER(12,2) );

CREATE TYPE lineitem_table AS TABLE OF lineitem;
  
CREATE TYPE purchase_order AS OBJECT (
  id          NUMBER,
  contact     external_person,
  lineitems   lineitem_table,
  
  MEMBER FUNCTION
  get_value   RETURN NUMBER );