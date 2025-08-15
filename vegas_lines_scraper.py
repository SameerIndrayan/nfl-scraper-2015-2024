import numpy as np
import pandas as pd
import random
import time
teams = [
    "crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb","htx", "clt", "jax", "kan", "sdg", "ram", "rai", "mia", "min", "nwe", "nor", 'nyg', 'nyj', "phi", 'pit', 'sea', 'sfo', 'tam', 'oti', 'was'
]

start_time = time.time()    

seasons = range(2015,2025)

veg_df = pd.DataFrame()
count = 0

for season in seasons:
    for team in teams:
        url = f'https://www.pro-football-reference.com/teams/{team}/{season}_lines.htm'
        count += 1
        print(f"{url}, {count} teams have been iterated.")

        lines_df = pd.read_html(url, header=0, attrs={'id': 'vegas_lines'})[0]

        # rename BEFORE concat
        lines_df = lines_df.rename(columns={'G#': 'Gtm', 'Over/Under': 'Total'})

        # insert season and team
        lines_df.insert(loc=0, column='Season', value=season)
        lines_df.insert(loc=1, column='Team', value=team.upper())

        # append to big df
        veg_df = pd.concat([veg_df, lines_df], ignore_index=True)

        time.sleep(random.randint(4, 5))

# filter once after loop
veg_df = veg_df.query('(Season <= 2020 and Gtm < 17) or (Season >= 2021 and Gtm < 18)')

print(veg_df.info())
veg_df.to_csv('nfl_vegas_lines_2015-2024.csv', index=False)
