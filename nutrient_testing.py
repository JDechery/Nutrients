# %% import / database block
import requests
import sqlite3

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

c.execute('SELECT * from items')
example_item = c.fetchone()
print(example_item[0])
# %% request block
report_url = 'https://api.nal.usda.gov/ndb/reports'
apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

# data = {'format' : 'json',
#         'type'   : 'b',
#         'api_key': apikey}
# data['ndbno'] = '01009'
# print(data)
data = (('ndbno', '01009'), ('type', 'b'), ('format', 'json'), ('api_key', apikey))

# seen = set()
# while True:
#     r = requests.get(report_url, params=data, allow_redirects=False)
#     loc = r.headers['location']
#     if loc in seen: break
#     seen.add(loc)
#     print(loc)
#     print(r.status_code)
nutrient_report = requests.get(report_url, params=data)

json_data = nutrient_report.json()
# %% format nutrient data and insert into table
subfields = ('ndbno', 'name', 'nutrients')
item_nutrients = dict((k, json_data['report']['food'][k]) for k in subfields)

# print(json_data)
