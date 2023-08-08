from game_interaction import *
import statistics as stat
import pandas as pd 
import numpy as np


df = pd.read_csv('sim_df.csv')
df = df.astype({'punt_yds': float})
df['punt'] = df['punt'].fillna(0.0)
df['fumble'] = df['fumble'].fillna(0.0)
max_effective_time = 900
df['time_left'] = df['time_left'].apply(lambda x: max_effective_time if x > max_effective_time else x)

new_games = pd.read_csv('new_espn_probs.csv') 
#new_games = pd.read_csv('games_left.csv')
new_games['home_prob'] = np.nan
new_games['home_mean'] = np.nan
new_games['home_std'] = np.nan
new_games['away_mean'] = np.nan
new_games['away_std'] = np.nan
new_games['pred_spread'] = np.nan


for row in new_games.index:
    TEAM_A = new_games.loc[row, 'home_team']
    TEAM_B = new_games.loc[row, 'away_team']
    A_scores = []
    B_scores = []
    A_wins = []
    game = Game(TEAM_A, TEAM_B, df, print=False, max_effective_time=max_effective_time)

    for j in range(512):
        final_score = None
        for i in range(0, 201):
            is_game_ended = game.simulate_play()
            if is_game_ended:
                final_score = game.scores
                A = final_score[TEAM_A]
                B = final_score[TEAM_B]
                A_scores.append(A)
                B_scores.append(B)
                if A > B:
                    A_wins.append(1)
                elif A == B:
                    A_wins.append(0.5)
                else:
                    A_wins.append(0)
                break
        if random() > 0.5:
            game.pos_team = game.home
            game.def_team = game.away
        else:
            game.pos_team = game.away
            game.def_team = game.home
        game.is_kickoff = True
        game.is_extra_point = True
        game.scores = {game.home: 0, game.away: 0}
        game.ydline_100_pos = None
        game.first_down = None
        game.time_left = 3600
        game.effective_time_left = 900
        game.max_effective_time = max_effective_time
        game.first_down_100 = None
        game.down = None

        game.pos_minus_def_score = None
        game.yd_to_go = None
        game.qtr = 1
        game.number_of_plays = 0
        print()
        print('--*---*---')
        print('Average', TEAM_A,'scores:', stat.mean(A_scores), ',',TEAM_B,'scores:', stat.mean(B_scores))
        print('Proportion of', TEAM_A,  'wins:', stat.mean(A_wins))
        print('iteration:', j)

    pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in {'home_team': [TEAM_A],
    'away_team': [TEAM_B],
    'home_score': A_scores,
    'away_score': B_scores
    }.items() ])).fillna(method='ffill').to_csv(f'new_games/wk13/{TEAM_A}vs{TEAM_B}.csv', index=False)