import numpy as np
import pandas as pd
import random
import time

nfl_df = pd.read_csv("nfl_gamelogs_2015-2024real.csv")
# veg_df = pd.read_csv('nfl_vegas_lines_2015-2024.csv')
veg_df = pd.read_csv('nfl_vegas_lines_2015-2016.csv')

# check 
print(nfl_df.shape)
print(veg_df.shape)

# MERGE
merged_df = pd.merge(nfl_df, veg_df, on=['Season', 'Team', 'Gtm'])

print(merged_df.shape)