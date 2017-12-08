create or replace package array_test_tapi
is

type num_arr IS TABLE OF NUMBER INDEX BY PLS_INTEGER;

procedure ins (
arr in num_arr,
iid in number
);

procedure get(
arr out num_arr,
iid in number
);

end array_test_tapi;
/
create or replace package body array_test_tapi
is
-- insert
procedure ins (
arr in num_arr,
iid in number
) is
st services_table__;
begin
    st := services_table__();
    for i in arr.first .. arr.last loop
        dbms_output.put_line('ok');
        st.extend;
        st(st.count) := new_service(arr(i));
    end loop;
    update qualifications set rendered_services = st where id = iid;
    dbms_output.put_line('ok');
end;

procedure get (
arr out num_arr,
iid in number
) is
st services_table__;
parr num_arr;
begin
    --parr := num_arr();
    --st := services_table__();
    --select rendered_services into st from qualifications where id = iid;
    --for i in st.first .. st.last loop
    --    dbms_output.put_line('ok');
        --parr.extend;
    --   arr(i) := st(i).id;
    --end loop;
    dbms_output.put_line('ok');
end;

end array_test_tapi;
/