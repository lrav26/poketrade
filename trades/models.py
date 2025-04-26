from django.db import models
from django.contrib.auth.models import User
from home.models import Pokemon

class TradeOffer(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
        ('CANCELLED', 'Cancelled'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_trades')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_trades')
    sender_pokemon = models.ManyToManyField(Pokemon, related_name='offered_in_trades')
    receiver_pokemon = models.ManyToManyField(Pokemon, related_name='requested_in_trades')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class TradeListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} offering {self.pokemon.name}"

class ListingOffer(models.Model):
    listing = models.ForeignKey('TradeListing', on_delete=models.CASCADE, related_name='offers')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    offered_pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('DECLINED', 'Declined'),
    ], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} offers {self.offered_pokemon.name} for {self.listing.pokemon.name}"
