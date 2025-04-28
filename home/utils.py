import requests
import random


def fetch_random_pokemon():
    pokemon_id = random.randint(1, 898)
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        return {
            "name": data["name"].capitalize(),
            "type": data["types"][0]["type"]["name"].capitalize(),
            "hp": stats.get("hp", 0),
            "attack": stats.get("attack", 0),
            "defense": stats.get("defense", 0),
            "sp_attack": stats.get("special-attack", 0),
            "sp_defense": stats.get("special-defense", 0),
            "speed": stats.get("speed", 0),
            "image_url": data["sprites"]["other"]["official-artwork"]["front_default"]
        }
    return None

def fetch_six_random_pokemon():
    pokemon_list = []
    while len(pokemon_list) < 6:
        p = fetch_random_pokemon()
        if p:
            pokemon_list.append(p)
    return pokemon_list
