from django.urls import path
from . import views

urlpatterns = [
    path('trade_center/', views.trade_center_home, name='trade_center_home'),
    path('list_for_trade/<int:pokemon_id>/', views.list_pokemon_for_trade, name='list_pokemon_for_trade'),
    path('make_offer/<int:listing_id>/', views.make_trade_offer, name='make_trade_offer'),
    path('my_listings_offers/', views.my_listings_offers, name='my_listings_offers'),
    path('respond_offer/<int:offer_id>/', views.respond_to_listing_offer, name='respond_to_listing_offer'),
]
