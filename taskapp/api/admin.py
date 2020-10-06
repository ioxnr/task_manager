from django.contrib import admin

# Register your models here.

from .models import *
from simple_history.admin import SimpleHistoryAdmin
from .models import Task

admin.site.register(Task, SimpleHistoryAdmin)