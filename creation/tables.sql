create table clients( 
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,

    constraint clients_pk primary key (id)
);

create table workers(
    id int not null,
    name varchar(10) not null,
    surname varchar(20) not null,
    patronymic varchar(30),
    sex char not null check(sex in ('m','f')),
    address varchar(50) not null,
    position varchar(20) not null,
    qualification varchar(20) not null,

    constraint workers_pk primary key (id)
);

create table contacts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    type varchar(10) not null check(type in ('phone','e-mail','vk')),
    contact varchar(20) not null,

    constraint contacts_pk primary key (id),
    constraint person_id_clients_workers_fk check(is_person_id_valid(person_status));
);

create table services(
    id int not null,
    name varchar(20) not null,
    price numeric not null,
    description varchar(100),
    avg_duration int,
    
    constraint services_pk primary key (id)
);
--alter table services add avg_duration int;

create table requests(
    id int not null,
    visit_date_time timestamp not null,
    worker_id int not null,
    client_id int not null,
    service_id int not null,
    note varchar(100),
    factical_durability numeric,
    
    constraint requests_pk primary key (id),
    constraint requests_workers_fk foreign key(worker_id) references workers(id),
    constraint requests_clients_fk foreign key(client_id) references clients(id),
    constraint requests_services_fk foreign key(service_id) references services(id)
);

create table holdings(
    id int not null,
    name varchar(100) not null,
    price numeric not null,
    quantity numeric not null,
    
    constraint holdings_pk primary key (id)
);

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

create table premiums_sizes(
    id int not null,
    name varchar(20) not null,
    min numeric not null,
    max numeric not null,
    description varchar(200),
    
    constraint premiums_sizes_pk primary key(id)
);

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

create table accounts(
    id int not null,
    person_id int not null,
    person_status varchar(10) not null check(person_status in ('worker','client')),
    login varchar(20) not null,
    passwd varchar(20) not null,
    avatar blob,
    
    constraint accounts_pk primary key(id)
);
    

create table workers_statuses(
    id int not null,
    name varchar(20) not null,
    description varchar(100),
    
    constraint workers_statuses_pk primary key(id)
);