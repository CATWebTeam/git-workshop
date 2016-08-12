drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  username text not null,
  email text not null,
  pw_hash text not null
);

drop table if exists follower;
create table follower (
  who_id integer,
  whom_id integer
);

drop table if exists message;
create table twitte (
  twitte_id integer primary key autoincrement,
  user_id integer not null,
  twitte_text text not null,
  pub_date integer
);
