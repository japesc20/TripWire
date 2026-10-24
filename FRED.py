import os
import requests
import polars as pl

from dotenv import load_dotenv


from load_duck import load_to_duckdb


load_dotenv()


URL = 'https://api.stlouisfed.org/fred/series/observations'


def extract_data(series_id: str, limit, observation_start: str):
  fred_key = os.getenv('FRED_API_KEY')


  params = {
        "series_id": series_id,
        "api_key": fred_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
        "observation_start": observation_start
    }
  
  response = requests.get(URL, params=params, timeout=30)
  
  if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

  
  return response.json()


def get_observations(data):
   return data["observations"]


def observations_cleaned(observations):
  df = pl.DataFrame(observations)
  df = df.select(['date', 'value'])

  df = df.with_columns(
    pl.col('date').str.to_datetime(),
    pl.col('value').cast(pl.Float64, strict=False)
  )

  return df


def drop_missing_values(df):
   return df.drop_nulls(subset='value')


if __name__ == "__main__":
  data = extract_data(series_id='BAMLH0A0HYM2', limit=None, observation_start='2018-01-01')
  df = observations_cleaned(get_observations(data))
  df = drop_missing_values(df)

  n = load_to_duckdb(df, 'BAMLH0A0HYM2')

  print(n)
  # print(df.shape)
  # print(df['date'].min(), df['date'].max())
  # print(df['value'].null_count())