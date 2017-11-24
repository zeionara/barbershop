CREATE INDEX workers_index ON workers(position, qualification);

CREATE INDEX requests_index ON requests(worker_id, client_id, service_id);

CREATE UNIQUE INDEX salaries_index ON salaries(worker_id);
--already exists.CONSTRAINT PRIMARY KEY -is generating an index. Primary key constraint cannot exists without an index. 

CREATE INDEX premiums_index ON premiums(worker_id, premium_id);

CREATE INDEX workers_date_states_index ON workers_date_states(worker_id);
--such column list already indexed