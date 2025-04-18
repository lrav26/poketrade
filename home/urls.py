from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('collection/', views.collection, name='collection'),  # This is the collection page route
    path('pokemon/<int:id>/', views.pokemon_detail, name='pokemonDetail'),
    path('nickname_update/<int:pk>/', views.nickname_update, name='nickname_update'),
    path('logs/', views.logs, name='logs'),
]