from django.contrib import admin
from .models import MarketplaceListing, TransactionHistory

admin.site.register(MarketplaceListing)
admin.site.register(TransactionHistory)
