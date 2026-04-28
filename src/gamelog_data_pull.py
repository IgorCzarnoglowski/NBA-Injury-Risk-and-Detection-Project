from nba_api.stats.endpoints import playergamelog, commonplayerinfo
from nba_api.stats.static import players
import pandas as pd
import time
import os

DATASET_PATH = os.path.join(os.getcwd(), '..', 'data', 'Injury_History.csv')

def get_player_id(player_name: str) -> int:
    all_players = players.get_players()
    player = [p for p in all_players if p['full_name'].lower() == player_name.lower()]

    if not player:
        raise ValueError(f"Nie znaleziono gracza: {player_name}")

    return player[0]['id']

def join_players_name_id(names: list):
    data = []

    for n in names:
        player_id = get_player_id(n)
        data.append({
            'PLAYER_ID': player_id,
            'PLAYER_NAME': n
        })

    df = pd.DataFrame(data)

    return df

def get_all_gamelogs_for_seasons(players: pd.DataFrame):
    all_gamelogs = []
    seasons = ['2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20']

    for _, row in players.iterrows():
        player_name = row['PLAYER_NAME']
        for season in seasons:
            try:
                gamelog = playergamelog.PlayerGameLog(
                    player_id=row['PLAYER_ID'],
                    season=season,
                    season_type_all_star='Regular Season'
                )
                df = gamelog.get_data_frames()[0]

                if df.empty:
                    continue

                all_gamelogs.append(df)


                print(f"✓ {player_name} w sezonie {season} — {len(df)} meczów")

            except Exception as e:
                print(f"✗ {player_name} w sezonie {season} — błąd: {e}")

            time.sleep(1)

    return pd.concat(all_gamelogs, ignore_index=True)


def get_players_info(players_df: pd.DataFrame) -> pd.DataFrame:
    info_rows = []

    for _, row in players_df.iterrows():
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=row['PLAYER_ID'])
            df = info.get_data_frames()[0]
            info_rows.append(df.iloc[0])
            print(f"✓ {row['PLAYER_NAME']} — info fetched")
        except Exception as e:
            print(f"✗ {row['PLAYER_NAME']} — błąd: {e}")
        time.sleep(1)

    return pd.DataFrame(info_rows).reset_index(drop=True)


if __name__ == '__main__':
    injury_df = pd.read_csv(DATASET_PATH)
    unique_names = injury_df['Name'].unique()
    pd.set_option("display.max_columns", 100)

    players_df = join_players_name_id(unique_names)

    #gamelogs = get_all_gamelogs_for_seasons(players_df)
    #gamelogs.to_csv('gamelogs_2014_2020.csv', index=False)

    players_info = get_players_info(players_df)
    players_info.to_csv('players.csv', index=False)