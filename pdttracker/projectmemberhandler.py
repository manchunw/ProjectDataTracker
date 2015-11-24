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


def add_developer_to_project(developer, project):
	newProjectMember= ProjectMember.objects.create(work_in= project, member=developer)

	return newProjectMember

@login_required
def remove_developer_from_project(developer, project):
	ProjectMember.objects.filter(work_in= project, member=developer).delete()

	return null

