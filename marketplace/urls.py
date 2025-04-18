from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('listing/<int:listing_id>/', views.marketplace_listing_detail, name='marketplace_listing_detail'),
    path('listing/<int:listing_id>/buy/', views.buy_pokemon, name='buy_pokemon'),
    path('create_listing/<int:pokemon_id>/', views.create_listing, name='create_listing'),
]
