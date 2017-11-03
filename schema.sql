
drop table if exists images;

create table images(
  id integer primary key autoincrement,
  result text not null default '',
  score text not null default '',
  created_at text not null
);


drop table if exists captions;

create table captions(
  id integer primary key,
  caption text not null
);


