from django.contrib import admin

# Register your models here.

from .models import HBTask,HBTaskRun

admin.site.register(HBTask)
admin.site.register(HBTaskRun)
