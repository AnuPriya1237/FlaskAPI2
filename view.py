import sqlite3
def insert(start_time, end_time):
    connection = sqlite3.connect('dbase.db')
    cur = connection.cursor()
    cur.execute('insert into run(start_time, end_time) values (?,?)',(start_time, end_time))

    connection.commit()
    connection.close()


def getdata():
    connection = sqlite3.connect('dbase.db')
    cur = connection.cursor()
    cur.execute('select * from run')
    post = cur.fetchall()
    return post