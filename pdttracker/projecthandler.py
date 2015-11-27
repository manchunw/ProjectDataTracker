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
from pdttracker.ReportHandler import *
from pdttracker.phasehandler import *
from pdttracker.iterationhandler import *

def add_project(request,project_title, project_description,project_sloc,current_phase,current_iteration, assign_member, phase_names, iteration_names):
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

        phases = phase_names.split('\r\n')
        iterations = iteration_names.split('\r\n')
        newProject = Project.objects.create(
            project_title=project_title, 
            project_description=project_description, 
            project_sloc= project_sloc,
            current_phase= current_phase,
            current_iteration= current_iteration,
            in_charge_by = request.user,
            num_phase = len(phases),
            num_iteration = len(iterations)
        )
        newReport = add_project_report(newProject)
        newProject.project_report = newReport
        newProject.save()
        parr = []
        iarr = []
        c = 1
        for p in phases:
            parr.append(create_phase(p, newProject, c))
            d = 1
            for i in iterations:
                iarr.append(create_iteration(i, parr[c-1], newProject, d))
                d = d + 1
            c = c + 1

        for member in assign_member:
            add_developer_to_project(member, newProject)

        
        Project.objects.filter(pk=newProject.pk).update(
            current_phase=parr[0],
            current_iteration=iarr[0]
        )
        newProject2 = Project.objects.get(pk=newProject.pk)
        
        return newProject2

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










