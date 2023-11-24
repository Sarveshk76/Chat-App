from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import *
from .forms import *
from django.views.generic import *


@login_required
def home(request):
    user_obj = User.objects.get(email=request.user.email)
    return render(request, 'base.html', {'other_user': user_obj})

@login_required
def profile(request):
    userform = UserForm(request.POST)
    profileform = ProfileForm(request.POST)

    return render(request, 'main/profile.html', {'user_form':userform, 'profile_form':profileform})

@login_required
def chats(request):
    recent_users = User.objects.filter(last_login__date=date.today()).exclude(email=request.user.email)
    all_users = User.objects.exclude(email=request.user.email)
    return render(request, 'main/chats.html', {'all_users': all_users, 'recent_users': recent_users})

@login_required
def chatpage(request, username):
    recent_users = User.objects.filter(last_login__date=date.today()).exclude(email=request.user.email)
    all_users = User.objects.exclude(email=request.user.email)
    users = User.objects.exclude(first_name=username)
    user_obj = User.objects.get(first_name=username)
    return render(request, 'main/chats.html', {'users': users,
                                               'user_obj': user_obj,
                                               'all_users': all_users,
                                               'recent_users': recent_users})

@login_required
def contacts(request):
    return render(request, 'main/contacts.html')

@login_required
def groups(request):
    groups = UserGroup.objects.all()
    return render(request, 'main/groups.html', {'groups':groups})

@login_required
def settings(request):
    return render(request, 'main/settings.html')

