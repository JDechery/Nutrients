import sqlite3

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

# %% get nutrient list_url
apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'
nitems = 450
list_url = 'https://api.nal.usda.gov/ndb/list'
data = (('format', 'json'), ('lt', 'n'), ('sort', 'n'), ('max', nitems), ('offset', 0), ('api_key', apikey))

nutrient_response = requests.get(list_url, params=data)
nutrient_data = nutrient_response.json()
nutrient_data = nutrient_data['list']['item']
nutrient_ids = [(n['id'], n['name']) for n in nutrient_data]

# %% create tables with column for each nutrient
query = 'CREATE TABLE nutrients ('
col12 = 'id INT PRIMARY KEY, name TEXT, '
col3plus = ', '.join(['{} TEXT'.format(n[1]) for n in nutrient_ids])
query = ''.join([query, col12, col3plus, ');'])
c.execute(query)

conn.commit()
conn.close()
