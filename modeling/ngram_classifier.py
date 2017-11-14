import Nutrients.utils as utl
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
import pickle
import datetime

targets, predictors = utl.get_ngramtargets_nutrientpredictors(mincount=250)

# %% gridsearch for best random forest classifier (by f1_score)
# cv = StratifiedKFold(8)
classifier = RandomForestClassifier(n_jobs=-1, n_estimators=250, random_state=123456)
# param_grid = {'n_estimators': range(10, 211, 50), 'max_features': ['sqrt', None]}
# gsrch = GridSearchCV(estimator=classifier, param_grid=param_grid, scoring=make_scorer(f1_score), cv=cv)

# %%
acc = {}
for word in targets.columns:
    scores = cross_val_score(classifier, predictors, targets[word], cv=8, scoring=make_scorer(f1_score))
    acc[word] = scores
    print(word, scores)

# save results
today = datetime.datetime.now()
filepath = 'F:/Data/forest_ngram_results_' + today.strftime('%Y%m%d') + '.pkl'
with open(filepath, 'wb') as pklfile:
    pickle.dump(acc, pklfile)
