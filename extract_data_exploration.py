"""sql joins and data cleaning for analysis."""
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn import decomposition
from pprint import pprint

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)

quantities = pd.read_sql_query('SELECT * from quantity', conn)
foods = pd.read_sql_query('SELECT * from food', conn)
nutrients = pd.read_sql_query('SELECT * from nutrient', conn)

pivotdf = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)


def nutrient_name2id(names, nutrient_df=nutrients):
    ids = nutrient_df.loc[nutrient_df['name'].isin(names)]['id'].values
    return ids


def nutrient_id2name(nutrient_id, nutrient_df=nutrients):
    name = nutrient_df.loc[nutrients['id'].isin(nutrient_id)]['name'].values
    return name


def food_id2name(ndbno, food_df=foods):
    name = food_df.loc[food_df['ndbno'].isin(ndbno)]['name'].values
    return name


def food_name2id(names, food_df=foods):
    ids = food_df.loc[food_df['name'].isin(names)]['ndbno'].values
    return ids


waterid = nutrient_name2id(['Water']).values
amount_water = pivotdf[waterid]
amount_water = amount_water[amount_water[waterid] != 0]
# amount_water.hist(bins=20)
dryfoods = amount_water[(amount_water[waterid] < 10.) & (amount_water[waterid] > 0.)].dropna()
dryfoodnames = food_id2name(dryfoods.index)
pprint(dryfoodnames)

num_items = quantities.groupby('nutrient_id')['id'].count()
num_items.plot.hist(bins=50)
# most nutrients are very sparse; only a few are ubiquitous
common_nutrients = num_items.loc[num_items > 1e4]
nutrient_names = pd.read_sql_query('SELECT * from nutrient', conn)
common_nutrients = pd.DataFrame(common_nutrients).merge(nutrient_names, left_index=True, right_on='id', how='left')
common_nutrients = common_nutrients.drop('id_y', axis=1).rename(columns={'id_x': 'counts'}).set_index('id')

diffunits = quantities['units'].loc[quantities['nutrient_id'] == 255].unique()
diffunits = quantities.groupby('nutrient_id')['units'].nunique()
(diffunits == 1).all()
# each nutrient is reported with consistent units (thankfully). no conversion necessary

# num_unreported = pivotdf.isnull().mean().plot('hist', bins=50)
cols = pivotdf.columns
nrow, ncol = pivotdf.shape
numempty = (pivotdf == 0).sum(axis=0)
fullcols = cols[numempty < nrow*.5]
sparsedf = pivotdf[[col for col in fullcols]]


X = pivotdf.copy()
svd_transform = decomposition.PCA(n_components=25, random_state=123456).fit(X)
svd_transform.components_.shape
plt.imshow(svd_transform.components_[:10, :], cmap='hot')
plt.show()
Xsparse = svd_transform.transform(X)
# method = manifold.TSNE(n_components=2, perplexity=30, init='pca', random_state=123456, n_iter_without_progress=10, verbose=1)
method = manifold.LocallyLinearEmbedding(n_neighbors=5, n_components=2, max_iter=1, eigen_solver='dense', random_state=123456)
Y = method.fit_transform(Xsparse)
fig, ax = plt.subplots()
ax.scatter(Y[:, 0], Y[:, 1])
plt.show()

Y = decomposition.PCA().fit(X)
pprint(Y.explained_variance_ratio_)
