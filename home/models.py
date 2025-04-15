from django.db import models
from django.contrib.auth.models import User

class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemons',
                             default=1)  # 1 could be the ID of a default user, such as the admin
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pokemons')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    image_url = models.URLField()
    nickname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nickname or self.name
