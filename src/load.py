import os
import pandas as pd
from sqlalchemy import create_engine

TRANSFORMED_PATH = "/tmp/transformed_weather.pkl"


def load(df, host, db, user, password, table):
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:5432/{db}")
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into {table}")


if __name__ == "__main__":
    df = pd.read_pickle(TRANSFORMED_PATH)
    load(
        df,
        os.getenv("DB_HOST", "db"),
        os.getenv("DB_NAME", "weatherdb"),
        os.getenv("DB_USER", "postgres"),
        os.getenv("DB_PASSWORD", "postgres"),
        os.getenv("DB_TABLE", "weather_data"),
    )
