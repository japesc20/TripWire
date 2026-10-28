import json
import uuid
from datetime import datetime, timezone

import duckdb

from market_signal import PARAMS, classify
from signal_inputs import DB_PATH, get_signal_inputs


def write_snapshot(db_path=DB_PATH):
    inputs = get_signal_inputs(db_path)
    state = classify(
        inputs["drawdown"], inputs["oas_chg_5obs"],
        inputs["above_sma"], inputs["lag_days"],
    )

    snapshot_id = str(uuid.uuid4())
    ts_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    con = duckdb.connect(str(db_path))
    con.execute("""
        CREATE TABLE IF NOT EXISTS signal_snapshots (
            snapshot_id  VARCHAR PRIMARY KEY,
            ts_utc       VARCHAR NOT NULL,
            market_state VARCHAR NOT NULL,
            inputs       VARCHAR NOT NULL,
            params       VARCHAR NOT NULL
        )
    """)
    con.execute(
        "INSERT INTO signal_snapshots VALUES (?, ?, ?, ?, ?)",
        [
            snapshot_id, ts_utc, state,
            json.dumps(inputs, default=str, sort_keys=True),
            json.dumps(PARAMS, sort_keys=True),
        ],
    )
    con.close()
    return snapshot_id, state


if __name__ == "__main__":
    print(write_snapshot())