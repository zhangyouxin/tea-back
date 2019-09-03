DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS messages;

create table users (id SERIAL PRIMARY KEY, username VARCHAR(25) NOT NULL, password VARCHAR(128) NOT NULL, super smallint NOT NULL DEFAULT 0);
CREATE UNIQUE INDEX users_username ON users (username);

insert into users(username, password, super) values('admin', 'PBKDF2$sha256$901$qy3SCiU4YncLaVLv$uE/2grmw1lxKm4CsbrqcL6ObQKLXHZxk', 1);
insert into users(username, password) values('jin', 'PBKDF2$sha256$901$qy3SCiU4YncLaVLv$uE/2grmw1lxKm4CsbrqcL6ObQKLXHZxk');


create table message (id SERIAL PRIMARY KEY, sub_topic VARCHAR(25) NOT NULL, device_no VARCHAR(25) NOT NULL, message VARCHAR(128) NOT NULL DEFAULT 0);
insert into messages(sub_topic, device_no, message) values('sub', '123', 'hello');
