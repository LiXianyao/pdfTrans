-- we don't know how to generate schema aux_verification (class Schema) :(
create table if not exists entity_mark
(
	id bigint auto_increment
		primary key,
	content text not null,
	passed bit default b'0' not null,
	reviewed bit default b'0' not null,
	ver_date date null,
	user_id bigint null
)
charset=utf8
;

create table if not exists rela_name_no
(
	id bigint auto_increment comment '主键'
		primary key,
	rela_name varchar(255) not null comment '关系名称',
	rela_no varchar(255) not null,
	constraint rela_name_no_rela_name_uindex
		unique (rela_name),
	constraint rela_name_no_rela_no_uindex
		unique (rela_no)
)
;

create table if not exists relation_mark
(
	id bigint auto_increment
		primary key,
	content text not null,
	passed bit default b'0' not null,
	relation_id bigint null,
	reviewed bit default b'0' not null,
	ver_date date null,
	user_id bigint null
)
charset=utf8
;

create table if not exists user
(
	id bigint auto_increment
		primary key,
	email varchar(64) not null,
	password varchar(128) not null,
	phone varchar(11) not null
)
charset=utf8
;

