import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE category (
  id INTEGER NOT NULL,
  image BLOB NOT NULL,
  information TEXT,
  name TEXT NOT NULL,
  PRIMARY KEY (id)
);''')

cur.execute('''
CREATE TABLE memes (
  id INTEGER NOT NULL,
  image BLOG NOT NULL,
  caption TEXT,
  location TEXT,
  username TEXT NOT NULL,
  timestamp TEXT,
  catid INTEGER NOT NULL,
  FOREIGN KEY (catid) REFERENCES category(id),
  PRIMARY KEY (id)
);
''')
f = open('init.sql', 'r')
for line in f:
    if line.startswith('INSERT INTO'):
        cur.execute(line)
