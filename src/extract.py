import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

RAW_PATH = "/tmp/raw_weather.pkl"


def extract():
    cache_session = requests_cache.CachedSession("/tmp/.openmeteo_cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": [38.25],
        "longitude": [21.74],
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "rain",
            "showers",
            "snowfall",
            "precipitation",
            "weather_code",
            "pressure_msl",
        ],
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    print(f"Coordinates: {response.Latitude()} N {response.Longitude()} E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "rain": hourly.Variables(2).ValuesAsNumpy(),
        "showers": hourly.Variables(3).ValuesAsNumpy(),
        "snowfall": hourly.Variables(4).ValuesAsNumpy(),
        "precipitation": hourly.Variables(5).ValuesAsNumpy(),
        "weather_code": hourly.Variables(6).ValuesAsNumpy(),
        "pressure_msl": hourly.Variables(7).ValuesAsNumpy(),
    }

    df = pd.DataFrame(data=hourly_data)
    print(f"Extracted {len(df)} rows")
    df.to_pickle(RAW_PATH)
    return df


if __name__ == "__main__":
    extract()
