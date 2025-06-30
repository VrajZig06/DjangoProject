from django.shortcuts import render
from django.shortcuts import render 
from django.http import HttpResponse
from .models import Room


rooms = [
        {'id' : 1 , "title" : "Let's Learn Python!"},
        {'id' : 2 , "title" : "Let's Explore World."},
        {'id' : 3 , "title" : "Let's Explore Java."},   
    ]

def home(request):
    return render(request,'base/home.html')

def rooms_view(request):
    rooms = Room.objects.all()
    context =  {"rooms": rooms}
    return render(request, 'base/room.html',context)

def room(request,id):

    selected_room = Room.objects.filter(id = id)

    if selected_room:
        context = {'room': selected_room[0]}
    
        return render(request, 'base/iroom.html', context)
    else:
        return HttpResponse("Room not found", status=404)