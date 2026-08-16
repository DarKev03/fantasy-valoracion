from pydantic import BaseModel


class JugadorResponse(BaseModel):
    name: str
    market_value: float
    media_rating: float
    oportunity_score: str

class JugadorRequest(BaseModel):
    name: str
