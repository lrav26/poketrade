from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import fetch_six_random_pokemon
from accounts.models import Profile


@receiver(post_save, sender=User)
def give_new_user_starter_pack(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, defaults={'poke_coins': 100.00})

        pokemons = fetch_six_random_pokemon()
        for poke in pokemons:
            Pokemon.objects.create(
                user=instance,
                name=poke["name"],
                type=poke["type"],
                hp=poke["hp"],
                attack=poke["attack"],
                image_url=poke["image_url"]
            )

class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemons')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField(default=0)
    sp_attack = models.IntegerField(default=0)
    sp_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    image_url = models.URLField()
    nickname = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Pokemon"

    def __str__(self):
        return self.nickname or self.name