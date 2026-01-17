from datetime import datetime

def generate_mock_signals():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    signals = [
        {"symbol": "NIFTY", "action": "BUY", "entry": 22450, "sl": 22380, "target": 22600, "time": now},
        {"symbol": "BANKNIFTY", "action": "SELL", "entry": 47800, "sl": 47950, "target": 47450, "time": now},
        {"symbol": "RELIANCE", "action": "BUY", "entry": 2920, "sl": 2895, "target": 2990, "time": now},
        {"symbol": "TCS", "action": "SELL", "entry": 3950, "sl": 4010, "target": 3850, "time": now},
        {"symbol": "INFY", "action": "BUY", "entry": 1670, "sl": 1645, "target": 1720, "time": now},
        {"symbol": "HDFCBANK", "action": "SELL", "entry": 1565, "sl": 1585, "target": 1530, "time": now},
    ]
    return signals
