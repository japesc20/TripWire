from market_signal import classify
from signal_inputs import get_signal_inputs

if __name__ == "__main__":
    inputs = get_signal_inputs()
    print(inputs)

    state = classify(
        inputs["drawdown"], inputs["oas_chg_5obs"],
        inputs["above_sma"], inputs["lag_days"],
    )
    print(state)