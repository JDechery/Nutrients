import pandas as pd
import Nutrients.utils as utl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn

# %%
nutrients = utl.load_sql_table('nutrient')
nutrients['id'] = nutrients['id'].astype('int64')
quantities = utl.load_sql_table('quantity')
qty = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)

qty_cov = qty.cov(min_periods=50).fillna(0).as_matrix()
cov_norm = np.log10(1+np.abs(qty_cov)) * np.sign(qty_cov)  # normalize for visualization
# %%
matplotlib.rcParams.update({'font.size': 16})
# fig, ax = plt.subplots(figsize=(12, 8))
# seaborn.heatmap(np.log10(np.abs(qty_cov+1)) * np.sign(qty_cov), ax=ax)
# plt.show()
fig, ax = plt.subplots(figsize=(12, 8))
offdiag = 1-np.eye(len(cov_norm))
var, vbin = np.histogram(np.diag(cov_norm), bins=25)
width = 0.7 * (vbin[1] - vbin[0])
center = (vbin[:-1] + vbin[1:]) / 2
plt.bar(center, var/sum(var), align='center', width=width, alpha=.5)
cvar, cvbin = np.histogram(cov_norm[offdiag.astype('bool')], bins=25)
width = 0.7 * (cvbin[1] - cvbin[0])
center = (cvbin[:-1] + cvbin[1:]) / 2
plt.bar(center, cvar/sum(cvar), align='center', width=width, alpha=.5)
ax.set_yscale('log')
plt.show()

# %% anecdotes

cov_norm[~offdiag.astype('bool')] = 0
covinds = np.argsort(np.ravel(cov_norm))
covsubs = [np.unravel_index(idx, cov_norm.shape) for idx in covinds]
covsubs = covsubs[::2]

print('Largest negative covariances:')
for subs in covsubs[:5]:
    print(cov_norm[subs], nutrients.iloc[list(subs)]['name'].values)
print('Largest positive covariances:')
for subs in covsubs[-5:]:
    print(cov_norm[subs], nutrients.iloc[list(subs)]['name'].values)
