from datetime import timedelta
from django.db.models import F
from pdttracker.models import *
from pdttracker.ReportHandler import add_to_person_hrs

def start_timer(request, mode, time, project=None, defect=None):
	user = request.user
	if not Timer.objects.filter(mode=mode, created_for=project).exists():
		timer = Timer.objects.create(
			mode = mode,
			created_for = project,
		)
		return timer
	else: 
		return None

def end_timer(request, time, last_time, mode, project=None, defect=None):
	user = request.user
	if time is not None and last_time is not None:
		Timer.objects.filter(created_for=project, mode=mode).update(
		    num_hrs = F('num_hrs') + ((time - last_time) / timedelta(seconds=1) / 3600),
		)
	newTimer = Timer.objects.filter(created_for=project, mode=mode)
	if newTimer.count() > 0:
		return newTimer
	else:
		return None

def reset_timer(time, project=None, phase=None, iteration=None):
	if not iteration == None:
		rt = Report.objects.filter(iteration=iteration)
		ph = Phase.objects.filter(iteration=iteration)[:1].get()
		pj = Project.objects.filter(phase=ph)[:1].get()
	elif not phase == None:
		pj = Project.objects.filter(phase=phase)[:1].get()
	elif not project == None:
		pj = project

	devmode = Timer.objects.get(created_for=pj, mode='devmode')
	mgmtmode = Timer.objects.get(created_for=pj, mode='mgmtmode')
	defectmode = Timer.objects.get(created_for=pj, mode='defectmode')
	add_to_person_hrs(iteration, devmode.num_hrs, defectmode.num_hrs, mgmtmode.num_hrs)
	timers = Timer.objects.filter(created_for=pj)
	timers.num_hrs = 0
	timers.save()
