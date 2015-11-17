import django_tables2 as tables
from django.contrib.auth.models import User, Group
from pdttracker.models import *

class ProjectTable(tables.Table):
    class Meta:
        model = Project
        attrs = {"class": "table"}

class IterationTable(tables.Table):
    class Meta:
        model = Iteration
        attrs = {"class": "table"}

class PhaseTable(tables.Table):
    class Meta:
        model = Phase
        attrs = {"class": "table"}

class ActionLogTable(tables.Table):
    class Meta:
        model = ActionLog
        attrs = {"class": "table"}

class UserTable(tables.Table):
	selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
	class Meta:
		model = User
		fields = ("selection", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "last_login")
		attrs = {"class": "table"}

class UserInfoTable(tables.Table):
    class Meta:
        model = Group
        attrs = {"class": "table"}

class UserTypeTable(tables.Table):
	class Meta:
		model = Defect
		attrs = {"class": "table"}

class DefectTable(tables.Table):
    class Meta:
        model = Defect
        attrs = {"class": "table"}
