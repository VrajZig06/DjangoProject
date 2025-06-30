from django.contrib import admin
from base.models import *
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)

