import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

DATASETS_DIR = os.path.join(os.getcwd(), '..', 'data')
load_dotenv()

def load_raw_data():
    df_injuries = pd.read_csv(os.path.join(DATASETS_DIR, 'Injury_History.csv'))
    df_stats = pd.read_csv(os.path.join(DATASETS_DIR, 'gamelogs_2014_2020.csv'))

    dataframes = {
        'injuries': df_injuries,
        'stats': df_stats
    }
    return dataframes

def get_engine():
    url = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    return create_engine(url)

def load_csv_to_table(csv_path: str, table_name:str):
    print(f'Loading {csv_path} to postgresql db...')
    engine = get_engine()
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False)

if __name__ == '__main__':
    load_csv_to_table("../data/Injury_History_Classified_AI.csv", "injuries")
    load_csv_to_table("../data/Gamelogs_2014-2020_Preprocessed.csv", "gamelogs")

