import pandas as pd
import Nutrients.utils as utl
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib
from sklearn.model_selection import StratifiedShuffleSplit
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
best_results = best_results.sort_values(by='mean_score', ascending=False)

# %% plot
matplotlib.rcParams.update({'font.size': 14})
fig, axs = plt.subplots(ncols=3, figsize=(12, 6))

plt.sca(axs[0])
plt.hist(best_results['mean_score'], bins=20)
plt.xlabel('f1 score of best forest')
plt.ylabel('# words')
plt.title('all words')

plt.sca(axs[1])
top_results = best_results.iloc[:25, :]
plt.scatter(top_results.term_prob, top_results.mean_score, alpha=.8)
np.random.seed(123456)
text_positions = [(x+np.random.randn()*.002, y+np.random.randn()*.002) for x, y in zip(top_results.term_prob, top_results.mean_score)]
[plt.text(pt[0], pt[1], txt, fontsize=12) for pt, txt in zip(text_positions, top_results.index)]
plt.xlabel('word probability')
plt.ylabel('best forest f1 score')
plt.title('best words')

plt.sca(axs[2])
bot_results = best_results.iloc[-25:, :]
plt.scatter(bot_results.term_prob, bot_results.mean_score, alpha=.8)
text_positions = [(x+np.random.randn()*.002, y+np.random.randn()*.002) for x, y in zip(bot_results.term_prob, bot_results.mean_score)]
[plt.text(pt[0], pt[1], txt, fontsize=12) for pt, txt in zip(text_positions, bot_results.index)]
plt.xlabel('word probability')
plt.ylabel('best forest f1 score')
plt.title('worst words')

plt.subplots_adjust(wspace=.4)
plt.show()

# %% param results
results = {}
for key, val in forest_clf.items():
    pars = [tuple(el.values()) for el in val[0]['params']]
    results[key] = val[0]['mean_test_score']
pars = [list(map(str, p)) for p in pars]
results = pd.DataFrame.from_dict(results, orient='index')
results.columns = pd.MultiIndex.from_tuples(pars, names=['max_features', 'n_estimators'])

results = results.div(results.max(axis=1), axis=0)

fig, ax = plt.subplots(figsize=(9, 6))
results.boxplot(rot=90, showfliers=False)
plt.grid(False)
plt.title('forest parameters scores')
plt.ylabel('mean score (relative to best)')
plt.xlabel('parameters (max_features, n_estimators)')
plt.show()

# %% best performing forest
example_word = 'lean'
clf = forest_clf[example_word][1]
train_ind, test_ind = tuple(StratifiedShuffleSplit(n_splits=1).split(predictors, targets[example_word]))[0]
Xtrain, Xtest, ytrain, ytest = predictors.iloc[train_ind, :],         \
                               predictors.iloc[test_ind, :],          \
                               targets[example_word].iloc[train_ind], \
                               targets[example_word].iloc[test_ind]
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)
print('test-data confusion matrix')
print(confusion_matrix(ytest, ypred))

features = list(zip(clf.feature_importances_, nutrients['name']))
features = sorted(features, key=lambda x: x[0], reverse=True)
print('10 ten predictive nutrients for ' + example_word.join('\''*2))
print(*['%0.3f, %s' % item for item in features[:10]], sep='\n')


# %% plot top 3 nutrient pairs
matplotlib.rcParams.update({'font.size': 16})
fig, axs = plt.subplots(ncols=3, figsize=(12, 6))

plot_idx = 0
Ypred_full = clf.predict(predictors)
for pair in ([0, 1], [0, 2], [1, 2]):
    nutrient_x = features[pair[0]][1]
    nutrient_y = features[pair[1]][1]
    X = predictors.loc[:, nutrients['id'].loc[nutrients['name'] == nutrient_x]].as_matrix()
    Y = predictors.loc[:, nutrients['id'].loc[nutrients['name'] == nutrient_y]].as_matrix()

    plt.sca(axs[plot_idx])
    axs[plot_idx].set_xlabel(nutrient_x)
    axs[plot_idx].set_ylabel(nutrient_y)
    plt.scatter(X[Ypred_full == 0], Y[Ypred_full == 0], color='r', alpha=.1)
    plt.scatter(X[Ypred_full == 1], Y[Ypred_full == 1], color='k', alpha=.1)
    plot_idx += 1

for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
plt.show()
