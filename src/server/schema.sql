
drop table if exists images;

create table images(
  id text primary key,
  created_at text not null,
  categories text not null default "[]",
  width int not null,
  height int not null,
  result text,
  motion text,
  latency int,
  device_id text,
  ip_address text
);



