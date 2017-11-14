import pandas as pd
import Nutrients.utils as utl
import numpy as np
import scipy
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

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


# %%
def get_nutrient_stats(group):
    column_p = group.apply(lambda x: np.mean(x > 0))
    column_var = group.apply(lambda x: np.var(x[x > 0]))
    # return {'var': group.var().mean(),
    #         'entropy': np.mean([scipy.stats.entropy([p, 1-p]) for p in column_p]),
    #         'nonzero_var': np.mean(column_var)}
    return [group.var().mean(), np.mean([scipy.stats.entropy([p, 1-p]) for p in column_p]), np.mean(column_var)]


nutrient_stats = {}
for word in targets.columns:
    stats = predictors.groupby(targets[word]).apply(get_nutrient_stats)
    nutrient_stats[word] = [x-y for x, y in zip(stats[1], stats[0])]
# %%
stat_df = pd.concat([pd.DataFrame.from_dict(nutrient_stats, orient='index'), best_results['mean_score']], axis=1)
stat_df.dropna(inplace=True)
stat_df.columns = ['var', 'entropy', 'nonzero_var', 'mean_score']
# stat_df['var'] = stat_df['var'].apply(lambda x: np.log10(np.abs(x)+1) * np.sign(x))
# stat_df['nonzero_var'] = stat_df['nonzero_var'].apply(lambda x: np.log10(np.abs(x)+1) * np.sign(x))
# %%
sns.pairplot(stat_df)
plt.show()
