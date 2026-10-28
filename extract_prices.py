import yfinance as yf
import polars as pl

from load_duck import load_prices_to_duckdb



TICKERS = ["VOO", "SCHD", "XLV", "XLP", "VGLT"]


def extract_prices(ticker: str, start: str):
  df = yf.download(ticker, start=start, auto_adjust=False, progress=False)

  if df is None or df.empty:
    raise RuntimeError(f"No price data returned for {ticker}")

  return df


def clean_prices(df, ticker):
  df = df.droplevel("Ticker", axis=1)
  df = df.reset_index()
  out = pl.from_pandas(df)

  return out.select(
    pl.lit(ticker).alias("ticker"),
    pl.col("Date").cast(pl.Date).alias("date"),
    pl.col("Close").round(4).alias("close"),
    pl.col("Adj Close").round(4).alias("adj_close")
  )


def refresh_prices(ticker):
  raw = extract_prices(ticker, '2018-01-01')
  df = clean_prices(raw, ticker)

  return load_prices_to_duckdb(df)



if __name__ == "__main__":
  for t in TICKERS:
    # refresh_prices(t)
    print(t, refresh_prices(t))