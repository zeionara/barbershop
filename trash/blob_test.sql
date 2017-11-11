DROP TABLE lob_tab;

CREATE TABLE lob_tab (
  number_content    NUMBER(10),
  varchar2_content  VARCHAR2(100),
  date_content      DATE,
  clob_content      CLOB,
  blob_content      BLOB
);

select * from lob_tab;

select * from accounts;