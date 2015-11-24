from django.contrib import admin
from pdttracker.models import *

class ActionLogDescriptionAdmin(admin.ModelAdmin):
	"""Admin for ActionLogDescription"""
	list_display = ('__str__', 'short_title')
		
admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Phase)
admin.site.register(ActionLog)
admin.site.register(ActionLogDescription, ActionLogDescriptionAdmin)
admin.site.register(Defect)
admin.site.register(ProjectMember)
admin.site.register(Timer)
admin.site.register(Report)