from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}",
    connect_args={"client_encoding": "win1250"}
)

df = pd.read_sql("SELECT * FROM injuries", engine)


def drop_noise_rows(df: pd.DataFrame) -> pd.DataFrame:
    print('Dropping rows that creates noise...')

    df_filtered = df[df['injury_classification'] != 2]

    return df_filtered

