# tested by Kelvin

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime

def home(request):
    s = "Hello World!"
    return HttpResponse(s)

def login(request):
	return render(request, 'login.html', {})

@login_required
def currentTime(request):
    s = datetime.datetime.now()
    return HttpResponse(s)
