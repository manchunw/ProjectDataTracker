from django.db.models import Q
from pdttracker.models import ActionLogDescription, Timer, Project, Defect
from pdttracker.TimerHandler import start_timer, end_timer, reset_timer
import datetime

def add_action_log(request, logtype, project=null, phase=null, iteration=null, defect=null, user=null):
	lt = ActionLogDescription.objects.get(short_title=logtype)
	if user == null:
		user = request.user
	time = datetime.datetime.now()
	mode = get_current_mode(request)
	if logtype == 'resumework': # still enter end_timer in management and removal mode with null defect value
		start_timer(request, mode, time, project)
	elif logtype == 'pausework': # still enter end_timer in management and removal mode with null defect value
		end_timer(request, time, project)
	elif logtype == 'clsitn':
		reset_timer(time, project, phase, iteration)
	elif logtype == 'clsphe':
		reset_timer(time, project, phase)
	elif logtype == 'clsproj':
		reset_timer(time, project)
	elif logtype == 'enterproj':
		start_timer(request, mode, time, project, defect)
	elif logtype == 'exitproj':
		end_timer(request, time, project, defect)
	elif logtype == 'logout':
		end_timer(request, time, project, defect)
	actionLogDesc = ActionLogDescription.objects.create(
		action_log_created_by = user,
		action_log_description = lt,
		project_tracked = project,
		defect_tracked = defect,
		iteration_tracked = iteration,
		phase_tracked = phase,
	)
	return actionLogDesc

def get_current_mode(request, user=null):
	if user == null:
		user = request.user
	devmode = ActionLogDescription.objects.get(short_title='devmode')
	defectmode = ActionLogDescription.objects.get(short_title="defectmode")
	mgmtmode = ActionLogDescription.objects.get(short_title='mgmtmode')
	al = ActionLog.objects.select_related('action_log_description').filter(Q(action_log_created_by=user) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode))).order_by('-created_at')[:1].get()
	return (al.action_log_description.short_title, al.created_at)

def get_latest_timer_start(request, user=null):
	if user == null:
		user = request.user
	devmode = ActionLogDescription.objects.get(short_title='devmode')
	defectmode = ActionLogDescription.objects.get(short_title="defectmode")
	mgmtmode = ActionLogDescription.objects.get(short_title='mgmtmode')
	resumework = ActionLogDescription.objects.get(short_title='resumework')
	al = ActionLog.objects.select_related('created_for', 'action_log_description').filter(Q(action_log_created_by=user) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode) | Q(action_log_description=resumework))).order_by('-created_at')[:1].get()
	return (al, al.created_at)
