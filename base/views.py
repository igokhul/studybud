from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

from .models import Room, Topic, Messages, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.
from .models import Room
from .forms import RoomForm

# rooms = [
#     {'id' : 1, 'name' : 'Lets learn python!'},
#     {'id' : 2, 'name' : 'Lets learn django!'},
#     {'id' : 3, 'name' : 'Lets learn REST'},
# ]


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found')
        
        user = authenticate(request, email=email , password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password doest not match')

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')

    context = {'form' : form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__topic__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Messages.objects.filter(Q(room__topic__topic__icontains=q))

    context = {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count, 'room_messages' : room_messages}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def room(request, primary_key):
    room = Room.objects.get(id=primary_key) 
    room_messages = room.messages_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', primary_key=room.id)

    context = {'room' : room, 'room_messages' : room_messages, 'participants' : participants}
    return render(request, 'base/room.html', context)


def user_profile(request, primary_key):
    user = User.objects.get(id=primary_key)
    rooms = user.room_set.all()
    room_messages = user.messages_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'rooms' : rooms, 'room_messages' : room_messages, 'topics' : topics}
    return render(request, 'base/profile.html', context)


def create_room(request):
    form =  RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(topic=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )

        return redirect('home')
 
    context = {'form' : form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, primary_key):
    room = Room.objects.get(id=primary_key)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(topic=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form' : form, 'topics' : topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_room(request, primary_key):
    room = Room.objects.get(id=primary_key) 

    if request.user != room.host:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj':room}
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def delete_message(request, primary_key):
    message = Messages.objects.get(id=primary_key)

    if request.user != message.user:
        return HttpResponse('You are not allowed here')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {'obj' : message}    
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', primary_key=user.id)

    context = {'form' : form}
    return render(request, 'base/update_user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(topic__icontains=q)
    context = {'topics' : topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    room_messages = Messages.objects.all()
    context = {'room_messages' : room_messages}
    return render(request, 'base/activity.html', context)