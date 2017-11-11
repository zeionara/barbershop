
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

create or replace type holding__ as object (
    id int,
    quantity int
);

create or replace type holdings_table__ as table of holding__;

create or replace type service__ as object (
    id int
);

create or replace type services_table__ as table of service__;

--
--special types
--
create or replace type client__ as object (
    name varchar(10),
    patronymic varchar(50),
    phone varchar(20),
    date_ date
);
drop type clients_table__;
create or replace type clients_table__ as table of client__;