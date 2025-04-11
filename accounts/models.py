# accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Automatically create/update profile when a user is created/updated
# accounts/models.py

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Only save if profile exists (it might not for legacy users)
        Profile.objects.get_or_create(user=instance)

