import sqlite3

connection = sqlite3.connect('dbase.db')
cur = connection.cursor()
cur.execute('drop table if exists run')
TABLE = """create table run (
                           id integer primary key autoincrement,
                           start_time DATETIME not null,
                           end_time DATETIME not null
                           );
                           """

cur.execute(TABLE)
connection.close()