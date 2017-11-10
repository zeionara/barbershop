LOAD DATA 
INFILE 'rows.txt'
   INTO TABLE accounts
   FIELDS TERMINATED BY ','
   (person_id    char(3),
    person_status  char(10),
	login			char(20),
	passwd		char(20),
    blob_filename     FILLER CHAR(100),
    avatar      LOBFILE(blob_filename) TERMINATED BY EOF)