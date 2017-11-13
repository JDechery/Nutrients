import requests
import sqlite3
import time
import logging
import sys


def format_ndbno(no):
    """Pad with zeros if ndbno only have 4 no's."""
    if len(str(no)) < 5:
        padsize = 5-len(str(no))
        pad = ['0' for _ in range(padsize)]
        ndbno = ''.join(pad+list(str(no)))
    else:
        ndbno = str(no)
    return ndbno


logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('nutrient_db.log'), logging.StreamHandler()])

apikey = '0nDIJuT0aCiNbIiwxVIpAWRUKauc4EdLNQgSjUc1'

report_url = 'https://api.nal.usda.gov/ndb/reports'
keeprunning = True
data = [['ndbno', '0'], ['format', 'json'], ['type', 'f'], ['api_key', apikey]]

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)
c = conn.cursor()
itemrows = c.execute("SELECT * from food LEFT JOIN quantity ON food.ndbno = quantity.food_id WHERE quantity.food_id IS NULL").fetchall()
loopid = 0
insert_query = 'INSERT OR IGNORE INTO quantity (food_id, nutrient_id, value, units) VALUES (?, ?, ?, ?)'
try:
    while keeprunning:
        itemrow = itemrows[loopid]
        logging.info('starting item {i} {j}'.format(i=itemrow[0], j=itemrow[1]))
        ndbno = itemrow[0]
        data[0][1] = format_ndbno(ndbno)

        nutrient_report = requests.get(report_url, params=data)
        if nutrient_report.status_code != 200:
            logging.warn('request error: http code {code}'.format(code=nutrient_report.status_code))
            keeprunning = False
        else:
            json_data = nutrient_report.json()
            json_data = json_data['report']['food']
            foodname = json_data['name']
            nutrient_data = []
            for nut in json_data['nutrients']:
                nutrient_data.append((int(ndbno), int(nut['nutrient_id']), float(nut['value']), nut['unit']))

            for values in nutrient_data:
                c.execute(insert_query, values)

        loopid += 1
        conn.commit()
        time.sleep(8)  # hard coded rate limiting; max 1000/hour
except KeyboardInterrupt:
    conn.commit()
    conn.close()
    sys.exit(0)
else:
    conn.commit()
    conn.close()
