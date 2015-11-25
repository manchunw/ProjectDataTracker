import datetime
from django.db.models import Q
from pdttracker.models import *
from pdttracker.TimerHandler import start_timer, end_timer, reset_timer

def add_action_log(request, logtype, project=None, phase=None, iteration=None, defect=None, user=None):
	lt = ActionLogDescription.objects.get(short_title=logtype)
	if user == None:
		user = request.user
	time = datetime.datetime.now()
	if logtype == 'resumework': # still enter end_timer in management and removal mode with None defect value
		mode = get_current_mode(request)
		start_timer(request, mode, time, project)
	elif logtype == 'pausework': # still enter end_timer in management and removal mode with None defect value
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project)
	elif logtype == 'clsitn':
		reset_timer(time, project, phase, iteration)
	elif logtype == 'clsphe':
		reset_timer(time, project, phase)
	elif logtype == 'clsproj':
		reset_timer(time, project)
	elif logtype == 'enterproj':
		mode = get_current_mode(request)
		start_timer(request, mode, time, project, defect)
	elif logtype == 'exitproj':
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project, defect)
	elif logtype == 'logout':
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project, defect)
	actionLogDesc = ActionLog.objects.create(
		action_log_created_by = user,
		action_log_description = lt,
		project_tracked = project,
		defect_tracked = defect,
		iteration_tracked = iteration,
		phase_tracked = phase,
	)
	return actionLogDesc

def get_latest_timer_start(request, user=None):
	if user == None:
		user = request.user
	devmode = ActionLogDescription.objects.get(short_title='devmode')
	defectmode = ActionLogDescription.objects.get(short_title="defectmode")
	mgmtmode = ActionLogDescription.objects.get(short_title='mgmtmode')
	resumework = ActionLogDescription.objects.get(short_title='resumework')
	al = ActionLog.objects.select_related('created_for', 'action_log_description').filter(Q(action_log_created_by=user.id) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode) | Q(action_log_description=resumework))).order_by('-created_at')
	if al.count() > 0:
		return al[0].created_at
	else:
		return None

def get_current_mode(request, user=None):
	if user == None:
		user = request.user
	devmode = ActionLogDescription.objects.get(short_title='devmode')
	defectmode = ActionLogDescription.objects.get(short_title="defectmode")
	mgmtmode = ActionLogDescription.objects.get(short_title='mgmtmode')
	al = ActionLog.objects.select_related('action_log_description').filter(Q(action_log_created_by=user) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode))).order_by('-created_at')
	if al.count() > 0:
		return al[0].action_log_description.short_title
	else:
		return None
