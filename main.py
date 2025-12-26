from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ⭐ 一定要有，否則前端一定 fetch 失敗
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
    entry: float
    stop: float

@app.post("/calculate")
def calculate(data: TradeInput):
    risk_amount = data.capital * data.risk_pct / 100
    diff = abs(data.entry - data.stop)

    take_profit = (
        data.entry + diff * 1.8
        if data.entry > data.stop
        else data.entry - diff * 1.8
    )

    return {
        "direction": data.direction,
        "entry": data.entry,
        "stop": data.stop,
        "take_profit": round(take_profit, 2),
        "risk": risk_amount,
    }
