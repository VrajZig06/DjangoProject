from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(request):
    return render(request,'base/home.html')


def rooms_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.all()

    if q:
        rooms = Room.objects.filter(topic__name__contains = q)
        room_count = len(rooms)
    else:
        rooms = Room.objects.all()
        room_count = rooms.count()
    

    context =  {"rooms": rooms,'topics' :topics,'room_count' : room_count}
    return render(request, 'base/room.html',context)


def room(request,id):

    selected_room = Room.objects.filter(id = id)
    all_messages = Message.objects.all()
    participants = selected_room[0].participants.all()

    if selected_room:
        context = {'room': selected_room[0],'all_messages' : all_messages,'participants':participants}
    
        return render(request, 'base/iroom.html', context)
    else:
        return HttpResponse("Room not found", status=404)
    
@login_required(login_url='Home')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Rooms')
    context = {'form' : form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='Home')
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    print(room)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed to Edit this Room")

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect("Rooms")

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='Home')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not allowed to Edit this Room")
    if room:
        room.delete()
        return redirect('Rooms')
    return redirect('Rooms')


def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        try:
            user = User.objects.get(username = username)
            print(user)
        except Exception: 
            messages.error(request, "User does not exists.")

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Rooms')
        else:
            messages.error(request,"Username and password are wrong.")

    context = {"login" : "Done"}
    return render(request,'base/login_register.html',context)

@login_required(login_url='Home')
def logout_user(request):
    
    try:
        logout(request)
    except Exception:
        messages.error("Something ent Wrong!")
    return redirect("Home")

def register_user(request):
    form = UserCreationForm()
    context = {"form" : form}
    return render(request,'base/login_register.html',context)

@login_required(login_url="Home")
def create_message(request,pk):
    room = Room.objects.get(id = pk)
    context = {"room" : room}
    print(request.user)
    print(room.host)
    if request.method == 'POST':
        print(request.POST.get('message_body'))
        message = Message.objects.create(user = request.user,room = room,body = request.POST.get('message_body'))
        message.save()
        return redirect(f'http://127.0.0.1:8000/room/{room.id}/')

    return render(request,'base/iroom.html',context)