from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from pdttracker.models import *
from pdttracker.tables import *
from django_tables2 import RequestConfig
from .forms import LoginForm
import datetime

def home(request):
    s = "Hello World!"
    return HttpResponse(s)

@csrf_protect
def auth_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    next_page = request.GET.get("next")
                    if next_page:
                    	return HttpResponseRedirect(next_page)
                    else:
                    	return HttpResponseRedirect("/now/")
                else:
                    return HttpResponse("Your PDT account is disabled.")
            else:
                return render_to_response("login.html", {"title": "Login", "error_message": "Invalid username and/or password.", "form": form}, RequestContext(request))
        else:
            return render_to_response("login.html", {"title": "Login", "error_message": "Server transmission error. Try again.", "form": form}, RequestContext(request))
    else:
        form = LoginForm()

        return render(request, 'login.html', {"title": "Login", "form": form})

@login_required
def auth_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def table_view(request, table_name):
	tname = str(table_name)
	if tname == 'defect':
		return defect_view(request)
	elif tname == 'project':
		return project_view(request)
	elif tname == 'iteration':
		return iteration_view(request)
	elif tname == 'phase':
		return phase_view(request)
	elif tname == 'action_log':
		return action_log_view(request)
	elif tname == 'user':
		return user_view(request)
	elif tname == 'userinfo':
		return user_info_view(request)
	else:
		return currentTime(request)

@login_required
def currentTime(request):
    s = datetime.datetime.now()
    return render(request, 'view_time.html', {"time": str(s)})

@login_required
def project_view(request):
    table = ProjectTable(Project.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_project.html", {"project": table})

@login_required
def iteration_view(request):
    table = IterationTable(Iteration.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_iteration.html", {"iteration": table})

@login_required
def phase_view(request):
    table = PhaseTable(Phase.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_phase.html", {"phase": table})

@login_required
def action_log_view(request):
    table = ActionLogTable(ActionLog.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_action_log.html", {"action_log": table})

@login_required
def user_view(request):
    table = UserTable(User.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_user.html", {"user": table})

@login_required
def user_info_view(request):
    table = UserInfoTable(Group.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_user_info.html", {"permission": table})

@login_required
def defect_view(request):
    table = DefectTable(Defect.objects.all())
    RequestConfig(request).configure(table)
    return render(request, "view_defect.html", {"defect": table})
