import requests
from app import models

BASE_URL = "https://server.analiticafantasy.com/api/v1"


def get_season_summary(season: int) -> dict:
    response = requests.get(f"{BASE_URL}/fantasy-player-stats/season-summary", params={"season": season})
    response.raise_for_status()
    return response.json()

def get_player_stats(name: str, season: int = 2026) -> models.JugadorResponse | None:
    stats = get_season_summary(season)
    player_name, player_index = get_player_name(stats, name)
    market_value = stats["data"][player_index]["marketValue"]
    media_rating = stats["data"][player_index]["averagePoints"]
    oportunity_score=get_score(stats["data"][player_index])

    if player_name is None:
        return None
    
    return models.JugadorResponse(
        name=player_name,
        market_value=market_value,
        media_rating=media_rating,
        oportunity_score=oportunity_score
    )
    
    

def get_player_name(data: dict, name: str) -> tuple[str, int] | None:
    i = 0
    for player in data.get("data", []):
        i += 1
        if (name.lower()) in player["playerName"].lower():
            return player["playerName"], i-1
    return None

def get_score(player: dict) -> str:
    POSITIONS = {
    1: 0.561,
    2: 0.369,
    3: 0.207,
    4: 0.199,    
}
    position = player.get("positionId")
    market_value = player.get("marketValue")
    media_rating = player.get("averagePoints")
    score = calculate_score(market_value, media_rating)

    if score > POSITIONS.get(position, 0):
        return "Buena oportunidad"
    else:
        return "Mala oportunidad"

def calculate_score(market_value: float, media_rating: float) -> float:
    return ((media_rating / market_value) * 1000000)

if __name__ == "__main__":
    data = get_season_summary()
    print(data)
