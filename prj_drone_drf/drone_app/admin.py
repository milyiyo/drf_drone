from django.contrib import admin

from prj_drone_drf.drone_app.models import Drone, Medication

# Register your models here.

admin.site.register(Drone)
admin.site.register(Medication)
