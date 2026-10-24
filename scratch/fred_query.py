import duckdb

conn = duckdb.connect("monitor.duckdb", read_only=True)

rows = conn.execute("""
    WITH r AS (
        SELECT date, value,
               row_number() OVER (ORDER BY date DESC) AS raw_pos
        FROM fred_series
        WHERE series_id = 'BAMLH0A0HYM2' AND date >= '2026-10-01'
    ),
    c AS (
        SELECT date,
               row_number() OVER (ORDER BY date DESC) AS clean_pos
        FROM oas_clean
        WHERE date >= '2026-10-01'
    )
    SELECT r.date, r.value, r.raw_pos, c.clean_pos
    FROM r LEFT JOIN c USING (date)
    ORDER BY r.date DESC
""").fetchall()

for r in rows:
    print(r)
conn.close()