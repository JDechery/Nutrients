import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline
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

most_common_words = wordcounts[:25].index.unique()
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

nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
combined_data = nutrient_amount.join(wordPresence, how='left')
targets = combined_data[most_common_words]
predictors = combined_data[nutrient_amount.columns]

# %% cross validated pipeline to find best boosted classifier for each word
prepper = PCA()
# estimator = LogisticRegression(penalty='l1', random_state=123456, max_iter=10, solver='saga', verbose=False, n_jobs=-1)
classifier = GradientBoostingClassifier(random_state=123456)
cv = StratifiedKFold(3)
# param_grid = {'prepper__n_components': [75, 100], 'estimator__C': [.75, 1.]}
param_grid = {'prepper__n_components': [200],
              'clf__n_estimators': [100, 150, 200],
              'clf__learning_rate': [1.0],
              'clf__max_depth': [1, 2]}
pipe = Pipeline([('prepper', prepper), ('clf', classifier)])
gsrch = GridSearchCV(estimator=pipe, param_grid=param_grid, scoring='accuracy', cv=cv)


def convert_accuracy(raw_accuracy, null_accuracy):
    """Convert sklearn accuracy value to null accuracy given by mean value of binary target."""
    if not isinstance(raw_accuracy, list):
        raw_accuracy = [raw_accuracy]
    perc_accuracy = list(map(lambda x: (x - null_accuracy) / (1. - null_accuracy), raw_accuracy))
    return perc_accuracy


# %%
acc = {}
for word in most_common_words:
    gsrch.fit(predictors, targets[word])
    acc[word] = (convert_accuracy(gsrch.best_score_, 1-targets[word].mean()), gsrch.best_estimator_)
    print(word, acc[word][0])
