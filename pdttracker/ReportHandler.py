from django.db.models import Count
from django.db.models import F
from pdttracker.models import Iteration, Phase, Project, Report
from .ReportPolicy import *

def add_iteration_report(iteration):
	"""Add iteration report when an iteration is created"""
	title = iteration.iteration_title + get_report_suffix()
	i = Iteration.objects.get(pk=iteration.pk)
	current_phase = Phase.objects.filter(iteration = i)[:1].get()
	# dsloc = 0
	if i.iteration_sequence == 1:
		# if the iteration is the first one, get the previous phase
		if current_phase.phase_sequence == 1:
			# if the phase is the first one, assign iteration to zero
			dsloc = 0
		else:
			# get the dsloc of the current phase
			current_phase_report = Report.objects.filter(phase = current_phase)[:1].get()
			dsloc = current_phase_report.dsloc
	else:
		# get the dsloc of the previous iteration
		prev_i = Iteration.get_previous_iteration(iteration)
		dsloc = prev_i.dsloc
	t = str(title)
	r = Report.objects.create(report_title=t, delivered_sloc=dsloc)
	obj = Report.objects.get(title__exact=t)
	return obj

def add_phase_report(phase):
	"""Add phase report when a phase is created"""
	title = iteration.phase_title + get_report_suffix()
	p = Phase.objects.get(pk=phase.pk)
	if p.phase_sequence == 1:
		dsloc = 0
	else:
		# get the dsloc of the previous iteration
		prev_p = Phase.get_previous_phase(iteration)
		dsloc = prev_p.dsloc
	t = str(title)
	r = Report(report_title=t, dsloc=dsloc)
	r.save()
	obj = Report.objects.get(title__exact=t)
	return obj

def add_project_report(project):
	"""Add project report when a project is created"""
	title = project.project_title + get_report_suffix()
	r = Report(report_title=title, dsloc=0)
	r.save()
	obj = Report.objects.get(title__exact=title)
	return obj

def add_to_delivered_sloc(iteration, sloc):
	Report.objects.filter(iteration = iteration).update(
		delivered_sloc = F('delivered_sloc') + sloc,
	)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(
		delivered_sloc = F('delivered_sloc') + sloc,
	)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(
		delivered_sloc = F('delivered_sloc') + sloc,
	)
	# """Add to delivered sloc after an iteration is complete"""
	# # update iteration report dsloc
	# i = Iteration.objects.get(pk=iteration.pk)
	# r = Report.objects.filter(iteration = iteration)[:1].get()
	# old_value = i.sloc
	# new_value = r.delivered_sloc + sloc - old_value
	# new_dsloc_per_person_mths = new_value / r.person_mths
	# new_defect_density = r.defects_injected / new_value / 1000
	# r.update(delivered_sloc=new_value, delivered_sloc_per_person_mths=new_dsloc_per_person_mths, defect_density_per_ksloc=new_defect_density)
	# # update phase report sloc
	# ph = Phase.objects.filter(iteration = iteration)[:1].get()
	# ph_r = Report.objects.filter(phase = ph)[:1].get()
	# new_ph_value = ph_r.delivered_sloc + new_value - old_value
	# new_ph_dsloc_per_person_mths = new_ph_value / ph_r.person_mths
	# new_ph_defect_density = ph_r.defects_injected / new_ph_value / 1000
	# ph_r.update(delivered_sloc=new_ph_value, delivered_sloc_per_person_mths=new_ph_dsloc_per_person_mths, defect_density_per_ksloc=new_ph_defect_density)
	# # update project report sloc
	# pj = Project.objects.filter(phase = ph)[:1].get()
	# pj_r = Report.objects.filter(project = pj)[:1].get()
	# new_pj_value = pj_r.delivered_sloc + new_value - old_value
	# new_pj_dsloc_per_person_mths = new_pj_value / pj_r.person_mths
	# new_pj_defect_density = pj_r.defects_injected / new_pj_value / 1000
	# pj_r.update(delivered_sloc=new_pj_value, delivered_sloc_per_person_mths=new_pj_dsloc_per_person_mths, defect_density_per_ksloc=new_pj_defect_density)

def add_to_person_hrs(iteration, ph_devmode, ph_defectmode, ph_mgmtmode):
	"""Add to person hours after an iteration is complete"""
	Report.objects.filter(iteration = iteration).update(
		person_hrs_defectmode = F('person_hrs_defectmode') + ph_defectmode,
		person_hrs_mgmtmode = F('person_hrs_mgmtmode') + ph_mgmtmode,
		person_hrs_devmode = F('person_hrs_devmode') + ph_devmode,
	)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(
		person_hrs_defectmode = F('person_hrs_defectmode') + ph_defectmode,
		person_hrs_mgmtmode = F('person_hrs_mgmtmode') + ph_mgmtmode,
		person_hrs_devmode = F('person_hrs_devmode') + ph_devmode,
	)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(
		person_hrs_defectmode = F('person_hrs_defectmode') + ph_defectmode,
		person_hrs_mgmtmode = F('person_hrs_mgmtmode') + ph_mgmtmode,
		person_hrs_devmode = F('person_hrs_devmode') + ph_devmode,
	)

	# # update iteration report person hours
	# r = Report.objects.filter(iteration = iteration)[:1].get()
	# old_phrs_dev = r.person_hrs_devmode
	# new_phrs_dev = old_phrs_dev + ph_devmode
	# old_phrs_def = r.person_hrs_defectmode
	# new_phrs_def = old_phrs_def + ph_defectmode
	# old_phrs_mgt = r.person_hrs_mgmtmode
	# new_phrs_mgt = old_phrs_mgt + ph_mgmtmode
	# old_value = old_phrs_dev + old_phrs_def + old_phrs_mgt
	# new_value = new_phrs_dev + new_phrs_def + new_phrs_mgt
	# new_person_mths = new_value * get_person_mth_ratio()
	# new_dsloc_per_person_mths = r.delivered_sloc / new_person_mths
	# new_inject_rate = r.defects_injected / new_phrs_dev
	# new_removal_rate = r.defects_removed / new_phrs_def
	# r.update(
	# 	person_hrs_devmode=new_phrs_dev,
	# 	person_hrs_mgmtmode=new_phrs_mgt,
	# 	person_hrs_defectmode=new_phrs_def, 
	# 	delivered_sloc_per_person_mths=new_dsloc_per_person_mths, 
	# 	person_mths=new_person_mths, 
	# 	injection_rate_per_person_hrs=new_inject_rate, 
	# 	removal_rate_per_person_hrs=new_removal_rate,
	# )
	# # update phase report person hours
	# ph = Phase.objects.filter(iteration = iteration)[:1].get()
	# ph_r = Report.objects.filter(phase = ph)[:1].get()
	# new_ph_phrs_dev = ph_r.person_hrs_devmode + new_phrs_dev
	# new_ph_phrs_mgt = ph_r.person_hrs_mgmtmode + new_phrs_mgt
	# new_ph_phrs_def = ph_r.person_hrs_defectmode + new_phrs_def
	# new_ph_value = new_value + ph_r.person_hrs_defectmode + ph_r.person_hrs_mgmtmode + ph_r.person_hrs_devmode
	# new_person_mths = new_ph_value * get_person_mth_ratio()
	# new_dsloc_per_person_mths = ph_r.delivered_sloc / new_ph_person_mths
	# new_inject_rate = ph_r.defects_injected / new_ph_phrs_dev
	# new_removal_rate = ph_r.defects_removed / new_ph_phrs_def
	# ph_r.update(
	# 	person_hrs_devmode=new_ph_phrs_dev,
	# 	person_hrs_mgmtmode=new_ph_phrs_mgt,
	# 	person_hrs_defectmode=new_ph_phrs_def, 
	# 	delivered_sloc_per_person_mths=new_dsloc_per_person_mths, 
	# 	person_mths=new_person_mths, 
	# 	injection_rate_per_person_hrs=new_inject_rate, 
	# 	removal_rate_per_person_hrs=new_removal_rate,
	# )
	# # update project report person hours
	# pj = Project.objects.filter(phase = ph)[:1].get()
	# pj_r = Report.objects.filter(project = pj)[:1].get()
	# new_pj_phrs_dev = pj_r.person_hrs_devmode + new_phrs_dev
	# new_pj_phrs_mgt = pj_r.person_hrs_mgmtmode + new_phrs_mgt
	# new_pj_phrs_def = pj_r.person_hrs_defectmode + new_phrs_def
	# new_pj_value = new_value + pj_r.person_hrs_defectmode + pj_r.person_hrs_mgmtmode + pj_r.person_hrs_devmode
	# new_person_mths = new_pj_value * get_person_mth_ratio()
	# new_dsloc_per_person_mths = pj_r.delivered_sloc / new_pj_person_mths
	# new_inject_rate = pj_r.defects_injected / new_pj_phrs_dev
	# new_removal_rate = pj_r.defects_removed / new_pj_phrs_def
	# pj_r.update(
	# 	person_hrs_devmode=new_pj_phrs_dev,
	# 	person_hrs_mgmtmode=new_pj_phrs_mgt,
	# 	person_hrs_defectmode=new_pj_phrs_def, 
	# 	delivered_sloc_per_person_mths=new_dsloc_per_person_mths, 
	# 	person_mths=new_person_mths, 
	# 	injection_rate_per_person_hrs=new_inject_rate, 
	# 	removal_rate_per_person_hrs=new_removal_rate,
	# )

def add_defect_update(iteration):
	Report.objects.filter(iteration = iteration).update(defects_injected=F('defects_injected')+1)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(defects_injected=F('defects_injected')+1)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(defects_injected=F('defects_injected')+1)
	# """Update defect counter after a defect is added"""
	# r = Report.objects.filter(iteration = iteration)[:1].get()
	# new_value = r.defects_injected + 1
	# new_inject_rate = new_value / r.person_hrs_devmode
	# new_defect_density = new_value / r.delivered_sloc / 1000
	# r.update(defects_injected=new_value, injection_rate_per_person_hrs=new_inject_rate, defect_density_per_ksloc=new_defect_density)
	# ph = Phase.objects.filter(iteration = iteration)[:1].get()
	# ph_r = Report.objects.filter(phase = ph)[:1].get()
	# new_ph_value = ph_r.defects_injected + 1
	# new_ph_inject_rate = new_ph_value / ph_r.person_hrs_devmode
	# new_ph_defect_density = new_ph_value / ph_r.delivered_sloc / 1000
	# ph_r.update(defects_injected=new_ph_value, injection_rate_per_person_hrs=new_ph_inject_rate, defect_density_per_ksloc=new_ph_defect_density)
	# pj = Project.objects.filter(phase = ph)[:1].get()
	# pj_r = Report.objects.filter(project = pj)[:1].get()
	# new_pj_value = pj_r.defects_injected + 1
	# new_pj_inject_rate = new_pj_value / pj_r.person_hrs_devmode
	# new_pj_defect_density = new_pj_value / pj_r.delivered_sloc / 1000
	# pj_r.update(defects_injected=new_pj_value, injection_rate_per_person_hrs=new_pj_inject_rate, defect_density_per_ksloc=new_pj_defect_density)
	
def remove_defect_update(iteration):
	Report.objects.filter(iteration = iteration).update(defects_removed=F('defects_removed')+1)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(defects_removed=F('defects_removed')+1)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(defects_removed=F('defects_removed')+1)
	# """Update defect counter after a defect is added"""
	# r = Report.objects.filter(iteration = iteration)[:1].get()
	# new_value = r.defects_removed + 1
	# new_removal_rate = new_value / r.person_hrs_defectmode
	# new_defect_density = new_value / r.delivered_sloc / 1000
	# r.update(defects_injected=new_value, injection_rate_per_person_hrs=new_inject_rate, defect_density_per_ksloc=new_defect_density)
	# ph = Phase.objects.filter(iteration = iteration)[:1].get()
	# ph_r = Report.objects.filter(phase = ph)[:1].get()
	# new_ph_value = ph_r.defects_injected + 1
	# new_ph_inject_rate = new_ph_value / ph_r.person_hrs_defectmode
	# new_ph_defect_density = new_ph_value / ph_r.delivered_sloc / 1000
	# ph_r.update(defects_injected=new_ph_value, injection_rate_per_person_hrs=new_ph_inject_rate, defect_density_per_ksloc=new_ph_defect_density)
	# pj = Project.objects.filter(phase = ph)[:1].get()
	# pj_r = Report.objects.filter(project = pj)[:1].get()
	# new_pj_value = pj_r.defects_injected + 1
	# new_pj_inject_rate = new_pj_value / pj_r.person_hrs_defectmode
	# new_pj_defect_density = new_pj_value / pj_r.delivered_sloc / 1000
	# pj_r.update(defects_injected=new_pj_value, injection_rate_per_person_hrs=new_pj_inject_rate, defect_density_per_ksloc=new_pj_defect_density)

def generate_iteration_report(iteration):
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	pj = Project.objects.filter(phase = ph)[:1].get()
	pj_r = Report.objects.filter(project = pj)[:1].get()
	Report.objects.filter(iteration = iteration).update(
		delivered_sloc_of_project = F('delivered_sloc') / pj_r.delivered_sloc,
		person_mths = (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) / get_person_mth_ratio(),
		person_mths_of_project = (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) / (pj_r.person_hrs_defectmode + pj_r.person_hrs_devmode + pj_r.person_hrs_mgmtmode),
		delivered_sloc_per_person_mths = F('delivered_sloc') / (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) * get_person_mth_ratio(),
		injection_rate_per_person_hrs = F('defects_injected') / F('person_hrs_devmode'),
		removal_rate_per_person_hrs = F('defects_removed') / F('person_hrs_defectmode'),
		defect_density_per_ksloc = F('defects_injected') / pj_r.delivered_sloc * 1000,
	)
	r = Report.objects.filter(iteration = iteration)[:1].get()
	return r

def generate_phase_report(phase):
	pj = Project.objects.filter(phase = phase)[:1].get()
	pj_r = Report.objects.filter(project = pj)[:1].get()
	Report.objects.filter(phase = phase).update(
		delivered_sloc_of_project = F('delivered_sloc') / pj_r.delivered_sloc,
		person_mths = (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) / get_person_mth_ratio(),
		person_mths_of_project = (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) / (pj_r.person_hrs_defectmode + pj_r.person_hrs_devmode + pj_r.person_hrs_mgmtmode),
		delivered_sloc_per_person_mths = F('delivered_sloc') / (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) * get_person_mth_ratio(),
		injection_rate_per_person_hrs = F('defects_injected') / F('person_hrs_devmode'),
		removal_rate_per_person_hrs = F('defects_removed') / F('person_hrs_defectmode'),
		defect_density_per_ksloc = F('defects_injected') / pj_r.delivered_sloc * 1000,
	)
	r = Report.objects.filter(phase = phase)[:1].get()
	return r

def generate_project_report(project):
	Report.objects.filter(project = project).update(
		delivered_sloc_of_project = 1,
		person_mths = (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) / get_person_mth_ratio(),
		person_mths_of_project = 1,
		delivered_sloc_per_person_mths = F('delivered_sloc') / (F('person_hrs_defectmode') + F('person_hrs_devmode') + F('person_hrs_mgmtmode')) * get_person_mth_ratio(),
		injection_rate_per_person_hrs = F('defects_injected') / F('person_hrs_devmode'),
		removal_rate_per_person_hrs = F('defects_removed') / F('person_hrs_defectmode'),
		defect_density_per_ksloc = F('defects_injected') / F('delivered_sloc') * 1000,
	)
	r = Report.objects.filter(project = project)[:1].get()
	return r

def get_report(reporttype, entity):
	"""get report given report type and the object"""
	if reporttype == 'project':
		r = generate_project_report(entity)
	elif reporttype == 'phase':
		r = generate_phase_report(entity)
	elif reporttype == 'iteration':
		r = generate_project_report(entity)
	return r

def get_yield(project):
	"""get yield given a pk value of a project"""
	ds = Defect.objects.filter(recorded_in=project).values('iteration_injected__iteration_name', 'iteration_resolved__iteration_name').order_by().annotate(num=Count('pk'))
	ph = Phase.objects.filter(project=project).all()
	iterations = Iteration.objects.filter(phase=ph).values('iteration_sequence').order_by('in_phase__phase_sequence', 'iteration_sequence')
	inject_num = {}
	resolve_num = {}
	resolve_last_num = {}
	inject_iteration = []
	resolve_iteration = []
	# initialize values
	for i in iterations:
		inject_num[str(i.iteration_name)] = 0
	for i in iterations:
		resolve_num[str(i.iteration_name)] = 0
	for d in ds:
		# populate total inject numbers on the bottom of the table
		inject_num[str(d['iteration_injected__iteration_name'])] += int(d['num'])
		# populate total resolve numbers on the right of the table
		resolve_num[str(d['iteration_resolved__iteration_name'])] += int(d['num'])
		# populate the last row of defect resolved, for escape calculation
		resolve_last_num[str(d['iteration_injected__iteration_name'])] = int(d['num'])
		if str(d['iteration_injected__iteration_name']) not in inject_iteration:
			inject_iteration.append(str(d['iteration_injected__iteration_name']))
		if str(d['iteration_resolved__iteration_name']) not in resolve_iteration:
			resolve_iteration.append(str(d['iteration_resolved__iteration_name']))
	# populate escape number and prepare for yield calculation
	m = 0
	n = 0
	cumulative_inject_num = {}
	cumulative_resolve_num = {}
	escape_arr = []
	for i in len(inject_iteration):
		m += inject_num[inject_iteration[i]]
		cumulative_inject_num[inject_iteration[i]] = m
		escape_arr[i] = round(resolve_last_num[inject_iteration[i]] * (1 - 0.8))
		cumulative_inject_num[inject_iteration[i]] += escape_arr[i]
	for i in len(resolve_iteration):
		n += resolve_num[resolve_iteration[i]]
		cumulative_resolve_num[resolve_iteration[i]] = n
	# populate yield
	yield_arr = []
	for i in len(inject_iteration):
		if i == 0:
			yield_arr.append(resolve_num[resolve_iteration[i]] / cumulative_inject_num[inject_iteration[i]])
		else:
			yield_arr.append(resolve_num[resolve_iteration[i]] / (cumulative_inject_num[inject_iteration[i]] - cumulative_resolve_num[resolve_iteration[i-1]]))
	# populate table-convenient output
	return (ds, inject_iteration, resolve_iteration, inject_num, resolve_num, escape_arr, yield_arr)