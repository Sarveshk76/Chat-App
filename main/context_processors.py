from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
import json
from datetime import date
from .models import *

def sections_processor(request):
    recent_users = User.objects.filter(last_login__date=date.today()).exclude(email=request.user.email)
    all_users = User.objects.exclude(email=request.user.email)
    all_users_json = serializers.serialize('json', all_users)
    users = User.objects.exclude(first_name=request.user.first_name)
    user_obj = User.objects.get(first_name=request.user.first_name)
    return {'users': users,
            'user_obj': user_obj,
            'all_users': all_users,
            'all_users_json': all_users_json,
            'recent_users': recent_users}