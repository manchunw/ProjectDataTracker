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

@login_required
def create_iteration(phase):
   
    for num in range(1,5):
            Iteration.objects.create(iteration_name= 'iteration'+ num, in_phase= phase)

        
    return null

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