import sqlite3
import requests

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

# %% get nutrient list_url
apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'
nitems = 450
list_url = 'https://api.nal.usda.gov/ndb/list'
data = (('format', 'json'), ('lt', 'n'), ('sort', 'n'), ('max', nitems), ('offset', 0), ('api_key', apikey))

nutrient_response = requests.get(list_url, params=data)
#print(nutrient_response.status_code)
# %% create table for individual nutrient metadata
nutrient_data = nutrient_response.json()
nutrient_data = nutrient_data['list']['item']
nutrient_ids = [(n['id'], n['name']) for n in nutrient_data]
#uids = list(set([int(x[0]) for x in nutrient_ids]))

creation_query = 'CREATE TABLE nutrients (id INT PRIMARY KEY, name TEXT)'
c.execute(creation_query)
c.executemany('INSERT INTO nutrients (id, name) VALUES (?, ?)', nutrient_ids)
conn.commit()

# %% create tables with column for each nutrient; column name is foreign key to nutrient table
nutrient_fk = sorted([x[0] for x in nutrient_ids])
query = 'CREATE TABLE foods ('
col12 = 'id INT PRIMARY KEY, name TEXT, '
col3plus = ', '.join(['n{} REAL'.format(n) for n in nutrient_fk])
query = ''.join([query, col12, col3plus, ');'])
print(query)
c.execute(query)

conn.commit()
conn.close()
