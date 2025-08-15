import numpy as np
import pandas as pd
import random
import time

nfl_df = pd.read_csv('nfl_gamelog_vegas_2015-2024.csv')

# home favs
home_fav_df = nfl_df.query('Home == 1' and '-7.0 <= Spread <= -6.5')
home_fav_count = len(home_fav_df)

# wins from all home favs
home_win_df = home_fav_df.query('Win == 1')
home_win_count = len(home_win_df)

# percentage
# print(f'Win percentage for home teams favored from -7.0 to -6.5: {home_win_count / home_fav_count:.2%} ({home_win_count} of {home_fav_count})')
print(home_win_df.info())

# print(home_win_count)