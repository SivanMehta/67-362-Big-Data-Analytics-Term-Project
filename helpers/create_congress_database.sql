-- drop tables

drop table if exists bills;
drop table if exists bill_subjects;

-- create tables

create table bills(bill_id text, sponsor text, status int);
create table bills_subjects(bill_id text, subject text);

-- import the data (You have to change these paths on your machine beacuse postgres requires absolute paths)

copy bills from 'data_distilled/distilled_bills.csv' delimiter E'\t' CSV;

copy bills_subjects from 'data_distilled/distilled_bills_subjects.csv' delimiter E'\t' CSV;

