from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	"""Object of each project"""
	title = models.CharField(u'Title', max_length=50)
	description = models.TextField(u'Description')
	current_iteration = models.ForeignKey('Iteration', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	in_charge_by = models.ForeignKey(User,blank=False,null=False)
	def __str__(self):
		return self.title

class Iteration(models.Model):
	"""Iteration binded to Project"""
	project_id = models.ForeignKey('Project', blank=False, null=False)
	name = models.CharField(u'name', max_length=50)
	phase_id = models.ForeignKey('Phase', blank=False, null=False)
	# when calling iteration, it is sorted by sequence followed by creation date
	sequence = models.IntegerField(default=0)
	sloc = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

class Phase(models.Model):
	"""Phase binded to Project"""
	project_id = models.ForeignKey('Project', blank=False, null=False)
	name = models.CharField(u'name', max_length=50)
	# when calling iteration, it is sorted by sequence followed by creation date
	sequence = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

class ActionLog(models.Model):
	"""Action log for each user"""
	user_id = models.ForeignKey(User, blank=False, null=False)
	action_type_id = models.ForeignKey('ActionDescription', blank=False, null=False)
	project_id = models.ForeignKey('Project', blank=True, null=True)
	defect_id = models.ForeignKey('Defect', blank=True, null=True)
	iteration_id = models.ForeignKey('Iteration', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return u"%s - %s - %s - %s" % (self.user, self.project, self.actionType, self.created_at)

class ActionDescription(models.Model):
	"""Action type for each user"""
	title = models.CharField(u'Title', max_length=50)
	def __str__(self):
		return self.title

class ProjectMember(models.Model):
	"""Members participating in the project"""
	project_id = models.ForeignKey('Project', blank=False, null=False)
	member_id = models.ForeignKey(User, blank=False, null=False)

class Defect(models.Model):
	"""Defect item"""
	def __str__(self):
		return self.name

class UserInfo(models.Model):
	"""User information"""
	user_id = models.ForeignKey(User, blank=False, null=False)
	user_type_id = models.ForeignKey('UserType', max_length=50)
	created_at = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	def __str__(self):
		return self.name

class UserType(models.Model):
	"""User type"""
	title = models.CharField(u'User Type', max_length=50)
	def __str__(self):
		return self.title
		
		