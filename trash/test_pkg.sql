CREATE or replace PACKAGE tpg AS
   function calc_smth(nn int) return int;
END tpg;
/

CREATE or replace PACKAGE BODY tpg AS
-- the following parameter declaration raises an exception 
-- because 'DATE' does not match employees.hire_date%TYPE
-- PROCEDURE calc_bonus (date_hired DATE) IS
-- the following is correct because there is an exact match
   FUNCTION calc_smth (nn int) return int IS
   BEGIN
     DBMS_OUTPUT.PUT_LINE('Employees hired on ' || ' get bonus.');
     return nn*2;
   END;
END tpg;
/

tpg.calc_smth(10);