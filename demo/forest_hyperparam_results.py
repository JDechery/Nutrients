import pandas as pd
import Nutrients.utils as utl
import pickle
import matplotlib.pyplot as plt
import matplotlib
from itertools import chain

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=20)

with open('F:/Data/forest_results_20171113.pkl', 'rb') as f:
    forest_clf = pickle.load(f)


def extract_score(result_val):
    scores = [val[0]['mean_test_score'] for val in result_val]
    param = [val[0]['params'] for val in result_val]
    return param, scores


param_names = ['max_depth', 'min_samples_leaf', 'max_leaf_nodes']
# %%
results = {}
for key, val in forest_clf.items():
    params, results[key] = extract_score(val)
    results[key] = chain(*results[key])
params = list(chain(*params))
params = list(chain(*[[list(map(str, (k, v))) for k, v in p.items()] for p in params]))

results = pd.DataFrame.from_dict(results, orient='index')
results.columns = pd.MultiIndex.from_tuples(params, names=['params', 'count'])

# %%
matplotlib.rcParams.update({'font.size': 16})
fig, axs = plt.subplots(nrows=3, figsize=(12, 8))
plt.suptitle('random forest hyperparameter scores')
raw_plot = pd.concat([results.mean(), results.std()], axis=1)
norm_plot = results.div(results.max(axis=1), axis=0)
norm_plot = pd.concat([norm_plot.mean(), norm_plot.std()], axis=1)
for ii, param in enumerate(results.columns.levels[0]):
    npt = raw_plot.loc[param].shape[0]
    raw_plot.loc[param][0].plot(x=range(npt), yerr=raw_plot.loc[param][1], ax=axs[ii])
    norm_plot.loc[param][0].plot(yerr=norm_plot.loc[param][1], ax=axs[ii])
    axs[ii].set_xlabel(param)
    axs[ii].set_xticks(range(npt))
    axs[ii].set_xticklabels(list(raw_plot.loc[param].index))
    axs[ii].set_xlim((-.5, 5.5))
    axs[ii].set_ylim((0, 1))

axs[0].legend(['score', 'normalized'], frameon=False)
axs[1].set_xlabel('mean f1 score')
plt.subplots_adjust(hspace=.45, left=.25, right=.85)
plt.show()
