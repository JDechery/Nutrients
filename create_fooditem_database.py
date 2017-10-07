import requests
import json
import sqlite3
import time
import logging

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('fooditem_db.log'), logging.StreamHandler()])

apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

list_url = 'https://api.nal.usda.gov/ndb/list'
nitems = 900
keeprunning = True

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()

nloop = 0
data = {'format' : 'json',
        'lt'     : 'f',
        'sort'   : 'n',
        'max'    : nitems,
        'offset' : 7550,
        'api_key': apikey}
while keeprunning:

    item_list = requests.get(list_url, params=data)
    if item_list.status_code != 200:
        logging.warn('request error: http code {code}'.format(code=item_list.status_code))
        keeprunning = False
    else:
        logging.info('loop {i}'.format(i=nloop))
        json_data = item_list.json()

        items = json_data['list']['item']
        item_ids = [(int(it['id']), it['name']) for it in items]
        item_ids = dict(item_ids)

        for key, val in item_ids.items():
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
