import pandas as pd
import Nutrients.utils as utl
import numpy as np
import pickle
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from itertools import combinations

targets, predictors = utl.get_ngramtargets_nutrientpredictors(mincount=250)
with open('F:/Data/forest_ngram_results_20171113.pkl', 'rb') as f:
    results = pickle.load(f)

results = pd.DataFrame(results)
zresult = results.apply(lambda x: (x-np.mean(x))/np.std(x)).T

# %%
plt.errorbar(range(zresult.shape[1]), zresult.mean(), yerr=zresult.std())
plt.show()
# %% correlation matrix
matplotlib.rcParams.update({'font.size': 14})
fig, ax = plt.subplots(figsize=(10, 10))
corr = np.corrcoef(zresult.T)
sns.heatmap(corr)
ax.set_title('nutrient pearson correlation')
plt.axis('tight')
plt.show()


# %% k-means clustering
nclust = [3, 5]
pairid = tuple(combinations([0, 1, 2], 2))
fig, ax = plt.subplots(nrows=len(pairid), ncols=len(nclust), figsize=(12, 9))
for colid, nc in enumerate(nclust):
    est = KMeans(n_clusters=nc)
    est.fit(zresult)
    labels = est.labels_

    for rowid, pair in enumerate(pairid):
        plt.sca(ax[rowid, colid])
        plt.scatter(zresult.iloc[:, pair[0]], zresult.iloc[:, [pair[1]]], c=labels.astype('float'))
        plt.xlabel(str(pair[0]))
        plt.ylabel(str(pair[1]))
plt.show()
