from django.db.models import Count, F, Q
from pdttracker.models import *
from pdttracker.ReportPolicy import *

def add_iteration_report(iteration):
	"""Add iteration report when an iteration is created"""
	title = iteration.iteration_name + get_report_suffix()
	i = Iteration.objects.get(pk=iteration.pk)
	current_phase = Phase.objects.filter(iteration = i)[:1].get()
	dsloc = 0
	if i.iteration_sequence == 1:
		# if the iteration is the first one, get the previous phase
		if current_phase.phase_sequence == 1:
			# if the phase is the first one, assign iteration to zero
			dsloc = 0
		else:
			# get the dsloc of the current phase
			current_phase_report = Report.objects.filter(phase = current_phase)[:1].get()
			dsloc = current_phase_report.delivered_sloc
	else:
		# get the dsloc of the previous iteration
		prev_i = get_previous_iteration(iteration)
		if prev_i is not None:
			dsloc = prev_i.iteration_sloc
	t = str(title)
	r = Report.objects.create(report_title=t, delivered_sloc=dsloc)
	Iteration.objects.filter(pk=iteration.pk).update(iteration_report=r)
	obj = Report.objects.get(pk=r.pk)
	return obj

def add_phase_report(phase):
	"""Add phase report when a phase is created"""
	title = phase.phase_name + get_report_suffix()
	p = Phase.objects.get(pk=phase.pk)
	dsloc = 0
	if p.phase_sequence == 1:
		dsloc = 0
	else:
		# get the dsloc of the previous phase
		prev_p = get_previous_phase(phase)
		if prev_p is not None:
			dsloc = prev_p.dsloc
	t = str(title)
	r = Report(report_title=t, delivered_sloc=dsloc)
	r.save()
	Phase.objects.filter(pk=phase.pk).update(phase_report=r)
	obj = Report.objects.get(pk=r.pk)
	return obj

def add_project_report(project):
	"""Add project report when a project is created"""
	title = project.project_title + get_report_suffix()
	r = Report(report_title=title, delivered_sloc=0)
	r.save()
	obj = Report.objects.get(pk=r.pk)
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

def add_defect_update(iteration):
	Report.objects.filter(iteration = iteration).update(defects_injected=F('defects_injected')+1)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(defects_injected=F('defects_injected')+1)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(defects_injected=F('defects_injected')+1)
	
def remove_defect_update(iteration):
	Report.objects.filter(iteration = iteration).update(defects_removed=F('defects_removed')+1)
	ph = Phase.objects.filter(iteration = iteration)[:1].get()
	Report.objects.filter(phase = ph).update(defects_removed=F('defects_removed')+1)
	pj = Project.objects.filter(phase = ph)[:1].get()
	Report.objects.filter(project = pj).update(defects_removed=F('defects_removed')+1)

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
	# get table values
	ds = Defect.objects.filter(recorded_in=project).values('iteration_injected__iteration_name', 'iteration_resolved__iteration_name').order_by('iteration_injected__in_phase__phase_sequence', 'iteration_injected__iteration_sequence', 'iteration_resolved__in_phase__phase_sequence', 'iteration_resolved__iteration_sequence').annotate(num=Count('pk'))
	# get resolved row sum
	rs = Defect.objects.filter(recorded_in=project).values('iteration_resolved__iteration_name').order_by('iteration_resolved__in_phase__phase_sequence', 'iteration_resolved__iteration_sequence').annotate(num=Count('pk'))
	# get injected column sum
	cs = Defect.objects.filter(recorded_in=project).values('iteration_injected__iteration_name').order_by('iteration_injected__in_phase__phase_sequence', 'iteration_injected__iteration_sequence').annotate(num=Count('pk'))
	ph = Phase.objects.filter(in_project=project).all()
	iterations = Iteration.objects.filter(in_phase=ph).values('iteration_name').order_by('in_phase__phase_sequence', 'iteration_sequence')
	inject_num = {}
	resolve_num = {}
	resolve_last_num = {}
	inject_iteration = []
	resolve_iteration = []
	# initialize values
	for i in iterations:
		inject_num[str(i['iteration_name'])] = 0
		resolve_num[str(i['iteration_name'])] = 0
	for c in cs:
		# populate total inject numbers on the bottom of the table
		inject_num[str(c['iteration_injected__iteration_name'])] = int(c['num'])
		inject_iteration += [str(c['iteration_injected__iteration_name'])]
	for r in rs:
		# populate total resolve numbers on the right of the table
		resolve_num[str(r['iteration_resolved__iteration_name'])] = int(r['num'])
		resolve_iteration += [str(r['iteration_resolved__iteration_name'])]
	for d in ds:
		# populate the last row of defect resolved, for escape calculation
		resolve_last_num[str(d['iteration_injected__iteration_name'])] = int(d['num'])
	# populate escape number and prepare for yield calculation
	m = 0
	n = 0
	cumulative_escape = 0
	cumulative_inject_num = {}
	cumulative_resolve_num = {}
	escape_arr = []
	for i in range(len(inject_iteration)):
		m += inject_num[inject_iteration[i]]
		cumulative_inject_num[inject_iteration[i]] = m
		if inject_iteration[i] in resolve_last_num:
			escape_arr.append(round(resolve_last_num[inject_iteration[i]] * (1 - 0.8)))
		else:
			escape_arr.append(0)
		cumulative_escape += escape_arr[i]
		cumulative_inject_num[inject_iteration[i]] += escape_arr[i]
	for i in range(len(resolve_iteration)):
		n += resolve_num[resolve_iteration[i]]
		cumulative_resolve_num[resolve_iteration[i]] = n
	# populate yield
	yield_arr = []
	for i in range(len(inject_iteration)):
		if i == 0:
			yield_arr.append(format(resolve_num[resolve_iteration[i]] / cumulative_inject_num[inject_iteration[i]] * 100,'.2f'))
		else:
			yield_arr.append(format(resolve_num[resolve_iteration[i]] / (cumulative_inject_num[inject_iteration[i]] - cumulative_resolve_num[resolve_iteration[i-1]]) * 100, '.2f'))
	table_output = [[''] + inject_iteration + ['Total']]
	# populate table-convenient output
	for i in range(len(resolve_iteration)):
		out = [resolve_iteration[i]]
		for j in range(len(inject_iteration)):
			check = False
			for d in ds:
				if d['iteration_injected__iteration_name'] == inject_iteration[j] and d['iteration_resolved__iteration_name'] == resolve_iteration[i]:
					check = True
					out.append(str(d['num']))
			if check == False:
				out.append('')
		out.append(str(resolve_num[resolve_iteration[i]]))
		table_output.append(out)
	out2 = ['Escapes'] + [str(x) for x in escape_arr] + [str(cumulative_escape)]
	table_output.append(out2)
	num_list = [v for v in inject_num.values()]
	sum_list = str(sum(num_list))
	out3 = ['Total'] + [str(v) for v in cumulative_inject_num.values()] + [sum_list]
	table_output.append(out3)

	# return (ds, inject_iteration, resolve_iteration, inject_num, resolve_num, escape_arr, yield_arr)
	return (table_output, yield_arr)


def get_previous_phase(curr_phase):
    prev_seq = curr_phase.phase_sequence - 1
    if prev_seq == 0:
        return None
    else:
        if Phase.objects.filter(Q(project=curr_phase.in_project) & Q(phase_sequence=prev_seq)).count() > 0:
        	prev = Phase.objects.filter(project=curr_phase.in_project).get(phase_sequence=prev_seq)
        else:
        	return None
   
    return prev


def get_previous_iteration(curr_iteration):
    prev_seq = curr_iteration.iteration_sequence - 1
    if prev_seq == 0:
        return None
    else:
        if Phase.objects.filter(Q(project=curr_iteration.in_phase.in_project) & Q(phase_sequence=prev_seq)).count() > 0:
            prev = Iteration.objects.filter(in_phase=curr_iteration.in_phase).get(iteration_sequence=prev_seq)
        else:
            return None
   
    return prev