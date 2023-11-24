from django.urls import path
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('home/profile/', profile, name="profile"),
    path('home/chat/', chats, name="chats"),
    path('home/chat/<str:username>/', chatpage, name="chatpage"),
    path('home/group/', groups, name="groups"),
    path('home/contact/', contacts, name="contacts"),
    path('home/setting/', settings, name="settings"),
]
