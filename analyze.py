import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportion_confint
import matplotlib.pyplot as plt
from distfit import distfit
import glob
import statistics as stat

glued_data = pd.DataFrame()
for file_name in glob.glob('new_games/wk14/'+'*.csv'):
    x = pd.read_csv(file_name, low_memory=False)
    glued_data = pd.concat([glued_data,x],axis=0)

new_games = pd.read_csv('new_espn_probs.csv') 
new_games['prob_home_win'] = np.nan
new_games['home_mean'] = np.nan
new_games['home_std'] = np.nan
new_games['away_mean'] = np.nan
new_games['away_std'] = np.nan
new_games['pred_spread'] = np.nan
new_games['prob_home_cover'] = np.nan

for home in glued_data.home_team.unique():
    A_scores = glued_data.loc[glued_data.home_team == home, 'home_score'].to_numpy().tolist()
    B_scores = glued_data.loc[glued_data.home_team == home, 'away_score'].to_numpy().tolist()
    A_wins = np.where(np.array(A_scores) > np.array(B_scores), 1, np.where(np.array(A_scores) < np.array(B_scores), 0, 0.5)).tolist()

    home_scores = A_scores
    away_scores = B_scores
    diff_scores = np.array(B_scores) - np.array(A_scores)

    new_games.loc[new_games['home_team'] == home, 'pred_spread'] = np.median(diff_scores)
    new_games.loc[new_games['home_team'] == home, 'prob_home_win'] = np.mean(A_wins)
    new_games.loc[new_games['home_team'] == home, 'prob_home_win_lower'] = proportion_confint(sum(A_wins), len(A_wins))[0]
    new_games.loc[new_games['home_team'] == home, 'prob_home_win_upper'] = proportion_confint(sum(A_wins), len(A_wins))[1]
    new_games.loc[new_games['home_team'] == home, 'home_mean'] = np.mean(home_scores)
    new_games.loc[new_games['home_team'] == home, 'home_std'] = np.std(home_scores)
    new_games.loc[new_games['home_team'] == home, 'away_mean'] = np.mean(away_scores)
    new_games.loc[new_games['home_team'] == home, 'away_std'] = np.std(away_scores)
    new_games.loc[new_games['home_team'] == home, 'prob_home_cover'] = np.mean(diff_scores < new_games.loc[new_games['home_team'] == home, 'spread'].iloc[0])
    new_games.loc[new_games['home_team'] == home, 'prob_home_cover_lower'] = proportion_confint(np.sum(diff_scores < new_games.loc[new_games['home_team'] == home, 'spread'].iloc[0]), len(A_wins))[0]
    new_games.loc[new_games['home_team'] == home, 'prob_home_cover_upper'] = proportion_confint(np.sum(diff_scores < new_games.loc[new_games['home_team'] == home, 'spread'].iloc[0]), len(A_wins))[1]
    new_games['pick'] = np.where(new_games['pred_spread'] > new_games['spread'], new_games['away_team'], new_games['home_team'])
    new_games['difference'] = abs(new_games['spread'] - new_games['pred_spread'])

new_games.loc[~new_games.pred_spread.isna(), ['away_team', 'home_team', 'spread', 'pred_spread', 'difference', 'prob_home_win_lower','prob_home_win','prob_home_win_upper', 'prob_home_cover_lower', 'prob_home_cover', 'prob_home_cover_upper', 'pick']].to_excel('week14.xlsx',index=False)

A_scores = glued_data.loc[glued_data.home_team == 'Kent State', 'home_score'].to_numpy().tolist()
B_scores = glued_data.loc[glued_data.home_team == 'Kent State', 'away_score'].to_numpy().tolist()
A_wins = np.where(np.array(A_scores) > np.array(B_scores), 1, np.where(np.array(A_scores) < np.array(B_scores), 0, 0.5))

-(5*(200000*np.log(-stat.mean(A_wins)/(stat.mean(A_wins)-1))+ 16519))/123143
-(5*(200000*np.log(-0.894/(0.894-1))+ 16519))/123143
stat.mean(B_scores) - stat.mean(A_scores)
differences = np.array(B_scores) - np.array(A_scores)
np.mean(differences < -17.5)

np.mean(np.array(A_scores) > 40)

spread_check = np.where(differences < -15.5, 1, 0)
proportion_confint(sum(spread_check), len(A_wins))

proportion_confint(sum(A_wins), len(A_wins))

# Initialize
dist_A = distfit()
dist_B = distfit()

# Search for best theoretical fit on your emperical data
dist_A.fit_transform(np.array(A_scores))
dist_B.fit_transform(np.array(B_scores))

home_scores = dist_A.generate(10000000)
away_scores = dist_B.generate(10000000)
diff_scores = away_scores - home_scores

np.mean(diff_scores)
np.mean(diff_scores > 0)
proportion_confint(sum(diff_scores < 0), len(diff_scores))