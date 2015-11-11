from django.contrib import admin
from pdttracker.models import Project, Iteration, Phase, ActionLog, ActionDescription, ProjectMember, User, UserType, Defect

admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Phase)
admin.site.register(ActionLog)
admin.site.register(ActionDescription)
admin.site.register(ProjectMember)
admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Defect)