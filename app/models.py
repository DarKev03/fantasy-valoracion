from pydantic import BaseModel

class JugadorRequest(BaseModel):
    name: str

class CalculatedScore(BaseModel):
    score: str
    posible_real_price: float
    difference: float
    difference_percentage: str

class JugadorResponse(BaseModel):
    name: str
    market_value: float
    media_rating: float
    calculated_score: CalculatedScore