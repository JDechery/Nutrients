import pandas as pd
import sqlite3
import re
import itertools

def load_sql_table(tablename):
    """Load table from nutrients sql database."""
    dbfile = 'F:/Data/nutrients_database.sqlite'
    conn = sqlite3.connect(dbfile)
    query = 'SELECT * from ' + tablename
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def split_into_words(phrases):
    """Split food name into list of words."""
    matchString = '[^\W\d]*'
    words = [list(filter(None, re.findall(matchString, name))) for name in phrases]
    return words


def get_word_count_df(nwords=50):
    """Get binary word in foodname df."""
    foods = load_sql_table('food')
    food_names = foods['name'].values
    words_infood = split_into_words(food_names)
    all_words = map(str.lower, list(itertools.chain(*words_infood)))
    wordcounts = pd.Series(all_words).value_counts()
    unfun_words = ['upc', 's', 'with', 'and', 'in', 'a', 'gtin', 'to']  # hand selected words to ignore due to lack of fun
    wordcounts.drop(unfun_words, inplace=True)
    most_common_words = wordcounts[:nwords].index.unique()
    # TODO use sklearn CountVectorizer
    present = {}
    for item in words_infood:
        foodwords = list(map(str.lower, item))
        for word in most_common_words:
            if word not in present:
                present[word] = []
            if word in foodwords:
                present[word].append(1)
            else:
                present[word].append(0)
    return pd.DataFrame(data=present, index=foods['ndbno'])


def get_wordtargets_nutrientpredictors(nwords=50):
    quantities = load_sql_table('quantity')
    nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
    word_counts = get_word_count_df(nwords)
    combined_data = nutrient_amount.join(word_counts, how='left')
    targets = combined_data[word_counts.columns]
    predictors = combined_data[nutrient_amount.columns]
    return targets, predictors

# def get_joined_df():
#     """Lorem ipsum."""
#     quantities = load_sql_table('quantity')
#     nutrients = load_sql_table('nutrient')
#     foods = load_sql_table('food')
#
#     nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
#     combined_data = nutrient_amount.join(word_counts, how='left')
#     return combined_data
