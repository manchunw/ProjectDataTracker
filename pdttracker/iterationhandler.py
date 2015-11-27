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
def create_iteration(phase, project):
   
    for num in range(1,project.num_iteration):
        newIteration = Iteration.objects.create(iteration_name= 'iteration'+ num, in_phase= phase, iteration_sequence=num)
        newReport = add_iteration_report(newIteration)
        newIteration.iteration_report = newReport
        newIteration.save()

        
    return null

def create_iteration(iteration_name, phase, project, seq):
    newIteration = Iteration.objects.create(iteration_name= iteration_name, in_phase= phase, iteration_sequence=seq)
    newReport = add_iteration_report(newIteration)
    newIteration.iteration_report = newReport
    newIteration.save()

        
    return newIteration

@login_required
def remove_iteration(id):
    i = Iteration.objects.get(id=id)
    i.delete()
    
    return null

@login_required
def close_iteration(id):
    i = Iteration.objects.get(id=id)
    i.delete()
    
    return null

@login_required
def get_iteration_list(phaseid):
    p=Phase.objects.filter(pk=phaseid)
    iteration_list= Iteration.objects.filter(in_phase=p)
   
    return iteration_list

def get_previous_iteration(curr_iteration):
    prev_seq = curr_iteration.iteration_sequence - 1
    if prev_seq == 0:
        return null
    else:
        prev = Iteration.objects.filter(phase=curr_iteration.in_phase).get(iteration_sequence=prev_seq)
   
    return prev

@login_required
def is_last_iteration(project):
    pj = Project.objects.select_related("current_iteration").get(pk = project.pk)
    if pj.current_iteration.iteration_sequence == pj.num_iteration:
        return True
    else:
        return False

@login_required
def startIteration(phase):
    iteration = Iteration.objects.get(iteration_sequence=1, in_phase=phase)
    project.update(current_iteration=iteration)
    return project