from collections import OrderedDict
from django.db.models import Q
from rest_framework.fields import empty
from rest_framework.serializers import Serializer
from rest_framework.serializers import IntegerField, EmailField, CharField, \
    DateField, DateTimeField, TimeField, BooleanField
from . import models
from .defs import create_password_hash
from .validators import validate_phone, validate_passport, validate_med_policy
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenObtainPairView


class PatientRegistrationSerializer(Serializer):
    email = EmailField()
    phone = CharField(max_length=16)
    password = CharField(max_length=128)

    firstname = CharField(max_length=32)
    lastname = CharField(max_length=32)
    surname = CharField(max_length=32, required=False)

    birthdate = DateField()
    passport = CharField(min_length=10, max_length=10)
    med_policy = CharField(min_length=16, max_length=16)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.validated_data: OrderedDict

    def create(self, validated_data):
        return models.Patient.objects.create(**validated_data)

    def validate_phone(self, phone) -> str: return validate_phone(self=self, phone=phone)
    def validate_passport(self, passport) -> str: return validate_passport(self, passport)
    def validate_med_policy(self, med_policy) -> str: return validate_med_policy(self, med_policy)


class PatientLoginSerializer(Serializer):
    email = EmailField()
    password = CharField(max_length=128)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.validated_data: OrderedDict

    def patient_is_exists(self) -> tuple[bool, models.Patient | None]:
        users = models.Patient.objects.filter(Q(email=self.validated_data.get("email")))
        try:
            user = users.get()
            if user:
                return True, user
            return False, None
        except models.Patient.DoesNotExist:
            return False, None

    def patient_check_password(self, patient: models.Patient):
        self.validated_data["password"] = create_password_hash(self.validated_data.get("password"))
        # user: models.Patient = models.Patient.objects.filter(Q(email=self.validated_data.get("email"))).get()
        if patient.password == self.validated_data["password"]:
            return True
        else: return False


class AppointmentSerializer(Serializer):
    patient = IntegerField()
    doctor = IntegerField()
    schedule = IntegerField()

    def create(self, validated_data):
        return models.Appointment.objects.create(**validated_data)


class DoctorSpecializationSerializer(Serializer):
    specialization_name = CharField(max_length=128)

    def create(self, validated_data):
        return models.DoctorSpecialization.objects.create(**validated_data)


class ConsultationSerializer(Serializer):
    patient = IntegerField()
    doctor = IntegerField()
    date = DateField()

    def create(self, validated_data):
        validated_data["patient"] = models.Patient.objects.get(Q(patient_id=validated_data["patient"]))
        validated_data["doctor"] = models.Doctor.objects.get(Q(doctor_id=validated_data["doctor"]))
                
        if self.not_exists(doctor=validated_data["doctor"], patient=validated_data["patient"], date=validated_data["date"]):
            return models.Consultation.objects.create(**validated_data)
        else:
            return False
    
    def not_exists(self, patient, doctor, date):
        return True if not models.Consultation.objects.filter(Q(patient=patient, doctor=doctor, date=date)).exists() else False
    