import polars as pl
import duckdb



def load_to_duckdb(df, series_id, db_path='monitor.duckdb'):
  df = df.with_columns(
    pl.lit(series_id).alias('series_id'),
    pl.col('date').cast(pl.Date)
  ).select(['series_id', 'date', 'value'])


  conn = duckdb.connect(db_path)
  conn.execute("""
        CREATE TABLE IF NOT EXISTS fred_series (
          series_id VARCHAR,
          date DATE,
          value DOUBLE,
          PRIMARY KEY(series_id, date)
        )            
    """)

  conn.execute("""
      INSERT OR REPLACE INTO fred_series SELECT * from df
  """)
  
  row = conn.execute(
        "SELECT COUNT(*) FROM fred_series WHERE series_id = ?", [series_id]
    ).fetchone()
  assert row is not None
  n = row[0]

  
  conn.close()

  return n