import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn

with open('F:/Data/forest_results.pkl', 'rb') as f:
    forest_clf = pickle.load(f)
# %%
df = pd.concat([pd.DataFrame(data=[clf[1].feature_importances_], index=[food]) for food, clf in forest_clf.items()])
# nut_importance = []
# foodnames = []
# for food, clf in forest_clf.items():
#     nut_importance.append(clf[1].feature_importances_)
# nut_importance = np.asarray(nut_importance)
# %%
fig, ax = plt.subplots(figsize=(16, 8))
# seaborn.heatmap(df.apply(lambda x: x/max(x), axis=1), ax=ax)
seaborn.heatmap(df, ax=ax)
for item in ax.get_xticklabels():
    item.set_rotation(90)
plt.show()
