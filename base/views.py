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
    recent_messages = Message.objects.all()[0:6]

    if q != "":
        recent_messages = Message.objects.filter(room__topic__name=q)[0:6]

    if q:
        rooms = Room.objects.filter(topic__name__contains = q)
        room_count = len(rooms)
    else:
        rooms = Room.objects.all()
        room_count = rooms.count()
    

    context =  {"rooms": rooms,'topics' :topics,'room_count' : room_count,'recent_messages':recent_messages}
    return render(request, 'base/room.html',context)


def room(request,id):
    room = Room.objects.get(id=id)
    all_messages = room.message_set.all()
    participants = room.participants.all()
    context = {'room': room,'all_messages' : all_messages,'participants':participants}
    if room:
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
    if request.method == 'POST':
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                return redirect('login')
        except Exception:
            messages.error(request,"Registration Issues")
        
    context = {"form" : form}
    return render(request,'base/login_register.html',context)

@login_required(login_url="Home")
def create_message(request,pk):
    room = Room.objects.get(id = pk)
    context = {"room" : room}
    room.participants.add(room.host)
    if request.method == 'POST':
        print(request.POST.get('message_body'))
        message = Message.objects.create(user = request.user,room = room,body = request.POST.get('message_body'))
        message.save()
        room.participants.add(request.user)
        return redirect('Room',id=room.id)

    return render(request,'base/iroom.html',context)

@login_required(login_url="Home")
def delete_message(request,pk):
    message = Message.objects.get(id=pk)
    room = message.room
    if message.user != request.user:
        return HttpResponse("You are not allow to Delete this message.")
    
    message.delete()
    return redirect("Room",id = room.id)

def user_profile(request,pk):
    print(pk)
    user = User.objects.get(id=pk)
    print(user)
    context = {"user" : user}
    if not user:
        return HttpResponse("User not found.")
    
    return render(request,'base/userProfile.html',context)

