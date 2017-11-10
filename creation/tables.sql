create table clients( 
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,

    constraint clients_pk primary key (id)
);
/
create table positions(
    id int not null,
    name varchar(50) not null,
    description varchar(200),
    
    constraint positions_pk primary key (id)
);
/
create table qualifications(
    id int not null,
    name varchar(50) not null,
    description varchar(200),
    rendered_services services_table__,
    
    constraint qualifications_pk primary key (id)
)nested table rendered_services store as nested_rendered_services;
alter table nested_rendered_services add constraint unique_nested_services_id unique(id);
/
--insert into positions (name) values ('Демон - парикмахер');
--select * from positions;

create table workers(
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,
    position int not null,
    qualification int not null,

    constraint workers_pk primary key (id),
    constraint workers_positions_fk foreign key(position) references positions(id),
    constraint workers_qualification_fk foreign key(qualification) references qualifications(id)
);
--alter table workers add qualification int;
--update workers set qualification = 1 where id = 2;
--alter table workers modify qualification int not null;
--alter table workers add constraint workers_qualification_fk foreign key(qualification) references qualifications(id);

/
create table contacts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    type varchar(10) not null check(type in ('phone','e-mail','vk')),
    contact varchar(20) not null,

    constraint contacts_pk primary key (id),
    constraint person_id_clients_workers_fk;
);
/
create table services(
    id int not null,
    name varchar(20) not null,
    price numeric not null,
    description varchar(100),
    avg_duration int,
    
    constraint services_pk primary key (id)
);
--alter table services add avg_duration int;
/
create table requests(
    id int not null,
    visit_date_time timestamp not null,
    worker_id int not null,
    client_id int not null,
    service_id int not null,
    note varchar(100),
    factical_durability numeric,
    holdings holdings_table__,
    
    constraint requests_pk primary key (id),
    constraint requests_workers_fk foreign key(worker_id) references workers(id),
    constraint requests_clients_fk foreign key(client_id) references clients(id),
    constraint requests_services_fk foreign key(service_id) references services(id)
)nested table holdings store as nested_holdings;
/
--select * from requests;
alter table requests add holdings holdings_table__ nested table holdings store as nested_holdings;

create table holdings(
    id int not null,
    name varchar(100) not null,
    price numeric not null,
    quantity numeric not null,
    
    constraint holdings_pk primary key (id)
);
/
create table salaries(
    id int not null,
    worker_id int not null,
    common numeric not null,
    vacation numeric not null,
    sick numeric not null,
    
    constraint salaries_pk primary key(id),
    constraint salaries_workers_fk foreign key(worker_id) references workers(id),
    constraint salaries_workers_unique unique(worker_id)
);
/
create table premiums_sizes(
    id int not null,
    name varchar(20) not null,
    min numeric not null,
    max numeric not null,
    description varchar(200),
    
    constraint premiums_sizes_pk primary key(id)
);
/
create table premiums(
    id int not null,
    premium_id int not null,
    worker_id int not null,
    earning_date date not null,
    premium_size numeric not null,
    note varchar(150),
    
    constraint premiums_pk primary key(id),
    constraint premiums_workers_fk foreign key(worker_id) references workers(id),
    constraint premiums_premiums_sizes_fk foreign key(premium_id) references premiums_sizes(id)
);
/
create table accounts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    login varchar(20) not null,
    passwd varchar(20) not null,
    avatar blob,
    
    constraint accounts_pk primary key(id)
);
/
create table workers_states(
    id int not null,
    name varchar(20) not null,
    description varchar(100),
    
    constraint workers_statuses_pk primary key(id)
);
--alter table workers_statuses rename to workers_states;
--select * from workers_states;
/
create table workers_date_states(
    id int not null,
    worker_id int not null,
    states day_states__,
    
    constraint workers_date_states_pk primary key(id),
    constraint workers_date_states_workers_fk foreign key(worker_id) references workers(id),
    constraint wds_workers_unique unique(worker_id)
)nested table states.day_state_table store as nested_states;
alter table nested_states add constraint unique_dates unique(date_);
--alter table workers_date_states add constraint wds_workers_unique unique(worker_id);
--drop table workers_date_states;