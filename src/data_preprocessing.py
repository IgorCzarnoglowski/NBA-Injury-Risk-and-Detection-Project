import pandas as pd
from data_loader import load_data
from typing import Literal

def remove_duplicates(df: pd.DataFrame):
    df.drop_duplicates(inplace=True)

    return df

def remove_unused_columns(df: pd.DataFrame, unused_columns: list):
    print('Removing unused columns...')
    for c in unused_columns:
        if c in df.columns:
            df.drop(c, axis=1, inplace=True)
            print(f'Removed: {c}')

    return df

def join_positions(df: pd.DataFrame):
    print('Joining guards and forwards positions...')

    df["Position"] = df["Position"].replace({'PG': 'G', 'SG': 'G', 'SF': 'F', 'PF': 'F'})
    return df

def convert_data_column(df: pd.DataFrame):
    print('Converting time column to the same format...')

    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE']).dt.strftime('%d/%m/%Y')
    return df









if __name__ == '__main__':
    df = load_data()['stats']
    df = convert_data_column(df)
    print(df['GAME_DATE'])