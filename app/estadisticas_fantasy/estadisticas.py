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
        calculated_score=oportunity_score
    )
    
    

def get_player_name(data: dict, name: str) -> tuple[str, int] | None:
    i = 0
    for player in data.get("data", []):
        i += 1
        if (name.lower()) in player["nickname"].lower():
            return player["nickname"], i-1
    return None

def get_score(player: dict) -> models.CalculatedScore:
    POSITIONS = {
    1: 0.561,
    2: 0.369,
    3: 0.207,
    4: 0.199,    
}
    position = player.get("positionId")
    market_value = player.get("marketValue")
    media_rating = player.get("averagePoints")    
    posible_real_price = calculate_real_price(media_rating, POSITIONS.get(position, 0))   
    difference = posible_real_price - market_value 
    difference_percentage = (difference / market_value) * 100
    score_text = get_score_text(difference_percentage)
    
    return models.CalculatedScore(
        score=score_text,
        posible_real_price=round(posible_real_price, 2),
        difference=round(difference, 2),
        difference_percentage=f'{difference_percentage:.2f}%'
    )           

def calculate_score(market_value: float, media_rating: float) -> float:
    return ((media_rating / market_value) * 1000000)

def calculate_real_price(media_rating: float, position_value: float) -> float:    
    return (media_rating / position_value) * 1000000

def get_score_text(difference_percentage: float) -> str:
    if difference_percentage >= 50:
        return "Super ganga"
    elif difference_percentage >= 25 and difference_percentage < 50:
        return "Ganga"
    elif difference_percentage >= 10 and difference_percentage < 25:
        return "Buena oportunidad"
    elif difference_percentage >= -10 and difference_percentage < 10:
        return "Precio justo"
    elif difference_percentage >= -25 and difference_percentage < -10:
        return "Caro"
    elif difference_percentage >= -50 and difference_percentage < -25:
        return "Muy caro"
    elif difference_percentage < -50:
        return "Extremadamente Sobrevalorado"    

if __name__ == "__main__":
    data = get_season_summary()
    print(data)
