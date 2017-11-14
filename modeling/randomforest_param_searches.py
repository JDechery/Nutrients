# import pandas as pd
import Nutrients.utils as utl
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
import pickle
import datetime

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=20)

# %% 'array'-search across hyperparameters one at a time
param_grids = [
    {'max_depth': [3, 7, 13, 17, 23, None]},
    {'min_samples_leaf': [100, 50, 10, 5, 3, 1]},
    {'max_leaf_nodes': [2, 10, 50, 100, 200, None]}]


def make_gridsearch_param(param_grid):
    cv = StratifiedKFold(5)
    ntrees = 100
    classifier = RandomForestClassifier(n_estimators=ntrees, random_state=123456, n_jobs=-1)
    gsrch = GridSearchCV(estimator=classifier, param_grid=param_grid, scoring=make_scorer(f1_score), cv=cv)
    return gsrch


results = {}
print(targets.columns)
for word in targets.columns:
    print('starting ' + word)
    results[word] = []
    for grid in param_grids:
        gsrch = make_gridsearch_param(grid)
        gsrch.fit(predictors, targets[word])
        results[word].append((gsrch.cv_results_, gsrch.best_estimator_))
        print(word + ' completed')

# save results
today = datetime.datetime.now()
filepath = 'F:/Data/forest_results_' + today.strftime('%Y%m%d') + '.pkl'
with open(filepath, 'wb') as pklfile:
    pickle.dump(results, pklfile)
