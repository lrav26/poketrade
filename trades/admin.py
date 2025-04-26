from django.contrib import admin
from .models import TradeOffer, TradeListing, ListingOffer

@admin.register(TradeOffer)
class TradeOfferAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender__username', 'receiver__username')

@admin.register(TradeListing)
class TradeListingAdmin(admin.ModelAdmin):
    list_display = ('user', 'pokemon', 'created_at')
    search_fields = ('user__username', 'pokemon__name')

@admin.register(ListingOffer)
class ListingOfferAdmin(admin.ModelAdmin):
    list_display = ('listing', 'sender', 'offered_pokemon', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('sender__username', 'offered_pokemon__name', 'listing__pokemon__name')
