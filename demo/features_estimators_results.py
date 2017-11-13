import pandas as pd
import Nutrients.utils as utl
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=150)
nutrients = utl.load_sql_table('nutrient')
nutrients = nutrients.loc[nutrients['id'].isin(predictors.columns), :]

with open('F:/Data/forest_results_20171112.pkl', 'rb') as f:
    forest_clf = pickle.load(f)
# %% best results
best_results = {}
for key, val in forest_clf.items():
    best_idx = val[0]['rank_test_score'][0]-1
    params = val[0]['params'][best_idx]
    best_results[key] = (val[0]['mean_test_score'][best_idx], val[0]['std_test_score'][best_idx], params['max_features'], params['n_estimators'])

best_results = pd.concat([targets.mean(), pd.DataFrame.from_dict(best_results, orient='index')], axis=1)
best_results.columns = ['term_prob', 'mean_score', 'std_score', 'max_features', 'n_estimators']

# %% plot
resultplot = best_results.sort_values(by='mean_score', ascending=False)
resultplot = resultplot.iloc[:25, :]

matplotlib.rcParams.update({'font.size': 16})
fig, ax = plt.subplots(figsize=(12, 8))
plt.scatter(resultplot.term_prob, resultplot.mean_score)
np.random.seed(12345)
text_positions = [(x+np.random.randn()*.001, y+np.random.randn()*.01) for x, y in zip(resultplot.term_prob, resultplot.mean_score)]
[plt.text(pt[0], pt[1], txt) for pt, txt in zip(text_positions, resultplot.index)]
plt.xlabel('word probability')
plt.ylabel('best forest f1 score')
plt.show()

# %% full results
results = {}
for key, val in forest_clf.items():
    pars = [tuple(el.values()) for el in val[0]['params']]
    results[key] = val[0]['mean_test_score']
pars = [list(map(str, p)) for p in pars]
results = pd.DataFrame.from_dict(results, orient='index')
results.columns = pd.MultiIndex.from_tuples(pars, names=['max_features', 'n_estimators'])

results = results.div(results.max(axis=1), axis=0)

# %%
fig, ax = plt.subplots(figsize=(12, 8))
# kernels = list(results.apply(gaussian_kde))
# pts = np.arange(0, 1, .01)
# for idx, k in enumerate(kernels):
#     plt.plot(pts, k(pts)+idx)
results.boxplot(rot=90, showfliers=False)
plt.grid(False)
plt.title('grid search mean results')
plt.ylabel('mean score (normalized)')
plt.xlabel('parameters (max_features, n_estimators)')
plt.show()

# %% best performing forest
example_word = 'lean'
clf = forest_clf[example_word][1]
Xtrain, Xtest, ytrain, ytest = train_test_split(predictors, targets[example_word])
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)
print('test-data confusion matrix')
print(confusion_matrix(ytest, ypred))

features = list(zip(clf.feature_importances_, nutrients['name']))
features = sorted(features, key=lambda x: x[0], reverse=True)
print('10 ten predictive nutrients for ' + example_word.join('\''*2))
print(*['%0.3f, %s' % item for item in features[:10]], sep='\n')


# %% plot decision surface of feature pairs
matplotlib.rcParams.update({'font.size': 16})
fig, axs = plt.subplots(ncols=3, figsize=(12, 8))

plot_idx = 0
Ypred_full = clf.predict(predictors)
for pair in ([0, 1], [0, 2], [1, 2]):
    nutrient_x = features[pair[0]][1]
    nutrient_y = features[pair[1]][1]
    X = predictors.loc[:, nutrients['id'].loc[nutrients['name'] == nutrient_x]].as_matrix()
    Y = predictors.loc[:, nutrients['id'].loc[nutrients['name'] == nutrient_y]].as_matrix()

    plt.subplot(1, 3, plot_idx+1)
    plt.scatter(X[Ypred_full == 0]+1, Y[Ypred_full == 0]+1, color='r')
    plt.scatter(X[Ypred_full == 1]+1, Y[Ypred_full == 1]+1, color='k')
    axs[plot_idx].set_xscale('log')
    axs[plot_idx].set_yscale('log')
    # axs[plot_idx].set_xlim((-1, 6))
    # axs[plot_idx].set_ylim((-1, 6))
    plot_idx += 1

plt.axis("tight")
plt.show()
