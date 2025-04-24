from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade_home, name='trade_home'),
    path('create/<int:user_id>/', views.create_trade, name='create_trade'),
    path('respond/<int:trade_id>/', views.respond_to_trade, name='respond_to_trade'),
    path('cancel/<int:trade_id>/', views.cancel_trade, name='cancel_trade'),
    path('initiate/<int:pokemon_id>/', views.initiate_trade, name='initiate_trade'),
]