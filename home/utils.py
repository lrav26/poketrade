import requests
import random

def fetch_random_pokemon():
    """Fetches a single random Pokémon's data."""
    pokemon_id = random.randint(1, 151)  # Adjust range if needed
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"].capitalize(),
            "type": data["types"][0]["type"]["name"].capitalize(),
            "hp": data["stats"][0]["base_stat"],
            "attack": data["stats"][1]["base_stat"],
            "defense": data["stats"][2]["base_stat"],
            "sp_attack": data["stats"][3]["base_stat"],
            "sp_defense": data["stats"][4]["base_stat"],
            "speed": data["stats"][5]["base_stat"],
            "image_url": data["sprites"]["other"]["official-artwork"]["front_default"],
        }
    else:
        return None

def fetch_six_random_pokemon():
    """Fetches six random Pokémon."""
    pokemon_list = []
    while len(pokemon_list) < 6:
        p = fetch_random_pokemon()
        if p:
            pokemon_list.append(p)
    return pokemon_list