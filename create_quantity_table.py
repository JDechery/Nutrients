import sqlite3

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

quant_query = '''CREATE TABLE quantity (
                    id INTEGER PRIMARY KEY,
                    food_id INTEGER,
                    nutrient_id INTEGER,
                    value REAL,
                    units TEXT,
                    FOREIGN KEY (food_id) REFERENCES food(ndbno),
                    FOREIGN KEY (nutrient_id) REFERENCES nutrient(id))'''
print(quant_query)
c.execute(quant_query)
conn.commit()
conn.close()
