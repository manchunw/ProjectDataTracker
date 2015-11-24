from datetime import timedelta
from pdttracker.models import Timer
from pdttracker.ActionLogHandler import get_latest_timer_start, get_current_mode
from pdttracker.ReportHandler import add_to_person_hrs

def start_timer(request, mode, time, project=null, defect=null):
	user = request.user
	if not Timer.objects.filter(mode=mode, created_for=project).exists():
		timer = Timer.objects.create(
			mode = mode,
			created_for = project,
		)
		return timer
	else: 
		return null

def end_timer(request, user, time, project=null, defect=null):
	user = request.user
	(action_log, last_time) = get_latest_timer_start(request)
	(mode, mode_time) = get_current_mode(request)
	timer = Timer.objects.get(created_for=project, mode=mode)
	timer.num_hrs = timer.num_hrs + ((time - last_time) / timedelta(seconds=1) / 3600)
	timer.save()
	newTimer = Timer.objects.get(created_for=project, mode=mode)
	return newTimer

def reset_timer(time, project=null, phase=null, iteration=null):
	if not iteration == null:
		rt = Report.objects.filter(iteration=iteration)
		ph = Phase.objects.filter(iteration=iteration)[:1].get()
		pj = Project.objects.filter(phase=ph)[:1].get()
	elif not phase == null:
		pj = Project.objects.filter(phase=phase)[:1].get()
	elif not project == null:
		pj = project

	devmode = Timer.objects.get(created_for=pj, mode='devmode')
	mgmtmode = Timer.objects.get(created_for=pj, mode='mgmtmode')
	defectmode = Timer.objects.get(created_for=pj, mode='defectmode')
	add_to_person_hrs(iteration, devmode.num_hrs, defectmode.num_hrs, mgmtmode.num_hrs)
	timers = Timer.objects.filter(created_for=pj)
	timers.num_hrs = 0
	timers.save()
