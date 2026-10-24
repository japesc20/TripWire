import yfinance as yf
import pandas as pd


def extract_prices(ticker: str, start: str):
  df = yf.download(ticker, start=start, auto_adjust=False, progress=False)

  if df is None or df.empty:
    raise RuntimeError(f"No price data returned for {ticker}")

  return df


if __name__ == "__main__":
  df = extract_prices('VOO', '2018-01-01')
  print(type(df))
  print(df.shape)
  print(df.columns)
  print(df.dtypes)
  print(df.index[:3])
  print(df.tail())