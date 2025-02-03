from django.urls import path, include
from rest_framework import routers
from api import views

routers = routers.DefaultRouter()
routers.register("roulettes", views.RouletteViewSet)
routers.register("bets", views.BetViewSet)


urlpatterns = [path("", include(routers.urls))]
