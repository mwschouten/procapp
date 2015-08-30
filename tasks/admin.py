from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(HBTask)
admin.site.register(HBTaskRun)
admin.site.register(Waiting)
