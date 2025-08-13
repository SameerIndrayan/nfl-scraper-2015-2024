#libraries
import numpy as np
import pandas as pd
import random
import time

teams = [
    "crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb","htx", "clt", "jax", "kan", "sdg", "ram", "rai", "mia", "min", "nwe", "nor", 'nyg', 'nyj', "phi", 'pit', 'sea', 'sfo', 'tam', 'oti', 'was'
]

print(f'number of teams = {len(teams)}')

#renaming cols so no repeats
rename_dict = {
    'Unnamed: 5': 'Home', 'Rslt':'Win', "Pts":'Tm_Pts', 'PtsO': 'Opp_Pts', 'Cmp': 'pCmp', 'Att':'pAtt', 'Cmp%':'pCmp%', 'Yds':'pYds', 'TD':'pTD', 'Y/A':'pY/A', 'AY/A':'pAY/A', 'Rate': 'pRate', 'Yds.1':'SkYds', "Att.1":'rAtt', 'Yds.2':"rYds", 'TD.1':'rTD', 'Y/A.1':'rY/A', 'Yds.3':'PntYds', 'Pass':'fdPass', 'Rsh':'fdRush', 'Pen':"fdPen", 'Pen.1':'Pen', 'Yds.4':'PenYds'
}

#SCRAPE NFL GAMELOG DATA

#get starting time
start_time = time.time()

#range of szns to use
seasons = range(2015, 2025) # goes up 1 less than 2025

#empty dataframe to dump all team and opponent data
nfl_df = pd.DataFrame()
count = 0

#iterate thru szns
for season in seasons:
    #iterate thru teams
    for team in teams:
        #set URL
        url = 'https://www.pro-football-reference.com/teams/'+ team + '/' + str(season) + '/gamelog/'
        count+=1
        print(f"{url}, {count} teams have been iterated.")
        #from 2015 to 2024, there were 5246 games. 32 teams x 16 games for 2015 to 2020 + 32 teams x 17 games for 2021 to 2024 = 5248 games but Damar Hamlin injury so -2 --> 5246
        # SCRAPING TM STATS

        # Get team stats from game logs table
        table_id = 'table_pfr_team-year_game-logs_team-year-regular-season-game-log'
        tm_df = pd.read_html(url, header=1, attrs={'id':table_id})[0]

        #drop rows with rank (rk) value is Nan and rename some cols
        tm_df = tm_df.dropna(subset=['Rk'])
        tm_df = tm_df.rename(rename_dict, axis =1)

        #adding 'Tm_' prefix to game stats to know which is which
        pre_dict = {col:f'Tm_{col}' for col in tm_df.columns[11:1]}
        tm_df = tm_df.rename(columns=pre_dict)

        # SCRAPING OPP STATS
        table_id = 'table_pfr_team-year_game-logs_team-year-regular-season-opponent-game-log'
        opp_df = pd.read_html(url, header=1, attrs={'id':table_id})[0]

        #drop rows with rank (rk) value is Nan and rename some cols
        opp_df = opp_df.dropna(subset=['Rk'])
        opp_df = opp_df.rename(rename_dict, axis =1)

        #adding 'Tm_' prefix to game stats to know which is which
        pre_dict = {col:f'Tm_{col}' for col in tm_df.columns[11:1]}
        opp_df = opp_df.rename(columns=pre_dict)

        # COMBINING TM AND OPP DF
        cols_to_merge = tm_df.columns[:11].tolist() #making cols to merge

        merged_df = pd.merge(tm_df, opp_df, on=cols_to_merge) # team data and opp data in each row

        # insert szn and tm as new cols
        merged_df.insert(loc=0, column='Season', value=season)
        merged_df.insert(loc=1, column='Team', value=team.upper())

        # ADD TO NFL_DF (aggregate data frame)
        nfl_df = pd.concat([nfl_df, merged_df], ignore_index=True) #concat team gamelog to agg df

        # CLEANING UP DATA
        # dropping Rk column
        nfl_df = nfl_df.drop(columns=['Rk'], axis =1)

        # Home, Win, and OT cols to binary
        nfl_df['Home']= np.where(nfl_df['Home'] == '@', 0, 1)
        nfl_df['Win']= np.where(nfl_df['Home'] == 'W', 1, 0)
        nfl_df['OT']= np.where(nfl_df['OT'] == 'OT', 1, 0)

        time.sleep(random.randint(4,5)) # have to have at least 3 sec delay according to website rules

end_time = time.time()

print(f'Elapsed time: {end_time - start_time:1f} seconds')

print(nfl_df.info())

nfl_df.to_csv('nfl_gamelogs_2015-2024.csv', index=False)






