from fastapi import APIRouter, Header, HTTPException, Query
from app.estadisticas_fantasy import estadisticas
from app import models

router = APIRouter(prefix="/api/v1", tags=["players"])

@router.get("/players", response_model=models.JugadorResponse)
def get_player(player_name: str = Query(...)):
    player_stats = estadisticas.get_player_stats(player_name)
    if not player_stats:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_stats

@router.get("/players/health")
def health():
    return {"status": "ok"}
