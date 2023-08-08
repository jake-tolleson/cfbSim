setwd("~/Documents/cfbSim")
Sys.setenv(CFBD_API_KEY = "18+Gfbnr49kndT7jIOAyB/eFpSPweo3X3lZnjqrmH1Jgh1jvJslWxtH9oVpa8d/n")
library(tidyverse)
library(lubridate)
library(cfbfastR)

# get pbp
# for(week in 1:10){
# df <- cfbfastR::cfbd_pbp_data(year=2022, week=week)
# df <- df |> mutate(time_left = case_when(period==1~(clock.minutes*60+clock.seconds)+3*900,
#                                    period==2~(clock.minutes*60+clock.seconds)+2*900,
#                                    period==3~(clock.minutes*60+clock.seconds)+900,
#                                    period==4~(clock.minutes*60+clock.seconds),
#                                    TRUE~0))
# df |> write_csv(paste0('raw_data/2022_',week,'_pbp.csv'))
# }
week = 13
df <- cfbfastR::cfbd_pbp_data(year=2022, week=week)
df <- df |> mutate(time_left = case_when(period==1~(clock.minutes*60+clock.seconds)+3*900,
                                   period==2~(clock.minutes*60+clock.seconds)+2*900,
                                   period==3~(clock.minutes*60+clock.seconds)+900,
                                   period==4~(clock.minutes*60+clock.seconds),
                                   TRUE~0))
df|> write_csv(paste0('raw_data/2022_',week,'_pbp.csv'))

cfbd_play_types() |> View()


# Get basic game info
game_infos <- cfbd_game_info(2022)
game_infos <- game_infos |> filter(week == 14) |> filter(home_division == 'fbs')
betting <- cfbd_betting_lines(year=2022)

game_infos |> left_join(betting, on='game_id') |> filter(provider=='Bovada') |>
select(game_id, away_team, home_team, spread) |> write_csv('new_espn_probs.csv')

          