import requests
from app import models

BASE_URL = "https://server.analiticafantasy.com/api/v1"


def get_season_summary(season: int) -> dict:
    response = requests.get(f"{BASE_URL}/fantasy-player-stats/season-summary", params={"season": season})
    response.raise_for_status()
    return response.json()

def get_player_stats(name: str, season: int = 2026) -> list[models.JugadorResponse] | None:
    stats = get_season_summary(season)
    players_info = get_player_name(stats, name)
    players_response = []
    # player_name, player_index = get_player_name(stats, name)  
    for player_name, player_index in players_info:  
        market_value = stats["data"][player_index]["marketValue"]
        media_rating = stats["data"][player_index]["averagePoints"]
        oportunity_score=get_score(stats["data"][player_index])

        players_response.append(models.JugadorResponse(
            name=player_name,
            market_value=market_value,
            media_rating=media_rating,
            calculated_score=oportunity_score
        ))

    if not players_response:
        return None
    
    return players_response
    
    

def get_player_name(data: dict, name: str) -> list[tuple[str, int]] | None:
    i = 0
    candidates = []
    for player in data.get("data", []):
        i += 1
        if (name.lower()) in player["nickname"].lower():
            candidates.append((player["nickname"], i-1))
    if candidates:
        return candidates    
    return None

def get_score(player: dict) -> models.CalculatedScore:
    position = player.get("positionId")
    market_value = player.get("marketValue")
    media_rating = player.get("averagePoints")    
    # posible_real_price = calculate_real_price(media_rating, POSITIONS.get(position, 0))   
    posible_real_price = calculate_real_price(media_rating, get_position_value(position, media_rating))   
    difference = posible_real_price - market_value 
    difference_percentage = (difference / posible_real_price) * 100
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

def get_position_value(position_id: int, media_rating: float) -> float:
    POSITIONS = {
        1: 0.561,
        2: 0.369,
        3: 0.207,
        4: 0.199,    
    }

    POSITION_VALUES = {
        1: {  # POR
            (0, 1): 0.182,
            (1, 2): 1.257,
            (2, 3): 2.348,
            (3, 4): 3.137,
            (4, 5): 2.346,
            (5, 6): 1.883,
            (6, 7): 0.750,
            (7, 8): 0.381,
            (8, 9): 0.113,
        },
    
        2: {  # DEF
            (0, 1): 0.564,
            (1, 2): 1.537,
            (2, 3): 2.092,
            (3, 4): 1.172,
            (4, 5): 0.338,
            (5, 6): 0.216,
            (6, 7): 0.103,
        },
    
        3: {  # MED
            (0, 1): 0.627,
            (1, 2): 1.633,
            (2, 3): 2.135,
            (3, 4): 1.841,
            (4, 5): 0.645,
            (5, 6): 0.167,
            (6, 7): 0.077,
            (7, 8): 0.076,
            (8, 9): 0.081,
            (9, 10): 0.080,
        },
    
        4: {  # DEL
            (0, 1): 0.768,
            (1, 2): 1.601,
            (2, 3): 2.230,
            (3, 4): 2.093,
            (4, 5): 0.573,
            (5, 6): 0.190,
            (6, 7): 0.107,
            (7, 8): 0.067,
            (8, 9): 0.069,
            (9, 10): 0.069,
            (10, 11): 0.066,
            (11, 12): 0.085,
        }                
    }

    for minimun, maximun in POSITION_VALUES.get(position_id, {}):
        if minimun <= media_rating < maximun:
            return POSITION_VALUES[position_id][(minimun, maximun)]
    return POSITIONS.get(position_id, 0)


if __name__ == "__main__":
    data = get_season_summary()
    print(data)
