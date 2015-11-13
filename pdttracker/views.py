# tested by Kelvin

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
import datetime

def home(request):
    s = "Hello World!"
    return HttpResponse(s)

@csrf_protect
def auth_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/now/")
            else:
                return HttpResponse("Your PDT account is disabled.")
        else:
            print ("Invalid login details: "+ username + ", "+ password)
            return render_to_response("login.html", {"error_message": "Invalid username and/or password."}, RequestContext(request))
    else:
        return render(request, "login.html", {})

@login_required
def auth_logout(request):
	logout(request)
	return HttpResponseRedirect("/login/")

@login_required
def currentTime(request):
    s = datetime.datetime.now()
    return HttpResponse(s)

