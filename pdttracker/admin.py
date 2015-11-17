from django.contrib import admin
from pdttracker.models import *

admin.site.register(Project)
admin.site.register(Iteration)
admin.site.register(Phase)
admin.site.register(ActionLog)
admin.site.register(ActionDescription)
admin.site.register(UserInfo)
admin.site.register(UserType)
admin.site.register(Defect)