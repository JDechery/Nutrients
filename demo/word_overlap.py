import pandas as pd
import Nutrients.utils as utl
import itertools
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


# %% load food names and collect wordcounts
foods = utl.load_sql_table('food')
food_names = foods['name'].values
words_infood = utl.split_into_words(food_names)
all_words = map(str.lower, list(itertools.chain(*words_infood)))
wordcounts = pd.Series(all_words).value_counts()
unfun_words = ['upc', 's', 'with', 'and', 'in', 'a', 'gtin', 'to']  # hand selected words to ignore due to lack of fun
wordcounts.drop(unfun_words, inplace=True)

# %% wordcount distribution
matplotlib.rcParams.update({'font.size': 16})
fig, ax = plt.subplots(figsize=(12, 8))
wordcounts.hist(bins=20)
ax.set_yscale('log')
ax.set_xlabel('word counts')
ax.set_ylabel('occurences')
plt.show()

# %%
nwords = 150
word_df = utl.get_word_count_df(nwords)

word_similarity = 1 - cdist(word_df.T, word_df.T, metric='jaccard')
np.fill_diagonal(word_similarity, 0)
# %% plot distribution
fig, ax = plt.subplots(figsize=(12, 8))
plt.hist(np.ravel(word_similarity), bins=20)
ax.set_yscale('log')
ax.set_xlabel('jaccardian overlap between foodname words')
ax.set_ylabel('occurences')
plt.show()
# %% explore anecdotes
word_overlap = list(zip(word_similarity[word_similarity != 0], np.argwhere(word_similarity != 0)))
word_overlap = sorted(word_overlap, key=lambda x: x[0])  # better to use operator.itemgetter?
word_overlap = word_overlap[0::2]  # similarity matrix is symmetric
# TODO improve readability
uncommon_wordpair = word_df.columns[word_overlap[0][1]]
uncommon_ndbno = word_df[word_df[uncommon_wordpair].all(axis=1)].index
uncommon_ndbno = list(uncommon_ndbno.values)
common_wordpair = word_df.columns[word_overlap[-2][1]]
common_ndbno = word_df[word_df[common_wordpair].all(axis=1)].index
common_ndbno = list(common_ndbno.values)

print('Percent of word pairs co-occuring = {}'.format(len(word_overlap) / (len(word_similarity)**2/2-len(word_similarity))))
print('Uncommon pairing: {} + {}'.format(*uncommon_wordpair))
print(foods.loc[foods.ndbno == uncommon_ndbno[0]]['name'].values)
print('Common pairing: {} + {}'.format(*common_wordpair))
print(foods.loc[foods.ndbno == common_ndbno[0]]['name'].values)
