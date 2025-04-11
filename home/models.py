from django.db import models

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    hp = models.IntegerField()
    attack = models.IntegerField()
    image_url = models.URLField()
    nickname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nickname or self.name