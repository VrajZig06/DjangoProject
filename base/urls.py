from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("",home,name = "Home"),
    path("room/",rooms_view,name = "Rooms"),
    path("room/<int:id>/",room,name = "Room")
]
