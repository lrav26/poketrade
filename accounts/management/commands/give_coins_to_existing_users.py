from django.core.management.base import BaseCommand
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Give 100 PokeCoins to all existing users if they do not have coins set yet.'

    def handle(self, *args, **kwargs):
        updated = 0
        for profile in Profile.objects.all():
            if profile.poke_coins is None or profile.poke_coins == 0:
                profile.poke_coins = 100.00
                profile.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f"✅ Updated {updated} user(s) with 100 PokeCoins."))
