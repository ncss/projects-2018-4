import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()
f = open('init.sql', 'r')
cur.executescript(f.read())
cur.close()
conn.close()
