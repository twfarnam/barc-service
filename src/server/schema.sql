
drop table if exists images;

create table images(
  id integer primary key autoincrement,
  created_at text not null,
  result text,
  latency int,
  device_id text,
  ip_address text
);

