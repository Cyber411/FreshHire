from django.contrib import admin
from .models import User, SeekerProfile, EmployerProfile, Job, Application

from django.contrib import admin
from .models import SeekerProfile, EmployerProfile, Job, Application

admin.site.register(SeekerProfile)
admin.site.register(EmployerProfile)
admin.site.register(Job)
admin.site.register(Application)