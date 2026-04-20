import pandas as pd
from data_loader import load_raw_data
from typing import Literal
from src.gamelog_data_pull import get_player_id

def remove_duplicates(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)

    return df

def join_positions(df: pd.DataFrame):
    # Join positions in Injury dataset
    print('Joining guards and forwards positions...')

    df["Position"] = df["Position"].replace({'PG': 'G', 'SG': 'G', 'SF': 'F', 'PF': 'F'})
    return df

def remove_unused_columns(df: pd.DataFrame):
    # Removing unused columns in gamelogs dataset
    print('Removing unused columns...')
    unused_columns = ['VIDEO_AVAILABLE', 'FG3_PCT', 'FG_PCT', 'FT_PCT']

    for c in unused_columns:
        if c in df.columns:
            df.drop(c, axis=1, inplace=True)
            print(f'Removed: {c}')

    return df

def convert_data_column(df: pd.DataFrame):
    # Converting to the same data format, as a primary data format we use the on in injury_history
    print('Converting time column to the same format...')

    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE']).dt.strftime('%d/%m/%Y')
    return df

def rename_columns(df:pd.DataFrame, name: Literal['stats', 'injuries']):
    print(f'Renaming column names for {name} dataset...')
    if name not in ('stats', 'injuries'):
        raise ValueError(f'Invalid name. Choose from: stats, injuries')
    df.columns = df.columns.str.lower()
    if name == 'stats':
        df.rename(columns={
            'wl': 'match_result'
        }, inplace=True)
    elif name == 'injuries':
        df.rename(columns={
            'name': 'player_name',
            'date': 'injury_date',
            'notes': 'injury_description'
        }, inplace=True)
    return df

def map_game_host(df:pd.DataFrame):
    print('Mapping hosts to the game...')

    df['host_team'] = df['matchup'].apply(
        lambda x: x[-3:] if '@' in x else x[:3]
    )
    return df

def map_team_with_player(df: pd.DataFrame):
    print('Mapping player to his team...')

    df['player_team'] = df['matchup'].apply(
        lambda x: x[:3]
    )
    return df

def map_player_with_id(df: pd.DataFrame):
    print('Mapping id to the players...')
    for idx, name in df['Name'].items():
        player_id = get_player_id(name)
        df.at[idx, 'Player_id'] = player_id
    df['Player_id'] = df['Player_id'].astype(int)
    return df






if __name__ == '__main__':
    pd.set_option('display.max_columns', 30)
    injury_df = load_raw_data()['injuries']
    injury_df = remove_duplicates(injury_df)
    injury_df = join_positions(injury_df)
    injury_df = map_player_with_id(injury_df)
    injury_df = rename_columns(injury_df, 'injuries')
    injury_df['injury_id'] = range(len(injury_df))
    injury_df = injury_df.iloc[:, [6, 5, 0, 1, 2, 3, 4]]
    
    injury_df.to_csv('Injury_History_Preprocessed.csv', index=False)

    gamelog_df = load_raw_data()['stats']
    gamelog_df = remove_duplicates(gamelog_df)
    gamelog_df = remove_unused_columns(gamelog_df)
    gamelog_df = convert_data_column(gamelog_df)
    gamelog_df = rename_columns(gamelog_df, 'stats')
    gamelog_df = map_game_host(gamelog_df)
    gamelog_df['stats_id'] = range(len(gamelog_df))
    gamelog_df = map_team_with_player(gamelog_df)
    front_cols = ['stats_id', 'game_id', 'season_id', 'player_id', 'player_team', 'host_team']
    remaining = [c for c in gamelog_df.columns if c not in front_cols]
    gamelog_df = gamelog_df[front_cols + remaining]


    gamelog_df.to_csv('Gamelogs_2014-2020_Preprocessed.csv', index=False)


