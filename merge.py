import numpy as np
import pandas as pd
import random
import time

nfl_df = pd.read_csv("nfl_gamelogs_2015-2024real.csv")
veg_df = pd.read_csv('nfl_vegas_lines_2015-2024real.csv')


# check 
print(nfl_df.shape)
print(veg_df.shape)

# MERGE
merged_df = pd.merge(nfl_df, veg_df, on=['Season', 'Team', 'Gtm'])

print(merged_df.shape)

# cover column --> 1 = covered, 0 = not covered/push
merged_df['Cover'] = np.where(merged_df['Tm_Pts']+ merged_df['Spread'] > merged_df['Opp_Pts'], 1, 0)

# over col --> 1 = over, 0 = under/push
merged_df['Over'] = np.where(merged_df['Tm_Pts'] + merged_df['Opp_Pts'] > merged_df['Total'], 1, 0)
nfl_df = nfl_df.rename(columns={"Opp_x":'Opp'})
print(merged_df.info())

# test example
# print(merged_df.query('Season == 2024 and Team == "SFO"'))

merged_df.to_csv('nfl_gamelog_vegas_2015-2024real.csv', index=False)
