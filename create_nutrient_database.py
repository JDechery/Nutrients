import requests
import sqlite3
import time
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('nutrient_db.log'), logging.StreamHandler()])

apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

report_url = 'https://api.nal.usda.gov/ndb/report'
nitems = 900
keeprunning = True

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

item_ids = c.execute("SELECT ids from items")

nitem = 1
data = {'format' : 'json',
        'type'   : 'b'
        'ndbno'  : '',
        'api_key': apikey}
while keeprunning:

    data['ndbno'] = item_ids[nitem]
    nutrient_report = requests(report_url, params=data)
    if nutrient_report.status_code != 200:
        logging.warn('request error: http code {code}'.format(code=item_list.status_code))
        keeprunning = False
    else:
        logging.info('item {i}'.format(i=nitem))
        json_data = nutrient_report.json()

        #items = json_data['list']['item']
        #item_ids = [(int(it['id']), it['name']) for it in items]
        #item_ids = dict(item_ids)
        #nutrient_data = [()]

        for data in nutrient_data
            try:
                c.execute('INSERT OR IGNORE INTO items VALUES (?, ?);', (key, val))
            except Exception as e:
                logging.error('database operation failed')
                logging.error(str(e))
                break

    conn.commit()
    nloop += 1
    data['offset'] += nitems
    time.sleep(3600)#hard coded rate limiting; max 1000/hour


conn.commit()
conn.close()
