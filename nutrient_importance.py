import pandas as pd
import Nutrients.utils as utl
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

targets, predictors = utl.get_wordtargets_nutrientpredictors(nwords=25)
with open('F:/Data/forest_results.pkl', 'rb') as f:
    forest_clf = pickle.load(f)

# %%
test_scores = {}
for key, val in forest_clf.items():
    # test_scores.append((key, max(val[0]['mean_test_score'])))
    # best_result_idx
    test_scores[key] = max(val[0]['mean_test_score'])

test_scores = pd.concat([targets.mean(), pd.Series(test_scores)], axis=1)
test_scores.columns = ['term_prob', 'test_score']
test_scores.dropna(inplace=True)
# test_scores = sorted(test_scores, key=lambda x: x[1], reverse=True)

# %%
sns.pairplot(test_scores)
plt.show()

# %%
df = pd.concat([pd.DataFrame(data=[clf[1].feature_importances_], index=[food]) for food, clf in forest_clf.items()])
nut_importance = []
foodnames = []
for food, clf in forest_clf.items():
    nut_importance.append(clf[1].feature_importances_)
nut_importance = np.asarray(nut_importance)

# %%
fig, ax = plt.subplots(figsize=(16, 8))
sns.heatmap(df.apply(lambda x: x/max(x), axis=1), ax=ax)
sns.heatmap(df, ax=ax)
for item in ax.get_xticklabels():
    item.set_rotation(90)
plt.show()
