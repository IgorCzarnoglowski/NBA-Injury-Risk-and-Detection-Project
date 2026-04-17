import pandas as pd
from data_loader import load_data
from typing import Literal

def remove_duplicates(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)

    return df

def remove_unused_columns(df: pd.DataFrame):
    # Removing unused columns in gamelogs dataset
    print('Removing unused columns...')
    unused_columns = ['SEASON_ID', 'VIDEO_AVAILABLE', 'FG3_PCT', 'FG_PCT', 'FT_PCT']

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






if __name__ == '__main__':
    df = load_data()['stats']
    df = convert_data_column(df)
    df = map_game_host(df)