from FRED import extract_data, get_observations, observations_cleaned, drop_missing_values
from load_duck import load_to_duckdb


SERIES = ["BAMLH0A0HYM2", "VIXCLS", "T10Y2Y"]


def refresh_series(series_id):
  data = extract_data(series_id=series_id, limit=None, observation_start='2018-01-01')

  if data is None:
    return None

  df = drop_missing_values(observations_cleaned(get_observations(data)))

  return load_to_duckdb(df, series_id)



if __name__ == "__main__":
  for sid in SERIES:
    n = refresh_series(sid)
    print(sid, n)