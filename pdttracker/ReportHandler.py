from django.db.models import Count
from pdttracker.models import Iteration, Phase, Project, Report

def add_iteration_report(iteration, title):
	"""Add iteration report when an iteration is created"""
	i = Iteration.objects.get(pk=iteration.pk)
	current_phase = Phase.objects.filter(iteration = i)[:1].get()
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
	r = Report(report_title=t, dsloc=dsloc)
	r.save()
	obj = Report.objects.get(title__exact=t)
	return obj

def add_phase_report(phase, title):
	"""Add phase report when a phase is created"""
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

def add_project_report(project, title):
	"""Add project report when a project is created"""
	r = Report(report_title=t, dsloc=0)
	r.save()
	obj = Report.objects.get(title__exact=t)
	return obj

def add_to_delivered_sloc(iteration, sloc):
	"""Add to delivered sloc after an iteration is complete"""
	# update iteration report dsloc
	i = Iteration.objects.get(pk=iteration.pk)
	r = Report.objects.filter(iteration = iteration)[:1].get()
	old_value = i.sloc
	new_value = r.delivered_sloc + sloc - old_value
	new_dsloc_per_person_mths = new_value / r.person_mths
	new_defect_density = r.defects_injected / new_value / 1000
	r.update(delivered_sloc=new_value, delivered_sloc_per_person_mths=new_dsloc_per_person_mths, defect_density_per_ksloc=new_defect_density)
	# update phase report sloc
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	ph_r = Report.objects.filter(phase = ph)[:1].get()
	new_ph_value = ph_r.delivered_sloc + new_value - old_value
	new_ph_dsloc_per_person_mths = new_ph_value / ph_r.person_mths
	new_ph_defect_density = ph_r.defects_injected / new_ph_value / 1000
	ph_r.update(delivered_sloc=new_ph_value, delivered_sloc_per_person_mths=new_ph_dsloc_per_person_mths, defect_density_per_ksloc=new_ph_defect_density)
	# update project report sloc
	pj = Project.objects.filter(phase = ph)[:1].get()
	pj_r = Report.objects.filter(project = pj)[:1].get()
	new_pj_value = pj_r.delivered_sloc + new_value - old_value
	new_pj_dsloc_per_person_mths = new_pj_value / pj_r.person_mths
	new_pj_defect_density = pj_r.defects_injected / new_pj_value / 1000
	pj_r.update(delivered_sloc=new_pj_value, delivered_sloc_per_person_mths=new_pj_dsloc_per_person_mths, defect_density_per_ksloc=new_pj_defect_density)

def add_to_person_hrs(iteration, ph_to_add):
	"""Add to person hours after an iteration is complete"""
	# update iteration report person hours
	r = Report.objects.filter(iteration = iteration)[:1].get()
	old_value = r.person_hrs
	new_value = old_value + ph_to_add
	new_person_mths = new_value * get_person_mth_ratio()
	new_dsloc_per_person_mths = r.delivered_sloc / new_value
	new_inject_rate = r.defects_injected / new_value
	r.update(person_hrs=new_value, delivered_sloc_per_person_mths=new_dsloc_per_person_mths, person_mths=new_person_mths, injection_rate_per_person_hrs=new_inject_rate)
	# update phase report person hours
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	ph_r = Report.objects.filter(phase = ph)[:1].get()
	new_ph_value = ph_r.delivered_sloc + new_value - old_value
	new_ph_person_mths = new_ph_value * get_person_mth_ratio()
	new_ph_dsloc_per_person_mths = ph_r.delivered_sloc / new_ph_value
	new_ph_inject_rate = ph_r.defects_injected / new_ph_value
	ph_r.update(person_hrs=new_ph_value, delivered_sloc_per_person_mths=new_ph_dsloc_per_person_mths, person_mths=new_ph_person_mths, injection_rate_per_person_hrs=new_ph_inject_rate)
	# update project report person hours
	pj = Project.objects.filter(phase = ph)[:1].get()
	pj_r = Report.objects.filter(project = pj)[:1].get()
	new_pj_value = pj_r.delivered_sloc + new_value - old_value
	new_pj_person_mths = new_value * get_person_mth_ratio()
	new_pj_dsloc_per_person_mths = pj_r.delivered_sloc / new_pj_value
	new_pj_inject_rate = pj_r.defects_injected / new_pj_value
	pj_r.update(person_hrs=new_pj_value, delivered_sloc_per_person_mths=new_pj_dsloc_per_person_mths, person_mths=new_pj_person_mths, injection_rate_per_person_hrs=new_pj_inject_rate)

def add_defect_update(iteration):
	"""Update defect counter after a defect is added"""
	r = Report.objects.filter(iteration = iteration)[:1].get()
	new_value = r.defects_injected + 1
	new_inject_rate = new_value / r.person_hrs
	new_defect_density = new_value / r.delivered_sloc / 1000
	r.update(defects_injected=new_value, injection_rate_per_person_hrs=new_inject_rate, defect_density_per_ksloc=new_defect_density)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	ph_r = Report.objects.filter(phase = ph)[:1].get()
	new_ph_value = ph_r.defects_injected + 1
	new_ph_inject_rate = new_ph_value / ph_r.person_hrs
	new_ph_defect_density = new_ph_value / ph_r.delivered_sloc / 1000
	ph_r.update(defects_injected=new_ph_value, injection_rate_per_person_hrs=new_ph_inject_rate, defect_density_per_ksloc=new_ph_defect_density)
	pj = Project.objects.filter(phase = ph)[:1].get()
	pj_r = Report.objects.filter(project = pj)[:1].get()
	new_pj_value = pj_r.defects_injected + 1
	new_pj_inject_rate = new_pj_value / pj_r.person_hrs
	new_pj_defect_density = new_pj_value / pj_r.delivered_sloc / 1000
	pj_r.update(defects_injected=new_pj_value, injection_rate_per_person_hrs=new_pj_inject_rate, defect_density_per_ksloc=new_pj_defect_density)

def get_report(report_pk):
	"""get report given a pk value"""
	r = Report.objects.get(pk=report_pk)
	return r

def get_yield(project):
	"""get yield given a pk value of a project"""
	ds = Defect.objects.filter(recorded_in=project).values('iteration_injected', 'iteration_resolved').order_by().annotate(num=Count('pk'))
	iterations = Iteration.objects.filter(project=project).order_by('iteration_sequence')
	inject_num = {}
	resolve_num = {}
	resolve_last_num = {}
	inject_iteration = []
	resolve_iteration = []
	for i in iterations:
		inject_num[str(i)] = 0
	for i in iterations:
		resolve_num[str(i)] = 0
	for d in ds:
		inject_num[str(d['iteration_injected'])] += int(d['num'])
		resolve_num[str(d['iteration_resolved'])] += int(d['num'])
		resolve_last_num[str(d['iteration_injected'])] = int(d['num'])
		if str(d['iteration_injected']) not in inject_iteration:
			inject_iteration.append(str(d['iteration_injected']))
		if str(d['iteration_resolved']) not in resolve_iteration:
			resolve_iteration.append(str(d['iteration_resolved']))
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
	yield_arr = []
	for i in len(inject_iteration):
		if i == 0:
			yield_arr.append(resolve_num[resolve_iteration[i]] / cumulative_inject_num[inject_iteration[i]])
		else:
			yield_arr.append(resolve_num[resolve_iteration[i]] / (cumulative_inject_num[inject_iteration[i]] - cumulative_resolve_num[resolve_iteration[i-1]]))
	return (ds, inject_iteration, resolve_iteration, inject_num, resolve_num, escape_arr, yield_arr)