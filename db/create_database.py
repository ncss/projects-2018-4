import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()

f = open('init.sql', 'r')
for line in f:
    cur.execute(line)
conn.close()
