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
from .projectmemberhandler import *
from pdttracker.GroupHandler import *

def add_project(request,project_title, project_description,project_sloc,current_phase,current_iteration, assign_member):
#    form = ProjectForm(request.POST or None)
#    context = {
#        "form": form
#    }
#    if form.is_valid():
#        instance = form.save(commit=False)
#        instance.in_charge_by = request.user
#        newReport = ReportHandler.add_project_report()
##       newReport = Report.objects.create(report_title="on99")
#        instance.project_report=newReport
#        instance.save()
#        context = {
#            "title": "Thank you"
#    }
        # newReport = Report.objects.create(report_title="on99")
        newProject = Project.objects.create(project_title=project_title, 
        project_description=project_description, 
        project_sloc= project_sloc,
        current_phase= current_phase,
        current_iteration= current_iteration,
        in_charge_by = request.user
        )
        newReport = ReportHandler.add_project_report(newProject)
        newProject.project_report = newReport
        newProject.save()
        for member in assign_member:
            add_developer_to_project(member, newProject)
        
        return newProject

# @login_required
# def editProject(request, pk):
#     # instance = Project.objects.get(pk=pk)
#     # form = ProjectForm(request.POST or None, instance=instance)
#     # if form.is_valid():
#     #     form.save()
#         return redirect(reverse(project_view))

#     return editedProject

@login_required
def remove_project(id):
    p = Project.objects.get(id=id)
    p.delete()
    
    return null

@login_required
def close_project(id):
    p = Project.objects.get(id=id)
    p.update(is_active=False)
    
    return p

@login_required
def get_project(id):
    p = Project.objects.get(id=id)
   
    return p

@login_required
def get_project_list(request):
    if in_group(request.user, "Administrator"):
        project_list=   Project.objects.all()
    elif in_group(request.user, "Manager"):
        project_list=Project.objects.filter(in_charge_by=request.user)
    elif in_group(request.user, "Developer"):
        pm = ProjectMember.objects.filter(member=request.user)
        project_list= Project.objects.filter(projectmember=pm)
    else:
        project_list = None
    return project_list










