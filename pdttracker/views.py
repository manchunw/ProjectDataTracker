# tested by Kelvin

from django.http import HttpResponse
import datetime

def home(request):
    s = "Hello World!"
    return HttpResponse(s)

def currentTime(request):
    s = datetime.datetime.now()
    return HttpResponse(s)
