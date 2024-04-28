from django.contrib import admin
from .models import Doctor, DoctorSpecialization, DoctorSchedule, Article


for model in [Doctor, DoctorSpecialization, DoctorSchedule, Article]:
    admin.site.register(model)
