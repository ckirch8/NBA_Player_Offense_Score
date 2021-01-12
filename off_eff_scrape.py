import requests
import nba_api
from nba_api.stats.static import teams
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerdashboardbyyearoveryear, leaguedashptstats, boxscoreplayertrackv2, leaguegamelog, leaguedashplayerstats
import pandas as pd
import time

pt_stats = leaguedashptstats.LeagueDashPtStats(season='2019-20', pt_measure_type='Passing', player_or_team='Player',
                                                per_mode_simple='Totals')
time.sleep(.600)
pt_stats = pt_stats.get_data_frames()[0]

player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2019-20', per_mode_detailed='Totals')
time.sleep(.600)
player_stats = player_stats.get_data_frames()[0]


wanted_player = player_stats[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', 'AGE', 'GP', 'PTS', 'FGA', 'FTA', 'AST', 'TOV', 'OREB']]
wanted_pt = pt_stats[['PLAYER_ID', 'SECONDARY_AST', 'AST_PTS_CREATED', 'POTENTIAL_AST']]


data = pd.merge(wanted_player, wanted_pt, on='PLAYER_ID')
data['FT_AST'] = 0

IDs = data['PLAYER_ID'].to_list()
# IOE = int(AD['PTS'])/(int(AD['FGA']) + int(AD['TOV'] + .44*int(AD['FTA'])))
# print(IOE)
# print(AD)

# unknown = playerdashboardbyyearoveryear.PlayerDashboardByYearOverYear(player_id=2200, season='2019-20')
# unknown = unknown.get_data_frames()
# print(unknown)

games = leaguegamelog.LeagueGameLog(season='2019-20', season_type_all_star='Regular Season')
games = games.get_data_frames()[0]
games = pd.unique(games['GAME_ID'])
# print(games)
for game in games:
    score = boxscoreplayertrackv2.BoxScorePlayerTrackV2(game_id=game).get_data_frames()[0]
    time.sleep(.600)
    for i, row in score.iterrows():
        # print(row)
        # id = int(score.at[i, 'PLAYER_ID'])
        if(score.at[i, 'PLAYER_ID'] not in IDs):
            continue
        loc = IDs.index(score.at[i, 'PLAYER_ID'])
        ft_ast = score.at[i, 'FTAST']
        data.at[loc, 'FT_AST']+=ft_ast
    # print(score['FTAST'])

data['PGen'] = data['PTS'] + (df['AST_PTS_CREATED'] / (df['AST'] + df['FT_AST'])) * (data['AST'] + data['SECONDARY_AST'] + data['FT_AST'])
data['NPT'] = data['FGA'] + data['AST'] + data['SECONDARY_AST'] + data['FT_AST'] + data['TOV'] + .44*data['FTA'] - data['OREB']
data['NPTwAO'] = data['FGA'] + data['SECONDARY_AST'] + data['TOV'] + .44*data['FTA'] - data['OREB'] + data['POTENTIAL_AST']
data['PT'] = data['FGA'] + data['POTENTIAL_AST'] + data['SECONDARY_AST'] + data['FT_AST'] + .44*data['FTA']
data['SP'] = data['FGA'] + data['TOV'] + .44*data['FTA']
data['PP'] = data['SECONDARY_AST'] + data['FT_AST'] + data['TOV'] + data['POTENTIAL_AST']
data["STOV"] = ((data['FGA'] + .44*data['FTA']) / (data['PT'])) * data['TOV']
data["PTOV"] = ((data['SECONDARY_AST'] + data['FT_AST'] + data['POTENTIAL_AST']) / data['PT']) * data['TOV']
data["SP'"] = data['FGA'] + data['STOV'] + .44*data['FTA']
data["PP'"] = data['SECONDARY_AST'] + data['FT_AST'] + data['PTOV'] + data['POTENTIAL_AST']

data['PPG'] = data['PTS'] / data['GP']
data['APG'] = data['AST'] / data['GP']
data['PGen/G'] = data['PGen'] / data['GP']
data['PT/G'] = data['PT'] / data['GP']
data['NPT/G'] = data['NPT'] / data['GP']
data['NPTwAO/G'] = data['NPTwAO'] / data['GP']
data['SP/G'] = data['SP'] / data['GP']
data['PP/G'] = data['PP'] / data['GP']
data["SP'/G"] = data["SP'"] / data['GP']
data["PP'/G"] = data["PP'"] / data['GP']

data['IOE'] = data['PGen'] / data['NPT']
data['IOEwAO'] = data['PGen'] / data['NPTwAO']
data['ISE'] = data['PTS'] / data['SP']
data['IPE'] = (data['AST_PTS_CREATED'] / (data['AST'] + data['FT_AST'])) * (data['AST'] + data['SECONDARY_AST'] + data['FT_AST']) / (data['PP'])
data["ISE'"] = data['PTS'] / data["SP'"]
data["IPE'"] = (data['AST_PTS_CREATED'] / (data['AST'] + data['FT_AST'])) * (data['AST'] + data['SECONDARY_AST'] + data['FT_AST']) / (data["PP'"])

data['STOV'] = data['STOV'].apply('{:.3f}'.format)
data['PTOV'] = data['PTOV'].apply('{:.3f}'.format)

data['PPG'] = data['PPG'].apply('{:.1f}'.format)
data['APG'] = data['APG'].apply('{:.1f}'.format)

data['PGen/G'] = data['PGen/G'].apply('{:.2f}'.format)
data['PT/G'] = data['PT/G'].apply('{:.2f}'.format)
data['NPT/G'] = data['NPT/G'].apply('{:.2f}'.format)
data['NPTwAO/G'] = data['NPTwAO/G'].apply('{:.2f}'.format)
data['SP/G'] = data['SP/G'].apply('{:.2f}'.format)
data['PP/G'] = data['PP/G'].apply('{:.2f}'.format)
data["SP'/G"] = data["SP'/G"].apply('{:.2f}'.format)
data["PP'/G"] = data["PP'/G"].apply('{:.2f}'.format)

data['IOE'] = data['IOE'].apply('{:.3f}'.format)
data['IOEwAO'] = data['IOEwAO'].apply('{:.3f}'.format)
data['ISE'] = data['ISE'].apply('{:.3f}'.format)
data['IPE'] = data['IPE'].apply('{:.3f}'.format)
data["ISE'"] = data["ISE'"].apply('{:.3f}'.format)
data["IPE'"] = data["IPE'"].apply('{:.3f}'.format)

data.to_csv('offensive_efficiency.csv', index=False)
