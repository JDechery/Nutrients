import Nutrients.utils as utl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# %%
nutrients = utl.load_sql_table('nutrient')
nutrients['id'] = nutrients['id'].astype('int64')
quantities = utl.load_sql_table('quantity')
qty = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)

qty_cov = qty.cov(min_periods=50).fillna(0).as_matrix()
cov_norm = np.log10(1+np.abs(qty_cov)) * np.sign(qty_cov)  # normalize for visualization
# %%
matplotlib.rcParams.update({'font.size': 16})
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
# plt.show()

# %% correlation matrix
fig, ax = plt.subplots(figsize=(10, 10))
np.seterr(all='ignore')
corr = np.corrcoef(qty.T.fillna(0))
bad_cols = np.where(sum(np.isnan(corr)) == len(corr))
corr = np.delete(corr, bad_cols, axis=0)
corr = np.delete(corr, bad_cols, axis=1)
sns.heatmap(corr)
ax.set_title('nutrient pearson correlation')
plt.axis('tight')
plt.show()
