from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path("login/",login_page,name="login"),
    path("logout/",logout_user,name="logout"),
    path("register/",register_user,name="register"),
    path("user-profile/",user_profile,name="profile"),
    path("",home,name = "Home"),
    path("room/",rooms_view,name = "Rooms"),
    path("room/<int:id>/",room,name = "Room"),
    path("create-room/",create_room,name="createRoom"),
    path("update-room/<int:pk>/",update_room,name="updateRoom"),
    path("delete-room/<int:pk>/",delete_room,name="deleteRoom"),
    path("create-message/<int:pk>/",create_message,name="createMessage"),
    path("delete-message/<pk>/",delete_message,name="deleteMessage"),
]
