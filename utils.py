import pandas as pd
import sqlite3
import re


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


# def get_joined_df():
#     """Lorem ipsum."""
#     quantities = load_sql_table('quantity')
#     nutrients = load_sql_table('nutrient')
#     foods = load_sql_table('food')
#
#     nutrient_amount = quantities.pivot_table(index='food_id', columns='nutrient_id', values='value', fill_value=0)
#     combined_data = nutrient_amount.join(wordPresence, how='left')
#     return combined_data
