from django.contrib import admin
from prj_drone_drf.drone_app.models.drone import Drone
from prj_drone_drf.drone_app.models.load_information import LoadInformation
from prj_drone_drf.drone_app.models.medication import Medication

# Register your models here.

admin.site.register(Drone)
admin.site.register(Medication)
admin.site.register(LoadInformation)
