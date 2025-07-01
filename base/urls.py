from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("login/",login_page,name="login"),
    path("logout/",logout_user,name="logout"),
    path("",home,name = "Home"),
    path("room/",rooms_view,name = "Rooms"),
    path("room/<int:id>/",room,name = "Room"),
    path("create-room/",create_room,name="createRoom"),
    path("update-room/<int:pk>/",update_room,name="updateRoom"),
    path("delete-room/<int:pk>/",delete_room,name="deleteRoom"),
]
