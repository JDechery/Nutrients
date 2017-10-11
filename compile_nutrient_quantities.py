import requests
import sqlite3
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('nutrient_db.log'), logging.StreamHandler()])

apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

report_url = 'https://api.nal.usda.gov/ndb/reports'
keeprunning = True

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()
itemrows = c.execute("SELECT * from food")
data = [['ndbno', '0'], ['format', 'json'], ['type', 'b'], ['api_key', apikey]]

insert_query = 'INSERT OR IGNORE INTO quantity (food_id, nutrient_id, value, units) VALUES (?, ?, ?, ?)'
try:
    while keeprunning:
        item_row = itemrows.fetchone()
        ndbno = item_row[0]
        if len(str(ndbno))<5:
                padsize = 5-len(str(ndbno))
                pad = ['0' for _ in range(padsize)]
                ndbno = ''.join(pad+list(str(ndbno)))

        data[0][1] = ndbno
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
                nutrient_data.append((int(ndbno), int(nut['nutrient_id']), float(nut['value']), nut['unit']))

            for values in nutrient_data:
                c.execute(insert_query, values)

        conn.commit()
        #data['offset'] += nitems
        time.sleep(10)#hard coded rate limiting; max 1000/hour
except KeyboardInterrupt
    conn.commit()
    conn.close()
    sys.exit(0)
