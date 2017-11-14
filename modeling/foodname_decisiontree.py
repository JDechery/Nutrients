import Nutrients.utils as utl
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, make_scorer
from sklearn.ensemble import RandomForestClassifier
import pickle
import datetime

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=25)

# %% gridsearch for best random forest classifier (by f1_score)
classifier = RandomForestClassifier(n_jobs=-1, random_state=123456)
cv = StratifiedKFold(4)
param_grid = {'n_estimators': range(10, 211, 50), 'max_features': ['sqrt', None]}
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
