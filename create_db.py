'''
Created on 31 мая 2016 г.

@author: Михаил Булыгин <pararanax@gmail.com>
'''

import sqlite3


if __name__ == '__main__':
    conn = sqlite3.connect("sessions.db")
    conn.execute("DROP TABLE sessions")
    sql = '''CREATE TABLE sessions (sid VARCHAR (12), number VARCHAR, answer VARCHAR, timer VARCHAR, time DATETIME)'''
    conn.execute(sql)