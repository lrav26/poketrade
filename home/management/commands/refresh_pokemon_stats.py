import requests
from django.core.management.base import BaseCommand
from home.models import Pokemon

class Command(BaseCommand):
    help = 'Refresh all Pokémon stats from the PokéAPI'

    def handle(self, *args, **kwargs):
        for p in Pokemon.objects.all():
            url = f"https://pokeapi.co/api/v2/pokemon/{p.name.lower()}"
            res = requests.get(url)

            if res.status_code != 200:
                self.stdout.write(self.style.WARNING(f"Could not fetch data for {p.name}"))
                continue

            data = res.json()
            stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}

            p.hp = stats.get("hp", p.hp)
            p.attack = stats.get("attack", p.attack)
            p.defense = stats.get("defense", p.defense)
            p.sp_attack = stats.get("special-attack", p.sp_attack)
            p.sp_defense = stats.get("special-defense", p.sp_defense)
            p.speed = stats.get("speed", p.speed)
            p.save()

            self.stdout.write(self.style.SUCCESS(f"Updated {p.name}"))