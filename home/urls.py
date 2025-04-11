from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('collection', views.collection, name='home.collection'),
    path('pokemon/<int:id>/', views.pokemon_detail, name='pokemonDetail'),

]