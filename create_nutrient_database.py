import requests
import sqlite3
import time
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('nutrient_db.log'), logging.StreamHandler()])

apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

report_url = 'https://api.nal.usda.gov/ndb/reports'
nitems = 1
keeprunning = True

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

item_ids = c.execute("SELECT id from items").fetchall()
nitem = 1
data = [['format', 'json'], ['type', 'b'], ['ndbno', '0'], ['api_key', apikey]]

while keeprunning:
    ndbno = item_ids[nitem][0]
    if len(str(ndbno))<5:
        padsize = 5-len(str(ndbno))
        pad = ['0' for _ in range(padsize)]
        ndbno = ''.join(pad+list(str(ndbno)))

    data[2][1] = ndbno
    nutrient_report = requests.get(report_url, params=data)
    if nutrient_report.status_code != 200:
        logging.warn('request error: http code {code}'.format(code=item_list.status_code))
        keeprunning = False
    else:
        logging.info('item {i}'.format(i=nitem))
        json_data = nutrient_report.json()
        json_data = json_data['report']['food']
        foodname = json_data['name']
        nutrient_data = []
        for nut in json_data['nutrients']:
            nutrient_data.append((int(nut['nutrient_id']), nut['name'], float(nut['value']), nut['unit']))
        #items = json_data['list']['item']
        #item_ids = [(int(it['id']), it['name']) for it in items]
        #item_ids = dict(item_ids)
        #nutrient_data = [()]


    conn.commit()
    nloop += 1
    data['offset'] += nitems
    time.sleep(3600)#hard coded rate limiting; max 1000/hour


conn.commit()
conn.close()
