"""Food name wordcloud."""
import itertools
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import re
from wordcloud import WordCloud

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)

# quantities = pd.read_sql_query('SELECT * from quantity', conn)
foods = pd.read_sql_query('SELECT * from food', conn)
# nutrients = pd.read_sql_query('SELECT * from nutrient', conn)
foodNames = foods['name'].values

conn.close()


def splitNameIntoWords(nameList):
    """Split food name into list of words."""
    matchString = '[^\W\d]*'
    words = [list(filter(None, re.findall(matchString, name))) for name in nameList]
    return words


wordsInFoods = splitNameIntoWords(foodNames)
# foodNameDict = dict(zip(foods['ndbno'], wordsInFoods))
allWords = list(itertools.chain(*wordsInFoods))
wordcounts = pd.Series(allWords).value_counts()
wordcounts.index = wordcounts.index.map(str.lower)
unfun_words = ['upc', 's', 'with', 'and', 'in', 'a', 'gtin', 'to']
wordcounts.drop(unfun_words, inplace=True)

xx, yy = np.meshgrid(np.linspace(-10, 10, num=1600), np.linspace(-10, 10, num=1600))
mask = np.square(xx) + np.square(yy * 1.1) > 95
mask = mask.astype('uint8')*255  # WordCloud wants mask as uint8 with disallowed pixels == 255
# %%
wcloud = WordCloud(width=1600, height=1600, mask=mask, colormap='ocean').generate_from_frequencies(wordcounts[:100].to_dict())
plt.rcParams["figure.figsize"] = (8, 8)
fig, ax = plt.subplots(1)
ax.imshow(wcloud)
ax.xaxis.set(ticks=[])
ax.yaxis.set(ticks=[])
plt.savefig('most_common_words.png', dpi=300, bbox_inches='tight')
plt.show()
