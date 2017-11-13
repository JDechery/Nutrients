import pandas as pd
import Nutrients.utils as utl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# _, nutrients = utl.get_wordtargets_nutrientpredictors(nwords=0)
quantity = utl.load_sql_table('quantity')
nutrients = utl.load_sql_table('nutrient')


# %%
matplotlib.rcParams.update({'font.size': 16})
fig, axs = plt.subplots(nrows=3, figsize=(12, 8))
