

PARAMS = {
  "correcting_drawdown": -0.08,
  "stress_drawdown": -0.10,
  "oas_deadband": 0.05,
  "max_lag_days": 4,
}


def classify(drawdown, oas_change, above_sma, lag_days, p=PARAMS):
  if drawdown is None or oas_change is None or above_sma is None or lag_days is None:
    return "INSUFFICIENT_DATA"
  if lag_days > p["max_lag_days"]:
      return "STALE_DATA"
  if drawdown > p["correcting_drawdown"]:
      return "NORMAL"
  if oas_change < -p["oas_deadband"] and above_sma:
      return "STABILIZING"
  if drawdown <= p["stress_drawdown"] and oas_change > p["oas_deadband"]:
      return "STRESS"
  return "CORRECTING"


if __name__ == "__main__":
    cases = [
        (-0.0121, 0.01, True, 1, "NORMAL"),
        (-0.12, 0.01, False, 0, "CORRECTING"),
        (-0.12, 0.10, False, 0, "STRESS"),
        (-0.12, -0.10, True, 0, "STABILIZING"),
        (-0.12, -0.10, False, 0, "CORRECTING"),
        (-0.09, 0.10, False, 0, "CORRECTING"),
        (-0.0121, None, True, 1, "INSUFFICIENT_DATA"),
        (None, 0.01, True, 1, "INSUFFICIENT_DATA"),
        (-0.12, 0.10, False, 5, "STALE_DATA"),
    ]
    for dd, chg, above, lag, expected in cases:
        got = classify(dd, chg, above, lag)
        assert got == expected, f"{dd}, {chg}, {above}, {lag}: expected {expected}, got {got}"
    print("all cases pass")