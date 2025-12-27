# FastAPI 主框架
from fastapi import FastAPI

# CORS 中介層（允許前端跨網域呼叫 API）
from fastapi.middleware.cors import CORSMiddleware

# 資料驗證用（確保前端送來的資料格式正確）
from pydantic import BaseModel


app = FastAPI()

# CORS（GitHub Pages 必須）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允許所有前端網域（GitHub Pages 必須）
    allow_methods=["*"],      # 允許 POST / GET / OPTIONS
    allow_headers=["*"],      # 允許 JSON header
)

class TradeInput(BaseModel):
    direction: str    # Buy / Sell / Buy Stop / Sell Stop
    capital: float    # 本金
    risk_pct: float   # 風險比例（%）
    rr: float         # 盈虧比
    entryPrice: float      # 進場價
    stopPrice: float       # 止損價 
    
@app.post("/calculate")
def calculate(data: TradeInput):
    # 基本計算
    risk_amount = data.capital * data.risk_pct / 100 # 單筆可承受虧損金額
    price_diff = abs(data.entryPrice - data.stopPrice) # 進場與止損價差

    # 假設：0.01 手數 = 價差 * 1
    loss_per_001 = price_diff
    profit_per_001 = price_diff * data.rr

    # 建議手數（四捨五入到 0.01）
    lot = (risk_amount / loss_per_001)* 0.01

    # 實際盈虧
    actual_loss = loss_per_001 * lot
    actual_profit = profit_per_001 * lot

    # 止盈價
    if data.direction.lower().startswith("buy"):
        take_profit = data.entryPrice + price_diff * data.rr
    else:
        take_profit = data.entryPrice - price_diff * data.rr

    return {
        "direction": data.direction,
        "entryPrice": data.entryPrice,
        "stopPrice": data.stopPrice,
        "take_profit": round(take_profit, 2),
        "loss_per_001": round(loss_per_001, 2),
        "profit_per_001": round(profit_per_001, 2),
        "lot": round(lot, 2),
        "actual_loss": round(actual_loss, 2),
        "actual_profit": round(actual_profit, 2),
    }