import os
import pandas as pd

DATASETS_DIR = os.path.join(os.getcwd(), '..', 'data')

def load_raw_data():
    df_injuries = pd.read_csv(os.path.join(DATASETS_DIR, 'Injury_History.csv'))
    df_stats = pd.read_csv(os.path.join(DATASETS_DIR, 'gamelogs_2021_22.csv'))

    dataframes = {
        'injuries': df_injuries,
        'stats': df_stats
    }
    return dataframes

if __name__ == '__main__':
    print(load_raw_data()['injuries'].head())
    print(load_raw_data()['stats'].head())

