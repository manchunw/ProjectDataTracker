from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from pdttracker.models import *
from pdttracker.tables import *
from django_tables2 import RequestConfig
from .forms import *
import datetime
from django.core.urlresolvers import reverse
from pdttracker.projecthandler import *

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
                        return redirect(reverse(project_view))
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
def selectMode(request):
    return render(request, 'selectMode.html', {})

@login_required
def developmentMode(request):
    return render(request, 'developmentMode.html', {})

@login_required
def welcome(request):
    return render(request, 'welcome.html', {})


@login_required
def project_view(request):
    table = ProjectTable(get_project_list(request))
#    table = ProjectTable(Project.objects.filter(in_charge_by=request.user))
    RequestConfig(request).configure(table)
    return render(request, "view_project.html", {"project": table})

@login_required
def modifyProject(request, pk):
    project = Project.objects.get(pk=pk)
    iteration = Iteration.objects.get(pk=project.current_iteration.pk)
    phase = Phase.objects.get(pk=project.current_phase.pk)
#     table = ProjectTable(get_project_list(request))
# #    table = ProjectTable(Project.objects.filter(in_charge_by=request.user))
#     RequestConfig(request).configure(table)
    return render(request, "modifyProject.html", {"project_name": project.project_title, "project_SLOC": project.project_sloc, "current_phase": phase.phase_name, "current_iteration": iteration.iteration_name, "num_phase": project.num_phase, "num_iteration": project.num_iteration})

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

@login_required
def addProject(request):
    form = ProjectForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)
        #assign_member = form.cleaned_data.get('assign_member')
        data =form.cleaned_data['assign_member']
#        in_charge_by = request.user
#        bar = Report.objects.create(report_title="on99")
#        instance.project_report=bar
#        instance.save()

        add_project(request, instance.project_title ,  instance.project_description,instance.project_sloc,instance.current_phase,instance.current_iteration, data)
        context = {
            "title": "Thank you"
    }


    return render(request, "project_form.html", context)

@login_required
def editProject(request, pk):
    instance = Project.objects.get(pk=pk)
    form = ProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse(project_view))
    return render(request, 'editProject.html', {'form': form})

@login_required
def removeProject(request, id):
    p = Project.objects.get(id=id)
    p.delete()

    return render(request, "view_project.html", context)

@login_required
def addIteration(request):
    title = 'Add Iteration Now'
    form = IterationForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)
        instance.save()
        context = {
            "title": "Thank you"
        }

    
    return render(request, "iteration_form.html", context)

@login_required
def editIteration(request, pk):
    instance = Iteration.objects.get(pk=pk)
    form = IterationForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse(iteration_view))
    return render(request, 'editIteration.html', {'form': form})

@login_required
def removeIteration(request, id):
    p = Project.objects.get(id=id)
    p.delete()

    return render(request, "view_iteration.html", context)

@login_required
def addDefect(request):
    title = 'Add Defect Now'
    form = DefectForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)
        instance.save()
        context = {
            "title": "Thank you"
    }


    return render(request, "defect_form.html", context)

@login_required
def editDefect(request, pk):
    instance = Defect.objects.get(pk=pk)
    form = DefectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(reverse(defect_view))
    return render(request, 'editDefect.html', {'form': form})


