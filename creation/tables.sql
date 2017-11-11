--basic data about clients of the barbershop
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

--possible positions of workers and it's descriptions
create table positions(
    id int not null,
    name varchar(50) not null,
    description varchar(200),
    
    constraint positions_pk primary key (id)
);
/

--possible qualifications of workers, it's descriptions and
--lists of services which each worker having this qualification
--can provide
create table qualifications(
    id int not null,
    name varchar(50) not null,
    description varchar(200),
    rendered_services services_table__,
    
    constraint qualifications_pk primary key (id)
)nested table rendered_services store as nested_rendered_services;
alter table nested_rendered_services add constraint unique_nested_services_id unique(id);
/

--basic data about workers of the barbershop
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
/

--contacts for communicating with people connected to the barbershop
create table contacts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    type varchar(10) not null check(type in ('phone','e-mail','vk')),
    contact varchar(20) not null,

    constraint contacts_pk primary key (id),
);
/

--possible services with prices (in roubles), descriptions and average duration
--(in minutes) which the barbershop can provide
create table services(
    id int not null,
    name varchar(20) not null,
    price numeric not null,
    description varchar(100),
    avg_duration int,
    
    constraint services_pk primary key (id)
);
/

--requests to the barbershop from clients including necessary
--resources with quantity of them
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

--resources which the barbeshop uses during serving clients
--with remaining amount
create table holdings(
    id int not null,
    name varchar(100) not null,
    price numeric not null,
    quantity numeric not null,
    
    constraint holdings_pk primary key (id)
);
/
--sizes of daily salaries of workers

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

--sizes of rewards for workers if they do their work very well
create table premiums_sizes(
    id int not null,
    name varchar(20) not null,
    min numeric not null,
    max numeric not null,
    description varchar(200),
    
    constraint premiums_sizes_pk primary key(id)
);
/

--journal of given rewards
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

--people's accounts on the website of the barbershop
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

--possible states of workers like 'basic', 'sick', 'resting', etc
create table workers_states(
    id int not null,
    name varchar(20) not null,
    description varchar(100),
    
    constraint workers_statuses_pk primary key(id)
);
/

--states of workers for each day
--(if there is no entry for a day by default the worker is working that day)
create table workers_date_states(
    id int not null,
    worker_id int not null,
    states day_states__,
    
    constraint workers_date_states_pk primary key(id),
    constraint workers_date_states_workers_fk foreign key(worker_id) references workers(id),
    constraint wds_workers_unique unique(worker_id)
)nested table states.day_state_table store as nested_states;
alter table nested_states add constraint unique_dates unique(date_);
/