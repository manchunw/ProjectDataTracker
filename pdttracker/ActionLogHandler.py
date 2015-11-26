from django.utils import timezone
from django.db.models import Q
from pdttracker.models import *
from pdttracker.TimerHandler import start_timer, end_timer, switch_iteration

def add_action_log(request, logtype, project=None, phase=None, iteration=None, defect=None, user=None):
	lt = ActionLogDescription.objects.get(short_title=logtype)
	if user == None:
		user = request.user
	time = timezone.now()
	if project is not None:
		pj = Project.objects.select_related('current_phase', 'current_iteration').filter(pk=project.pk)
		if phase is None and pj[0].current_phase is not None:
			phase = pj[0].current_phase
		if iteration is None and pj[0].current_iteration is not None:
			iteration = pj[0].current_iteration
	if logtype == 'resumework': # still enter end_timer in management and removal mode with None defect value
		mode = get_current_mode(request)
		start_timer(request, time, mode, project, iteration)
	elif logtype == 'devmode' or logtype == 'mgmtmode' or logtype == 'defectmode':
		mode = get_current_mode(request)
		if mode is not None:
			end_timer(request, time, get_latest_timer_start(request), mode, project, iteration)
		start_timer(request, time, logtype, project, iteration)
	elif logtype == 'clsitn':
		switch_iteration(project, iteration)
	elif logtype == 'pausework': # still enter end_timer in management and removal mode with None defect value
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project, iteration)
	elif logtype == 'exitproj':
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project, iteration)
	elif logtype == 'logout':
		end_timer(request, time, get_latest_timer_start(request), get_current_mode(request), project, iteration)
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
	al = ActionLog.objects.select_related('project_tracked', 'action_log_description').filter(Q(action_log_created_by=user.id) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode) | Q(action_log_description=resumework))).order_by('-created_at')
	if len(al) > 0:
		return al[0].created_at
	else:
		return None

def get_current_mode(request, user=None):
	if user == None:
		user = request.user
	devmode = ActionLogDescription.objects.get(short_title='devmode')
	defectmode = ActionLogDescription.objects.get(short_title="defectmode")
	mgmtmode = ActionLogDescription.objects.get(short_title='mgmtmode')
	login = ActionLogDescription.objects.get(short_title='login')
	al = ActionLog.objects.select_related('action_log_description').filter(Q(action_log_created_by=user) & (Q(action_log_description=devmode) | Q(action_log_description=mgmtmode) | Q(action_log_description=defectmode))).order_by('-created_at')
	al2 = ActionLog.objects.select_related('action_log_description').filter(Q(action_log_created_by=user) & Q(action_log_description=login)).order_by('-created_at')
	if len(al) > 0 and len(al2) > 0:
		if al[0].created_at > al2[0].created_at: # must be in this login session
			return al[0].action_log_description.short_title
		else:
			return None
	else:
		return None
