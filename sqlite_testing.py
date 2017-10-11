#sqlite testing
import sqlite3

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()
itemrows = c.execute("SELECT * from food")
items = itemrows.fetchone();
for loopid in range(10):
    print(itemrows.fetchone())



conn.close()
