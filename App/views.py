from django.shortcuts import render
from .models import * 

def index(request):
    return render(request, "Index.html")


def room(request, room_name, user_name):
    chats = []
    group = Group.objects.filter(name=room_name).first()
        # Room Not Exisits in datbase
    if(group):
        chats = Chat.objects.filter(group=room_name)
    else:
        # Room Exisits Already in datbase
        group = Group(name=room_name)
        group.save()
    return render(request, "Room.html", {'roomname': room_name, 'username': user_name,'chats':chats})