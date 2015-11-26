import django_tables2 as tables
from django.contrib.auth.models import User, Group
from pdttracker.models import *
from django_tables2.utils import A

class ManagerProjectTable(tables.Table):
    class Meta:
        model = Project
        attrs = {"class": "table"}
    def render_edit(self):
        return 'edit'
    edit = tables.LinkColumn('editProject', args=[A('pk')], orderable=False, empty_values=())
    foo = tables.TemplateColumn('Edit {{ Project.id }}' )
    project_title = tables.LinkColumn('editProject', args=[A('pk')])

class DeveloperProjectTable(tables.Table):
    class Meta:
        model = Project
        attrs = {"class": "table"}
    project_title = tables.LinkColumn('selectMode', args=[A('pk')])

class IterationTable(tables.Table):
    class Meta:
        model = Iteration
        attrs = {"class": "table"}
    iteration_name = tables.LinkColumn('editIteration', args=[A('pk')])

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
    defect_title = tables.LinkColumn('editDefect', args=[A('pk')])