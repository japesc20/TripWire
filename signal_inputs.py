from pathlib import Path

import duckdb

DB_PATH = Path(__file__).resolve().parent / "monitor.duckdb"

SQL = """
    WITH px AS (
        SELECT date, close,
               close / max(close) OVER w252 - 1 AS drawdown,
               avg(close) OVER w10          AS sma10
        FROM prices
        WHERE ticker = 'VOO'
        WINDOW w252 AS (ORDER BY date ROWS BETWEEN 251 PRECEDING AND CURRENT ROW),
               w10  AS (ORDER BY date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW)
    ),
    spread AS (
        SELECT date, value,
               value - lag(value, 5) OVER (ORDER BY date) AS chg_5obs
        FROM oas_clean
    )
    SELECT
        px.date                             AS price_date,
        px.close                            AS close,
        px.sma10                            AS sma10,
        px.close > px.sma10                 AS above_sma,
        round(px.drawdown, 6)               AS drawdown,
        s.date                              AS oas_date,
        s.value                             AS oas,
        round(s.chg_5obs, 6)                AS oas_chg_5obs,
        date_diff('day', s.date, px.date)   AS lag_days
    FROM px
    ASOF LEFT JOIN spread s ON px.date >= s.date
    ORDER BY px.date DESC
    LIMIT 1
"""


def get_signal_inputs(db_path=DB_PATH):
    con = duckdb.connect(str(db_path), read_only=True)
    cur = con.execute(SQL)
    row = cur.fetchone()
    assert row is not None
    cols = [d[0] for d in cur.description]
    con.close()
    return dict(zip(cols, row))