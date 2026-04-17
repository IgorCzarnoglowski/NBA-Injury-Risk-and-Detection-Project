import pandas as pd
from data_loader import load_data
from typing import Literal
from src.gamelog_data_pull import get_player_id

def remove_duplicates(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)

    return df

def remove_unused_columns(df: pd.DataFrame):
    # Removing unused columns in gamelogs dataset
    print('Removing unused columns...')
    unused_columns = ['SEASON_ID', 'VIDEO_AVAILABLE', 'FG3_PCT', 'FG_PCT', 'FT_PCT', 'PLUS_MINUS']

    for c in unused_columns:
        if c in df.columns:
            df.drop(c, axis=1, inplace=True)
            print(f'Removed: {c}')

    return df

def join_positions(df: pd.DataFrame):
    # Join positions in Injury dataset
    print('Joining guards and forwards positions...')

    df["Position"] = df["Position"].replace({'PG': 'G', 'SG': 'G', 'SF': 'F', 'PF': 'F'})
    return df

def convert_data_column(df: pd.DataFrame):
    # Converting to the same data format, as a primary data format we use the on in injury_history
    print('Converting time column to the same format...')

    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE']).dt.strftime('%d/%m/%Y')
    return df

def rename_columns(df:pd.DataFrame, name: Literal['stats', 'injuries']):
    if name not in ('stats', 'injuries'):
        raise ValueError(f'Invalid name. Choose from: stats, injuries')
    df.columns = df.columns.str.lower()
    if name == 'stats':
        df.rename(columns={
            'wl': 'match_result'
        }, inplace=True)

    return df

def map_game_host(df:pd.DataFrame):
    df['host_team'] = df['matchup'].apply(
        lambda x: x[-3:] if '@' in x else x[:3]
    )
    return df

def map_player_with_id(df: pd.DataFrame):
    for idx, name in df['Name'].items():
        player_id = get_player_id(name)
        df.at[idx, 'Player_id'] = player_id
    df['Player_id'] = df['Player_id'].astype(int)
    return df






if __name__ == '__main__':
    df = load_data()['injuries']
    df = map_player_with_id(df)
    print(df.head(70))
