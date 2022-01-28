create table category(
    codename varchar(255) primary key,
    name varchar(255) not null,
    aliases text
);

create table purchase(
    id integer primary key,
    amount integer not null,
    name varchar(255) not null ,
    category_codename varchar(255) not null,
    created text default current_timestamp,
    FOREIGN KEY(category_codename) REFERENCES category(codename)
);

insert into category (codename, name, aliases)
values
    ("food", "продукты", "еда, кофе"),
    ("booze", "пьянка", "бар, ресторан, алкоголь"),
    ("taxi", "такси", "яндекс такси, yandex taxi, uber"),
    ("phone", "телефон", "теле2, связь, билайн"),
    ("books", "книги", "литература, литра, лит-ра"),
    ("internet", "интернет", "инет, inet, ростелеком"),
    ("subscriptions", "подписки", "подписка"),
    ("other", "прочее", "");

insert into purchase(amount, name, category_codename) values (650, 'интернет', 'internet');
insert into purchase(amount, name, category_codename) values (650, 'такса', 'taxi');
insert into purchase(amount, name, category_codename) values (440, 'крем', 'other');
insert into purchase(amount, name, category_codename) values (180, 'такса', 'taxi');
insert into purchase(amount, name, category_codename) values (230, 'такса', 'taxi');
insert into purchase(amount, name, category_codename) values (800, 'такса', 'taxi');
insert into purchase(amount, name, category_codename) values (500, 'баланс', 'phone');