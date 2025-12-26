def calculate_trade(capital, risk_pct, entry, stop, rr=1.8):
    risk_amount = capital * risk_pct / 100
    price_diff = abs(entry - stop)

    loss_per_lot = price_diff
    lot_size = risk_amount / loss_per_lot
    lot_size = round(lot_size, 2)

    actual_loss = loss_per_lot * lot_size
    take_profit = entry + price_diff * rr if entry > stop else entry - price_diff * rr
    actual_profit = actual_loss * rr

    return {
        "lot_size": lot_size,
        "stop_loss": stop,
        "take_profit": round(take_profit, 2),
        "actual_loss": round(actual_loss, 2),
        "actual_profit": round(actual_profit, 2),
    }
