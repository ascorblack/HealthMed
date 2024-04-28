from collections import OrderedDict
from django.db.models import Q
from rest_framework.fields import empty
from rest_framework.serializers import Serializer
from rest_framework.serializers import IntegerField, EmailField, CharField, \
    DateField, DateTimeField, TimeField, BooleanField
from users import models
from doctors.models import Article
from users.defs import create_password_hash
from users.validators import validate_phone, validate_passport, validate_med_policy
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenObtainPairView


class DoctorRegistrationSerializer(Serializer):
    email = EmailField()
    phone = CharField(max_length=16)
    password = CharField(max_length=128)

    firstname = CharField(max_length=32)
    lastname = CharField(max_length=32)
    surname = CharField(max_length=32, required=False)
    
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.validated_data: OrderedDict

    def create(self, validated_data):
        return models.Doctor.objects.create(**validated_data)

    def validate_phone(self, phone) -> str: return validate_phone(self=self, phone=phone)


class DoctorSerializer(Serializer):
    email = CharField(max_length=64)
    password = CharField(max_length=128)

    firstname = CharField(max_length=32)
    lastname = CharField(max_length=32)
    surname = CharField(max_length=32)

    def create(self, validated_data):
        return models.Doctor.objects.create(**validated_data)


class DoctorLoginSerializer(Serializer):
    email = EmailField(style={'input_type': 'email', 'placeholder': 'Email'})
    password = CharField(max_length=128, style={'input_type': 'password', 'placeholder': 'Пароль'})
    
    def doctor_is_exists(self) -> tuple[bool, models.Doctor | None]:
        doctors = models.Doctor.objects.filter(Q(email=self.validated_data.get("email")))
        try:
            doctor = doctors.get()
            if doctor:
                return True, doctor
            return False, None
        except models.Doctor.DoesNotExist:
            return False, None

    def doctor_check_password(self, doctor: models.Doctor):
        # self.validated_data["password"] = create_password_hash(self.validated_data.get("password"))
        if doctor.password == self.validated_data["password"]:
            return True
        else: return False


class DoctorScheduleSerializer(Serializer):
    doctor = IntegerField()
    schedule_date = DateField()
    schedule_start_time = TimeField()
    schedule_end_time = TimeField()
    schedule_state = BooleanField()

    def create(self, validated_data):
        validated_data["doctor"] = models.Doctor.objects.get(doctor_id=validated_data["doctor"])
        return models.DoctorSchedule.objects.create(**validated_data)


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

    def create(self, validated_data):
        return models.Consultation.objects.create(**validated_data)



class ArticleSerializer(Serializer):
    title = CharField(max_length=255)
    text = CharField()
    publisher = IntegerField()
    publish_date = DateField()

    def create(self, validated_data):
        validated_data["publisher"] = models.Doctor.objects.get(doctor_id=validated_data["publisher"])
        
        return Article.objects.create(**validated_data)
    
    def is_not_exists(self):
        return True if not Article.objects.filter(Q(title=self.validated_data.get("title"))).exists() else False
