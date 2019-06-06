-- we don't know how to generate schema aux_verification (class Schema) :(
create table entity_mark
(
  id             bigint auto_increment
    primary key,
  content        text             null,
  origin_content text             null,
  passed         int default '-1' not null,
  reviewed       int default '0'  not null,
  ver_date       date             null,
  stat_id        bigint           null,
  description    varchar(255)     null,
  verify_result  int default '-1' null,
  constraint FKk3cm81r6jr3y2rqnl6gxps8rp
  foreign key (stat_id) references ver_statement (id)
)
  charset = utf8;



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
)charset=utf8
;

create table mark_option
(
  id      bigint auto_increment
    primary key,
  opinion varchar(255) null
)
  charset = utf8;



create table relation_mark
(
  id             bigint auto_increment
    primary key,
  content        text             null,
  origin_content text             null,
  passed         int default '-1' not null,
  reviewed       int default '0'  not null,
  ver_date       date             null,
  relation_id    bigint           null,
  stat_id        bigint           null,
  description    varchar(255)     null,
  verify_result  int default '-1' null,
  constraint FK2x0thgu8byj8dvk2pa1gkvgkr
  foreign key (stat_id) references ver_statement (id),
  constraint FKnap6jpb946ljc0laiu59jwmpj
  foreign key (relation_id) references rela_name_no (id)
)
  charset = utf8;



create table user
(
  id       bigint auto_increment
    primary key,
  email    varchar(255)                         null,
  password varchar(255)                         null,
  name     varchar(255) default '天野远子'          null,
  avatar   varchar(255) default '/avatar.2.jpg' null,
  role     varchar(255) default 'admin'         null
)
  charset = utf8;


create table ver_statement
(
  id        bigint auto_increment
    primary key,
  mark_user varchar(10)     null,
  pdf_no    int             null,
  pdf_path  varchar(255)    null,
  user_id   bigint          null,
  state     int default '0' null,
  mark_id   int             null,
  constraint FKgxn709dk7on4hkv77650knqnh
  foreign key (user_id) references user (id)
)
  charset = utf8;

create index ver_statement_pdf_path_pdf_no_mark_id_index
  on ver_statement (pdf_path, pdf_no, mark_id);



