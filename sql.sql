CREATE TABLE thread 
(threadId INTEGER PRIMARY KEY AUTOINCREMENT,nama varchar(512) NOT NULL,post varchar(512) NOT NULL,userId int(12) NOT NULL );
CREATE TABLE comment ( commentId INTEGER PRIMARY KEY AUTOINCREMENT, comm varchar(512) NOT NULL, userId int(12) NOT NULL);
CREATE TABLE users ( userId INTEGER PRIMARY KEY AUTOINCREMENT, email varchar(128) NOT NULL, password varchar(512) NOT NULL );
insert into users values(1,"admin@susu.com","admin");
insert into thread values(1,"zz","zzz","1");
