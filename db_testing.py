import sqlite3

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

print('test')

c.execute('SELECT * from items')
print(len(c.fetchall()))

a = c.fetchone()
print(a)

conn.close()
