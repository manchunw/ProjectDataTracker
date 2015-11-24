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
def add_defect(defect_title, defect_type,defect_description,defect_remarks,recorded_in,iteration_injected):
	newDefect= Defect.objects.create(
	defect_title = defect_title, defect_type = defect_type,
	defect_description = defect_description,
	defect_remarks = defect_remarks,
	recorded_in = recorded_in,
	iteration_injected = iteration_injected)

	return newDefect

@login_required
def get_defect(id):
    d = Defect.objects.get(id=id)
   
    return d

@login_required
def get_defect_list(projectid, iterationid):
    p=Project.objects.filter(pk=projectid)
    i=iteration.ojects.filter(pk=iterationid)
    defect_list= Phase.objects.filter(recorded_in=p, iteration_injected=i)
   	
    return defect_list

