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
        url = 'https://www.pro-football-reference.com/teams/'+ team + '/' + str(season) + '_lines.htm'
        count+=1
        print(f"{url}, {count} teams have been iterated.")

        # get vegas lines (frm 'vegas_lines' table)
        lines_df = pd.read_html(url, header=0, attrs={'id':'vegas_lines'})[0]

        # insert szn and tm cols
        lines_df.insert(loc=0, column='Season', value = season)
        lines_df.insert(loc=1, column='Team', value = team.upper())

        # concat team lines datafram to aggregate df (along rows)
        veg_df = pd.concat([veg_df, lines_df], ignore_index=True)

        time.sleep(random.randint(4,5))

end_time = time.time()

elapsed_time = end_time - start_time
print(f'Elapsed Time:  {elapsed_time} seconds')

print(veg_df.info())
