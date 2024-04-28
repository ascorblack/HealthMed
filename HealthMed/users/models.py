from django.db import models
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
from doctors.models import DoctorSchedule, DoctorSpecialization, Doctor


class Patient(AbstractBaseUser):
    patient_id = models.AutoField(primary_key=True)

    email = models.EmailField(null=False, unique=True)
    phone = PhoneNumberField(null=False, unique=True)
    password = models.CharField(max_length=256, null=False)

    firstname = models.CharField(max_length=32, null=False)
    lastname = models.CharField(max_length=32, null=False)
    surname = models.CharField(max_length=32, null=True, default=None)

    birthdate = models.DateField()
    passport = models.CharField(max_length=10, null=False, unique=True)
    med_policy = models.CharField(max_length=16, null=False, unique=True)

    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = [
        "email",
        "phone",
        "password",
        "firstname",
        "lastname",
        "birthdate",
        "passport",
        "med_policy"
    ]

    class Meta:
        db_table = "users_patient"
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

    def __str__(self):
        return f"{self.lastname} {self.firstname} {self.surname}"

    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'phone': self.get_phone(),
            'password': self.password,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'surname': self.surname,
            'birthdate': self.birthdate.strftime("%Y-%m-%d"),
            'med_policy': self.med_policy,
            'passport': self.passport,
            'patient_id': self.patient_id,
            'is_active': self.is_active,
            'last_login': self.last_login,
        }

    def get_username(self):
        return self.email
    
    def get_phone(self):
        return f"{self.phone.country_code}{self.phone.national_number}"
    
    def get_self_record(self):
        return Patient.objects.filter(Q(patient_id=self.patient_id)).get()
    
    @classmethod
    def appointment_schedule(cls, patient_id: int, doctor_id: int, schedule_id: int):
        DoctorSchedule.objects.filter(schedule_id=schedule_id).update(schedule_state=True)
        return Appointment(
            patient=Patient.objects.get(patient_id=patient_id), 
            doctor=Doctor.objects.get(doctor_id=doctor_id),
            schedule=DoctorSchedule.objects.get(schedule_id=schedule_id)
        ).save()
        
    def custom_update(self, *args, **kwargs):
        edited = False
        for key, value in kwargs.items():
            self_value = getattr(self, key)
            if key == "phone": self_value = self.get_phone()
            if key == "birthdate":
                self_value = self.birthdate.strftime("%Y-%m-%d")
            if self_value != value:
                Patient.objects.filter(Q(patient_id=self.patient_id)).update(**{key: value})
                edited = True
        return edited


class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField(null=True, default=None)

    class Meta:
        db_table = "users_consultations"
        verbose_name = "Консультация"
        verbose_name_plural = "Консультации"
        
    def __str__(self):
        return f"{self.patient} -> {self.doctor}  ({self.date}) ({ 'Принято' if self.status else 'Отказано' if self.status is not None else 'Ожидает подтверждения' })"


    def to_dict(self):
        return dict(
            patient=dict(
                id=self.patient.patient_id,
                fullname=self.patient,
                ),
            doctor=dict(
                    fullname=self.doctor,
                    id=self.doctor.doctor_id,
                    sepcialization=dict(
                        id=self.doctor.specialization.specialization_id,
                        name=self.doctor.specialization.specialization_name,
                    )
                ),
            consultation=dict(
                date=self.date,
                status=self.status,
                id=self.consultation_id
            )
        )



class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE)

    class Meta:
        db_table = "users_appointments"
        verbose_name = "Запись к врачу"
        verbose_name_plural = "Записи к врачу"
        
    def __str__(self):
        return f"{self.patient} -> {self.doctor}"
        
    def to_dict(self):
        return dict(
            appointment_id=self.appointment_id,
            patient=dict(
                id=self.patient.patient_id,
                fullname=self.patient,
                ),
            doctor=dict(
                    fullname=self.doctor,
                    id=self.doctor.doctor_id,
                    sepcialization=dict(
                        id=self.doctor.specialization.specialization_id,
                        name=self.doctor.specialization.specialization_name,
                    )
                ),
            schedule=self.schedule.to_dict()
        )
