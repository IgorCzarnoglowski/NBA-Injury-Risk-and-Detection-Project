from nba_api.stats.endpoints import commonallplayers, playergamelog
import pandas as pd
import time

def get_all_gamelogs_for_season(season: str):
    # Pobierz wszystkich graczy z sezonu
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=0,
        season=season
    )
    players_df = all_players.get_data_frames()[0]
    print(f"Znaleziono {len(players_df)} graczy")
    print(players_df.columns.tolist())  # sprawdź kolumny

    all_gamelogs = []

    for _, player in players_df.iterrows():
        player_id = player['PERSON_ID']
        player_name = player['DISPLAY_FIRST_LAST']  # podmień jeśli inna kolumna

        try:
            gamelog = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season,
                season_type_all_star='Regular Season'
            )
            df = gamelog.get_data_frames()[0]

            if df.empty:
                continue

            df['PLAYER_ID'] = player_id
            df['PLAYER_NAME'] = player_name
            all_gamelogs.append(df)

            print(f"✓ {player_name} — {len(df)} meczów")

        except Exception as e:
            print(f"✗ {player_name} — błąd: {e}")

        time.sleep(0.6)  # obowiązkowe

    return pd.concat(all_gamelogs, ignore_index=True)


df = get_all_gamelogs_for_season('2021-22')
df.to_csv('gamelogs_2021_22.csv', index=False)