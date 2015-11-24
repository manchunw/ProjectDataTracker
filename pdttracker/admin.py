from django.contrib import admin
from pdttracker.models import *

admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Phase)
admin.site.register(ActionLog)
admin.site.register(ActionLogDescription)
admin.site.register(Defect)
admin.site.register(ProjectMember)
admin.site.register(Timer)
admin.site.register(Report)