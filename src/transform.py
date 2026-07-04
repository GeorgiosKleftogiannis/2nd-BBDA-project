import pandas as pd

RAW_PATH = "/tmp/raw_weather.pkl"
TRANSFORMED_PATH = "/tmp/transformed_weather.pkl"


def transform():
    transformed = pd.read_pickle(RAW_PATH)

    if "date" in transformed.columns:
        transformed["date"] = pd.to_datetime(transformed["date"], errors="coerce")
        num_cols = transformed.columns.drop("date")
    else:
        num_cols = transformed.columns

    transformed[num_cols] = transformed[num_cols].apply(pd.to_numeric, errors="coerce")
    transformed = transformed.drop_duplicates()

    print(f"Transformed {len(transformed)} rows")
    transformed.to_pickle(TRANSFORMED_PATH)
    return transformed


if __name__ == "__main__":
    transform()
