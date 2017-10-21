"""Fit logistic model get predictive power of nutrients on food names."""
import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt
import re
import itertools
dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)

quantities = pd.read_sql_query('SELECT * from quantity', conn)
foods = pd.read_sql_query('SELECT * from food', conn)
nutrients = pd.read_sql_query('SELECT * from nutrient', conn)

conn.close()

# pivotdf = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
# get most common food names


def splitNameIntoWords(nameList):
    """Split food name into list of words."""
    matchString = '[^\W\d]*'
    words = [list(filter(None, re.findall(matchString, name))) for name in nameList]
    return words


foodNames = foods['name'].values
wordsInFoods = splitNameIntoWords(foodNames)
allWords = list(itertools.chain(*wordsInFoods))
wordcounts = pd.Series(allWords).value_counts()
wordcounts.index = wordcounts.index.map(str.lower)
unfun_words = ['upc', 's', 'with', 'and', 'in', 'a', 'gtin', 'to']
wordcounts.drop(unfun_words, inplace=True)

most_common_words = wordcounts[:100].index.unique()
foodNameDict = dict(zip(foods['ndbno'], wordsInFoods))

present = {}
for ndbno in foodNameDict:
    for word in most_common_words:
        if word not in present:
            present[word] = []
        if word in map(str.lower, foodNameDict[ndbno]):
            present[word].append(1)
        else:
            present[word].append(0)

wordPresence = pd.DataFrame(data=present, index=foodNameDict.keys())
wordPresence.mean().hist()
plt.show()

nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
combined_data = nutrient_amount.join(wordPresence, how='left')

# %%
# nut_train, nut_test, word_train, word_test = train_test_split(combined_data[nutrient_amount.columns], combined_data[most_common_words[0]], random_state=123456)
predict_word = most_common_words[0]
train_inds, test_inds = StratifiedShuffleSplit(n_splits=2, random_state=123456).split(np.zeros(len(combined_data)), combined_data[predict_word])
nut_train, nut_test, word_train, word_test = combined_data[nutrient_amount.columns].iloc[train_inds[0]], \
                                             combined_data[nutrient_amount.columns].iloc[train_inds[1]],  \
                                             combined_data[predict_word].iloc[train_inds[0]],    \
                                             combined_data[predict_word].iloc[train_inds[1]]

mms = MinMaxScaler()
nut_train_scaled = mms.fit_transform(nut_train)
nut_test_scaled = mms.transform(nut_test)

logreg = LogisticRegression(penalty='l1', C=.25, random_state=123456, max_iter=1000, solver='saga', verbose=False, n_jobs=-1)
logreg.fit(nut_train_scaled, word_train)
# print('training: ', )
# print('test: ', )
print(predict_word)
print(logreg.score(nut_train_scaled, word_train)-(1-word_train.mean()), logreg.score(nut_test_scaled, word_test)-(1-word_test.mean()))
c = logreg.coef_
plt.hist(np.ravel(c))
plt.show()
