from django.contrib import admin
from .models import Patient, Consultation, Appointment


for model in [Patient, Consultation, Appointment]:
    admin.site.register(model)
