from datetime import timedelta
from django.db.models import F, Sum
from pdttracker.models import *
from pdttracker.ReportHandler import add_to_person_hrs

def start_timer(request, time, mode, project=None, iteration=None):
	if project is not None and iteration is not None:
		user = request.user
		if not Timer.objects.filter(mode=mode, timer_created_by__member=user, created_for=project, timing_iteration=iteration).exists():
			projectmember = None
			pm = ProjectMember.objects.filter(work_in=project, member=user)
			if pm.count() > 0:
				projectmember = pm[0]
			timer = Timer.objects.create(
				mode = mode,
				timer_created_by = projectmember,
				created_for = project,
				timing_iteration = iteration,
			)
			return timer
		else:
			timer = Timer.objects.get(mode=mode, timer_created_by__member=user, created_for=project, timing_iteration=iteration)
			return timer
	else: 
		return None

def end_timer(request, now_time, last_time, mode, project=None, iteration=None):
	user = request.user
	if now_time is not None and last_time is not None:
		Timer.objects.filter(mode=mode, timer_created_by__member=user, created_for=project, timing_iteration=iteration).update(
		    num_hrs = F('num_hrs') + ((now_time - last_time) / timedelta(seconds=1) / 3600),
		)
	newTimer = Timer.objects.filter(mode=mode, timer_created_by__member=user, created_for=project, timing_iteration=iteration)
	if newTimer.count() > 0:
		return newTimer
	else:
		return None

def switch_iteration(pj, old_iteration):
	if Timer.objects.filter(created_for=pj, timing_iteration=old_iteration, mode='devmode').exists():
		devmodeset = Timer.objects.get(created_for=pj, timing_iteration=old_iteration, mode='devmode').aggregate(Sum('num_hrs'))
		devmode = devmodeset['num_hrs__sum']
	else:
		devmode = 0
	if Timer.objects.filter(created_for=pj, timing_iteration=old_iteration, mode='mgmtmode').exists():
		mgmtmodeset = Timer.objects.get(created_for=pj, timing_iteration=old_iteration, mode='mgmtmode').aggregate(Sum('num_hrs'))
		mgmtmode = mgmtmodeset['num_hrs__sum']
	else:
		mgmtmode = 0
	if Timer.objects.filter(created_for=pj, timing_iteration=old_iteration, mode='defectmode').exists():
		defectmodeset = Timer.objects.get(created_for=pj, timing_iteration=old_iteration, mode='defectmode').aggregate(Sum('num_hrs'))
		defectmode = defectmodeset['num_hrs__sum']
	else:
		defectmode = 0
	add_to_person_hrs(old_iteration, devmode.num_hrs, defectmode.num_hrs, mgmtmode.num_hrs)
