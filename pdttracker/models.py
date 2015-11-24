from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	"""Object of each project"""
	project_title = models.CharField(u'Project title', max_length=50)
	project_description = models.TextField(u'Description')
	project_sloc = models.IntegerField(default=0)
	num_phase = models.IntegerField(default=0)
	num_iteration = models.IntegerField(default=0)
	current_phase = models.ForeignKey('Phase', blank=True, null=True)
	current_iteration = models.ForeignKey('Iteration', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	in_charge_by = models.ForeignKey(User,blank=False,null=False,related_name='in_charge_of')
	# report must be created before project can be created
	project_report = models.ForeignKey('Report', blank=True, null=True)
	is_active = models.BooleanField(default=True)
	yield_percentage = models.FloatField(default=0.8)
	def __str__(self):
		return self.project_title

class Iteration(models.Model):
	"""Iteration binded to Project"""
	iteration_name = models.CharField(u'Iteration name', max_length=50)
	iteration_sequence = models.IntegerField(default=0)
	iteration_sloc = models.IntegerField(default=0)
	in_phase = models.ForeignKey('Phase', blank=False, null=False)
	# report must be created before iteration can be created
	iteration_report = models.ForeignKey('Report', blank=False, null=False)
	def __str__(self):
		return self.iteration_name

class Phase(models.Model):
	"""Phase binded to Project"""
	phase_name = models.CharField(u'Phase name', max_length=50)
	phase_sequence = models.IntegerField(default=0)
	phase_sloc = models.IntegerField(default=0)
	in_project = models.ForeignKey('Project', blank=False, null=False)
	# report must be created before phase can be created
	phase_report = models.ForeignKey('Report', blank=False, null=False)
	def __str__(self):
		return self.phase_name

class ActionLog(models.Model):
	"""Action log for each user"""
	action_log_created_by = models.ForeignKey('ProjectMember', blank=True, null=True)
	action_log_description = models.ForeignKey('ActionLogDescription', blank=True, null=True)
	project_tracked = models.ForeignKey('Project', blank=True, null=True)
	defect_tracked = models.ForeignKey('Defect', blank=True, null=True)
	iteration_tracked = models.ForeignKey('Iteration', blank=True, null=True)
	phase_tracked = models.ForeignKey('Phase', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return u"%s %s - %s - %s - %s" % (self.action_log_created_by.first_name, self.action_log_created_by.last_name, self.project_tracked, self.action_log_description, str(self.created_at))

class ActionLogDescription(models.Model):
	"""Action type for each user"""
	title = models.CharField(u'Action log description title', max_length=50)
	short_title = models.CharField(u'Action log short name', max_length=10)
	def __str__(self):
		return self.title

class Defect(models.Model):
	"""Defect item"""
	defect_title = models.CharField(u'Defect title', max_length=50)
	defect_type = models.CharField(u'Defect type', max_length=50)
	defect_description = models.TextField(u'Defect description')
	defect_remarks = models.TextField(u'Defect remarks')
	recorded_in = models.ForeignKey('Project', blank=True, null=True)
	iteration_injected = models.ForeignKey('Iteration', blank=True, null=True, related_name='iteration_injected')
	iteration_resolved = models.ForeignKey('Iteration', blank=True, null=True, related_name='iteration_resolved')
	def __str__(self):
		return self.defect_title

class ProjectMember(models.Model):
	"""Project member binding"""
	work_in = models.ForeignKey('Project', blank=True, null=True)
	member = models.ForeignKey(User, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return "%s - %s" % (self.work_in.project_title, self.member)

class Timer(models.Model):
	"""Timer log"""
	created_for = models.ForeignKey('Project', blank=True, null=True)
	num_hrs = models.FloatField(default=0)
	mode = models.CharField(blank=False, null=False, default="devmode", max_length=10)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return "%s %s in %s" % (self.timer_created_by.member.first_name, self.timer_created_by.member.last_name, self.timer_created_by.work_in.project_title)

class Report(models.Model):
	"""Report generation"""
	report_title = models.CharField(u'Report title', max_length=50)
	defects_injected = models.IntegerField(default=0)					# input
	defects_removed = models.IntegerField(default=0)					# input
	delivered_sloc = models.IntegerField(default=0)						# input
	delivered_sloc_of_project = models.FloatField(default=0)			# percentage
	person_mths = models.IntegerField(default=0)
	person_mths_of_project = models.FloatField(default=0)				# percentage
	delivered_sloc_per_person_mths = models.FloatField(default=0)
	injection_rate_per_person_hrs = models.FloatField(default=0)
	removal_rate_per_person_hrs = models.FloatField(default=0)
	person_hrs_devmode = models.FloatField(default=0)					# input
	person_hrs_defectmode = models.FloatField(default=0)				# input
	person_hrs_mgmtmode = models.FloatField(default=0)					# input
	defect_density_per_ksloc = models.FloatField(default=0)
	yield_value = models.FloatField(default=0)							# percentage
	def __str__(self):
		return self.report_title
		
# class UserInfo(models.Model):
# 	"""User information"""
# 	user_id = models.OneToOneField(User, blank=False, null=False, primary_key=True)
# 	user_type_id = models.ForeignKey('UserType', max_length=50)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	is_active = models.BooleanField(default=True)
# 	def __str__(self):
# 		return "%s %s" % (self.user_id.first_name, self.user_id.last_name)

# class UserType(models.Model):
# 	"""User type"""
# 	title = models.CharField(u'User Type', max_length=50)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	def __str__(self):
# 		return self.title
		
		