from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from users.models import Patient, Doctor
from users.defs import check_password


class DoctorAuthBackend(BaseBackend):
    
    def authenticate(self, request, doctor: Doctor | None = None):

        if doctor is not None:
            return Doctor.objects.get(email=doctor.email)
        else:
            return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None