import pandas as pd
import Nutrients.utils as utl
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=150)
nutrients = utl.load_sql_table('nutrient')
nutrients = nutrients.loc[nutrients['id'].isin(predictors.columns), :]

with open('F:/Data/forest_results_20171112.pkl', 'rb') as f:
    forest_clf = pickle.load(f)

# %% collect feature importances
feat_importance = {}
score = {}
for key, val in forest_clf.items():
    best_idx = val[0]['rank_test_score'][0]-1
    score[key] = val[0]['mean_test_score'][best_idx]
    feat_importance[key] = val[1].feature_importances_

feat_importance = pd.DataFrame(feat_importance)
score = pd.Series(score)

feat_importance = feat_importance.apply(lambda x: sorted(x, reverse=True))
# col_sorted = feat_importance.columns[feat_importance.iloc[0, :].argsort()]
col_sorted = feat_importance.columns[score.argsort()]
# %% plot rank importances
matplotlib.rcParams.update({'font.size': 14})
fig = plt.figure(figsize=(12, 9))
ax1 = fig.add_axes([.1, .65, .3, .3])
ax2 = fig.add_axes([.1, .2, .7, .35])
ax3 = fig.add_axes([.5, .65, .3, .3])
cax = fig.add_axes([.82, .2, .02, .75])
fig.suptitle('distribution of feature importances')

feat_importance[col_sorted].cumsum().plot(ax=ax1, cmap=matplotlib.cm.viridis, alpha=.5, legend=False, logx=True, logy=True)
ax1.set_ylim([10**-1.1, 10**0.1])
ax1.set_xlim([1, 10**2.2])
ax1.set_ylabel('c.sum feature importance')
ax1.set_xlabel('rank feature')

ax3.scatter(feat_importance.iloc[0, :], score, alpha=.5, c='k', edgecolors=None)
ax3.set_xlabel('max. importance')
ax3.set_ylabel('forest f1 score')
FI_norm = feat_importance[col_sorted].div(feat_importance[col_sorted].iloc[0, :])
FI_norm.plot(ax=ax2, cmap=matplotlib.cm.viridis, alpha=.5, legend=False, logx=True, logy=True)
ax2.set_ylim([10**-3, 10**1.2])
ax2.set_xlim([1, 10**2.2])
ax2.set_ylabel('importance (normalized)')
ax2.set_xlabel('rank feature')

cb = matplotlib.colorbar.ColorbarBase(cax, cmap=matplotlib.cm.viridis, ticks=[])
cb.set_label('classification performance (AU)')
plt.axis('tight')
plt.show()
