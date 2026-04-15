import os
import pandas as pd

DATASETS_DIR = os.path.join(os.getcwd(), '..', 'data')

def load_data():
    df_injuries = pd.read_csv(os.path.join(DATASETS_DIR, 'Injury_History.csv'))
    df_stats = pd.read_csv(os.path.join(DATASETS_DIR, 'gamelogs_2021_22.csv'))

