import duckdb


con = duckdb.connect("monitor.duckdb", read_only=True)
rows = con.execute("""
    SELECT ts_utc, market_state,
           json_extract_string(inputs, '$.drawdown') AS drawdown,
           json_extract_string(inputs, '$.price_date') AS price_date
    FROM signal_snapshots
    ORDER BY ts_utc DESC
""").fetchall()
for r in rows:
    print(r)
con.close()