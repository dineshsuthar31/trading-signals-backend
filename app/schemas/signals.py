from pydantic import BaseModel
from typing import List

class SignalItem(BaseModel):
    symbol: str
    action: str
    entry: float
    sl: float
    target: float
    time: str

class SignalsResponse(BaseModel):
    paid: bool
    count: int
    signals: List[SignalItem]
