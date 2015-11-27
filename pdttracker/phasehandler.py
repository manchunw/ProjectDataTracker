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
from pdttracker.ReportHandler import *

@login_required
def create_phase(project):
   
    for num in range(1,5):
        newPhase = Phase.objects.create(phase_name= 'phase'+ num, in_project= project)
        newReport = add_phase_report(newPhase)
        newPhase.phase_report = newReport
        newPhase.save()

        
    return null

# @login_required
# def editProject(request, pk):
#     # instance = Project.objects.get(pk=pk)
#     # form = ProjectForm(request.POST or None, instance=instance)
#     # if form.is_valid():
#     #     form.save()
#         return redirect(reverse(project_view))

#     return editedProject

def create_phase(phase_name, project, seq):

    newPhase = Phase.objects.create(phase_name= phase_name, in_project= project, phase_sequence=seq)
    newReport = add_phase_report(newPhase)
    newPhase.phase_report = newReport
    newPhase.save()

        
    return newPhase

@login_required
def remove_phase(id):
    p = Phase.objects.get(id=id)
    p.delete()
    
    return null

@login_required
def close_phase(id):
    p = Phase.objects.get(id=id)
    
    return p

@login_required
def get_phase(id):
    p = Phase.objects.get(id=id)
   
    return p

@login_required
def get_phase_list(projectid):
    p=Project.objects.filter(pk=projectid)
    phase_list= Phase.objects.filter(project=p)
   
    return phase_list

@login_required
def is_last_phase(project):
    pj = Project.objects.select_related("current_phase").get(pk = project.pk)
    if pj.current_phase.phase_sequence == pj.num_phase:
        return True
    else:
        return False

@login_required
def switch_phase(project):
    pj = Project.objects.select_related("current_phase").filter(pk=project.pk)
    phase_seq = pj.current_phase.phase_sequence
    new_phase_seq = phase_seq + 1
    new_phase = Phase.objects.get(in_project=project, phase_sequence=new_phase_seq)
    project.update(current_phase=new_phase)
    return project

def get_previous_phase(curr_phase):
    prev_seq = curr_phase.phase_sequence - 1
    if prev_seq == 0:
        return null
    else:
        prev = Phase.objects.filter(project=curr_phase.in_project).get(phase_sequence=prev_seq)
   
    return prev