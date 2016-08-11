drop table if exists twittes
create table twittes (
  twitte_id integer primary key autoincrement,
  user_id intger not null,
  twitte_text text not null,
  pub_date integer
);
