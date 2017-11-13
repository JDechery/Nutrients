import pandas as pd
import Nutrients.utils as utl
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
import pickle
import datetime

# dbfile = 'F:/Data/nutrients_database.sqlite'
# conn = sqlite3.connect(dbfile)
#
# quantities = pd.read_sql_query('SELECT * from quantity', conn)
# foods = pd.read_sql_query('SELECT * from food', conn)
# nutrients = pd.read_sql_query('SELECT * from nutrient', conn)
#
# conn.close()
#
#
# def splitNameIntoWords(nameList):
#     """Split food name into list of words."""
#     matchString = '[^\W\d]*'
#     words = [list(filter(None, re.findall(matchString, name))) for name in nameList]
#     return words
#
#
# foodNames = foods['name'].values
# wordsInFoods = splitNameIntoWords(foodNames)
# allWords = list(itertools.chain(*wordsInFoods))
# wordcounts = pd.Series(allWords).value_counts()
# wordcounts.index = wordcounts.index.map(str.lower)
# unfun_words = ['upc', 's', 'with', 'and', 'in', 'a', 'gtin', 'to']
# wordcounts.drop(unfun_words, inplace=True)
#
# most_common_words = wordcounts[:25].index.unique()
# foodNameDict = dict(zip(foods['ndbno'], wordsInFoods))
#
# present = {}
# for ndbno in foodNameDict:
#     for word in most_common_words:
#         if word not in present:
#             present[word] = []
#         if word in map(str.lower, foodNameDict[ndbno]):
#             present[word].append(1)
#         else:
#             present[word].append(0)
#
# wordPresence = pd.DataFrame(data=present, index=foodNameDict.keys())
#
# nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
# combined_data = nutrient_amount.join(wordPresence, how='left')
# targets = combined_data[most_common_words]
# predictors = combined_data[nutrient_amount.columns]
targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=25)

# %% gridsearch for best random forest classifier (by f1_score)
# prepper = MinMaxScaler()
classifier = RandomForestClassifier(n_jobs=-1, random_state=123456)
cv = StratifiedKFold(4)
# param_grid = {'prepper__n_components': [75, 100], 'estimator__C': [.75, 1.]}
param_grid = {'n_estimators': range(10, 211, 50), 'max_features': ['sqrt', None]}
# pipe = Pipeline([('prepper', prepper), ('clf', classifier)])
gsrch = GridSearchCV(estimator=classifier, param_grid=param_grid, scoring=make_scorer(f1_score), cv=cv)

# %%
acc = {}
for word in targets.columns:
    gsrch.fit(predictors, targets[word])
    acc[word] = (gsrch.cv_results_, gsrch.best_estimator_)
    print(word, acc[word][0])

# save results
today = datetime.datetime.now()
filepath = 'F:/Data/forest_results_' + today.strftime('%Y%m%d') + '.pkl'
with open(filepath, 'wb') as pklfile:
    pickle.dump(acc, pklfile)
