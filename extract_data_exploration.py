"""sql joins and data cleaning for analysis."""
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

dbfile = 'F:/Data/nutrients_database.sqlite'
conn = sqlite3.connect(dbfile)

quantities = pd.read_sql_query('SELECT * from quantity', conn)
foods = pd.read_sql_query('SELECT * from food', conn)
nutrients = pd.read_sql_query('SELECT * from nutrient', conn)
nutrients.loc[nutrients['id'].isin([204,207])]['name']

def nutrient_name(nutrient_id, nutrient_df):
    name = nutrient_df.loc[nutrients['id'].isin(nutrient_id)]['name']
    return name

def food_name(ndbno, food_df):
    name = food_df.loc[food['ndbno'].isin(nutrient_id)]['name']
    return name

num_items = quantities.groupby('nutrient_id')['id'].count()
num_items.plot.hist(bins=50)
# most nutrients are very sparse; only a few are ubiquitous
common_nutrients = num_items.loc[num_items > 1e4]
nutrient_names = pd.read_sql_query('SELECT * from nutrient',conn)
common_nutrients = pd.DataFrame(common_nutrients).merge(nutrient_names, left_index=True, right_on='id', how='left')
common_nutrients = common_nutrients.drop('id_y', axis=1).rename(columns={'id_x': 'counts'}).set_index('id')

diffunits = quantities['units'].loc[quantities['nutrient_id']==255].unique()
diffunits = quantities.groupby('nutrient_id')['units'].nunique()
(diffunits==1).all()
# each nutrient is reported with consistent units (thankfully). no conversion necessary

pivotdf = quantities.pivot(index='ndbno', columns='nutrient_id', value='value')
