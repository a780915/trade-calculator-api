from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS（GitHub Pages 必須）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TradeInput(BaseModel):
    direction: str
    capital: float
    risk_pct: float
    rr: float
    entry: float
    stop: float

@app.post("/calculate")
def calculate(data: TradeInput):
    # 基本計算
    risk_amount = data.capital * data.risk_pct / 100
    price_diff = abs(data.entry - data.stop)

    # 假設：0.01 手數 = 價差 * 1
    loss_per_001 = price_diff
    profit_per_001 = price_diff * data.rr

    # 建議手數（四捨五入到 0.01）
    lot = risk_amount / loss_per_001
    lot = round(lot / 0.01) * 0.01

    actual_loss = loss_per_001 * (lot / 0.01)
    actual_profit = profit_per_001 * (lot / 0.01)

    # 止盈價
    if data.direction.lower().startswith("buy"):
        take_profit = data.entry + price_diff * data.rr
    else:
        take_profit = data.entry - price_diff * data.rr

    return {
        "direction": data.direction,
        "entry": data.entry,
        "stop": data.stop,
        "take_profit": round(take_profit, 2),
        "loss_per_001": round(loss_per_001, 2),
        "profit_per_001": round(profit_per_001, 2),
        "lot": round(lot, 2),
        "actual_loss": round(actual_loss, 2),
        "actual_profit": round(actual_profit, 2),
    }
