from django.shortcuts import render , redirect
from .models import Room , Topic, Message
from .form import RoomForm
from django.contrib.auth.models import User
from  django.contrib.auth import authenticate , login, logout
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse

# Create your views here.

def loginRoom(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'user error')

        user = authenticate(request, username= username, password = password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'User or pw is not correct')
    context = {'page' :page}
    return render(request, 'base/login-register.html' , context)


def logoutuser(request):
    logout(request)
    return redirect('home')


def registerpage(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()

            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'An error occured during registration')


    

    form = UserCreationForm()
    return render(request, 'base/login-register.html', {'form' : form})

def home(request ):
   
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(Topic__name__icontains = q) |
        Q(name__icontains =q) |
        Q(discriptions__icontains =q)
                                )


    topics = Topic.objects.all()
    room_count = rooms.count()

    roommassage = Message.objects.filter(Q(room__name__icontains = q))




    context = {"rooms" : rooms , 'topics' : topics , 'room_count': room_count , "roommassage" : roommassage} 


    return render(request, 'base/home.html' , context)

def room(request, pk ):

    room = Room.objects.get(id = pk)

    Roommessages = room.message_set.all().order_by('-update')

    participants = room.participents.all()

    if request.method == 'POST':

        messag = Message.objects.create(
            user = request.user,
            room = room ,
            body = request.POST['body']

        )
        room.participents.add(request.user)
        return redirect('room' , pk= room.id)

    


    context = {'room' : room ,"Roommessages" :Roommessages , 'participants' :participants}
    return render(request , 'base/room.html' ,context)

@login_required(login_url='login')
def createroom(request):

    form = RoomForm()

    context = {'form' : form}
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')



    return render(request, 'base/room-form.html' , context)

@login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id = pk)
    form = RoomForm(instance= room)


    if request.user != room.user :
        return HttpResponse('you can not update it')


    if request.method == "POST":

        form = RoomForm(request.POST, instance= room)

        if form.is_valid:
            form.save()
            return redirect('home')

    context = {"form" : form}
    return render(request , 'base/room-form.html' , context)

@login_required(login_url='login')

def deleteroom(request,  pk):
    room = Room.objects.get(id = pk)

    if request.user != room.user :
        return HttpResponse('you can not update it')

    
    if request.method == "POST":
        room.delete()

        return redirect('home')
    
    return render(request, "base/delete.html" , {'obj':room})


@login_required(login_url='login')
def delete_comment(request,  pk):

    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse('you cat not delete comment')
    
    if request.method == "POST":
        message.delete()

        return redirect('home' )
    
    return render(request, 'base/delete.html')
    
    
def commentdelelte(request, pk):

    message = Message.objects.get(id = pk)
    

    

    


    return render(request, 'base/delete.html')
    

