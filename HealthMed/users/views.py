from datetime import datetime
from django.db import utils
from django.db.models import Q
from django.http import HttpRequest, HttpResponseRedirect
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView, Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from . import serializers
from . import models
from .utils import gen_response
from .defs import UserNotExists, DataEntryError, UserAlreadyExists, PasswordDoNotMatch, \
    create_password_hash, get_integrity_error_field, RU_TRANSCRIPTS_FIELDS, PasswordIncorrect
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate, update_session_auth_hash, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sessions.models import Session
from .backends import PatientAuthBackend
from .models import Patient, DoctorSpecialization, Doctor, DoctorSchedule, Appointment
from email_validator import validate_email, EmailNotValidError


class UsersIndexAPIView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            user_json = user.to_dict()
            user_type = "patient" if "patient_id" in user_json else "doctor" if "doctor_id" in user_json else None
            
            return Response(template_name="users/user_cabinet.html", data=dict(
                                    authorized_status="personal-cabinet",
                                    user=user_json,
                                    user_type=user_type
                                )
                            )
        else:
            return HttpResponseRedirect("/")


class RegisterPatient(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        patient_serializer = serializers.PatientRegistrationSerializer(data=request.POST)
        
        if patient_serializer.is_valid():
            patient_serializer.validated_data["password"] = \
                create_password_hash(patient_serializer.validated_data["password"])
                
            if patient_serializer.validated_data.get("password") == \
                    create_password_hash(request.POST.get("password_repeat", "")):
                try:
                    patient_data = patient_serializer.save()
                except utils.IntegrityError as error:
                    error_field: str = get_integrity_error_field(error.args[0])
                    return gen_response(status_code=500,
                                        error_type=UserAlreadyExists().as_str(),
                                        error=[error_field, patient_serializer.validated_data.get(error_field),
                                               RU_TRANSCRIPTS_FIELDS.get(error_field, [""])[1]]
                                        )

                return gen_response(status_code=200)
            else:
                return gen_response(status_code=500, error_type=PasswordDoNotMatch().as_str(), error={
                    "password": "Passwords do not match",
                    "password_repeat": "Passwords do not match"
                })
        else:
            return gen_response(status_code=500, error_type=DataEntryError().as_str(), error=patient_serializer.errors)


class LoginPatient(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        login_serializer = serializers.PatientLoginSerializer(data=request.POST)

        if login_serializer.is_valid():
            
            patient_is_exists, patient = login_serializer.patient_is_exists()

            if patient_is_exists:
                if login_serializer.patient_check_password(patient=patient):
                    
                    authenticate(request=request, patient=patient)
                    
                    login(request=request, user=patient, backend="users.backends.PatientAuthBackend")
                    
                    return gen_response(status_code=200, details="successful log in!")
                else:
                    return gen_response(status_code=500,
                                        error={
                                            "password": "The password is wrong!"
                                        },
                                        error_type=PasswordIncorrect().as_str())
            else:
                return gen_response(status_code=500, error=f'The patient {login_serializer.validated_data.get("email")} '
                                                           f' not exists!',
                                    error_type=UserNotExists().as_str())
        else:
            return gen_response(status_code=500, error=login_serializer.errors, error_type=DataEntryError().as_str())


class LogOut(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        logout(request=request)
        return gen_response(status_code=200, details="successful log out!")


class RenderProfileWorkspace(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):

        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            workspace_name = request.GET.get("workspace", "")
            today = datetime.date(datetime.now())
            match workspace_name:
                case "appointment" | "consultation":
                    template_data = dict(
                                    specializations=[item.to_dict() for item in DoctorSpecialization.objects.all()]
                    )
                    if request.GET.get("specialization_id", False):
                        template_data.update(dict(
                            doctors=[doctor.to_dict(with_schedule=True if workspace_name == "appointment" else False, protected=True) 
                                    for doctor in Doctor.objects.filter(Q(specialization_id=request.GET.get("specialization_id", 0)))]
                    ))
                    
                    return Response(template_name=f"users/workspaces/user_{workspace_name}.html",
                                    data=template_data)
                case "user-appointments":
                    appointments: list[dict] = [
                        item.to_dict() for item in Appointment.objects.filter(Q(patient=user.patient_id)) if item.schedule.schedule_date > today
                    ]
                    consultations: list[dict] = [
                        item.to_dict() for item in models.Consultation.objects.filter(Q(patient=user.patient_id, date__gte=today)).order_by("date")
                    ]
                    appointments.sort(key=lambda x: x["schedule"]["date"])
                    return Response(template_name="users/workspaces/user_tables.html", data=dict(
                        appointments=appointments, consultations=consultations
                    ))
                case "history":
                    appointments: list[dict] = [
                        item.to_dict() for item in Appointment.objects.filter(Q(patient=user.patient_id)) if item.schedule.schedule_date < today
                    ]
                    consultations: list[dict] = [
                        item.to_dict() for item in models.Consultation.objects.filter(Q(patient=user.patient_id, date__lte=today)).order_by("date")
                    ]
                    appointments.sort(key=lambda x: x["schedule"]["date"])
                    return Response(template_name="users/workspaces/user_history.html", data=dict(
                        appointments=appointments, consultations=consultations
                    ))
                case _:
                    return gen_response(status_code=500, details="Such a workspace does not exist!")
        else:
            return gen_response(status_code=500, details="You are not logged in!")

    
class MakePatientAppointment(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            schedule_id = int(request.POST.get("schedule_id", False))
            try:
                schedule = DoctorSchedule.objects.get(schedule_id=schedule_id)
                
                if not schedule.schedule_state:
                                        
                    user.appointment_schedule(
                                            patient_id=user.patient_id,
                                            doctor_id=schedule.doctor.doctor_id, 
                                            schedule_id=schedule.schedule_id
                                            )
                    return Response({"status_type": "SUCCESS_APPOINTMENT"})
                else:
                    return Response({"status_type": "UNSUCCESS_APPOINTMENT"})
                
            except DoctorSchedule.DoesNotExist:
                return gen_response(status_code=500, error_type="SCHEDULE_NOT_FOUND")
                
        else:
            return gen_response(status_code=500, error_type="UNKNOWN_USER")
        return gen_response(status_code=500, error_type="UNKNOWN_ERROR")


class DenyPatientAppointment(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            schedule_id = int(request.POST.get("schedule_id", False))
            try:
                schedule = DoctorSchedule.objects.get(schedule_id=schedule_id)
                
                if schedule.schedule_state:
                    appointment_record: Appointment = Appointment.objects.filter(Q(schedule=schedule)).get()
                    
                    if appointment_record.patient.patient_id == user.patient_id:
                        appointment_record.delete()
                        DoctorSchedule.objects.filter(Q(schedule_id=schedule_id)).update(schedule_state=False)

                        return Response({"status_type": "SUCCESS_DISAPPOINTMENT"})
                else:
                    return Response({"status_type": "UNSUCCESS_DISAPPOINTMENT"})
                
            except DoctorSchedule.DoesNotExist:
                return gen_response(status_code=500, error_type="SCHEDULE_NOT_FOUND")
                
        else:
            return gen_response(status_code=500, error_type="UNKNOWN_USER")
        return gen_response(status_code=500, error_type="UNKNOWN_ERROR")


class EditPatientData(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            new_data = dict(
                email=request.POST.get("email", ""),
                birthdate=request.POST.get("birthdate", ""),
                passport=request.POST.get("passport", ""),
                med_policy=request.POST.get("med_policy", ""),
            )
            error_info = {}
                
            if new_data["passport"].isdigit() and len(new_data["passport"]) == 10:
                if new_data["med_policy"].isdigit() and len(new_data["med_policy"]) == 16:
                    try:
                        validate_email(new_data["email"], check_deliverability=False)
                        edited = user.custom_update(**new_data)
                        if edited:
                            return Response({}, status=200)
                        else:
                            return gen_response(status_code=500, error_type="NOTHING_CHANGE")
                    except EmailNotValidError:
                        error_info.update({"email": "incorrect"})
                else:
                    error_info.update({"med_policy": "incorrect"})
            else:
                error_info.update({"passport": "incorrect"})
            
            if error_info:
                return gen_response(status_code=500, error_type="INCORRECT_INFO", error=error_info)
            return Response({}, status=200)
        
        return Response({}, status=500)


class MakePatientConsultationRequest(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            doctor_id = int(request.POST.get("doctor_id", False))
            date = request.POST.get("date", False)
            data = dict(
                doctor=doctor_id,
                patient=user.patient_id,
                date=date
            )
            
            if doctor_id and date:
                consultation = serializers.ConsultationSerializer(data=data)
                
                if consultation.is_valid():
                    if consultation.save():
                        return Response({"status_type": "SUCCESS_ADD_REQUEST"})
                    else:
                        return gen_response(status_code=500, error_type="CONSULT_REQUEST_ALREADY_EXISTS") 
                else:
                    return gen_response(status_code=500, error_type="INCORRECT_DATA", error=consultation.errors)
            else:
                return gen_response(status_code=500, error_type="NOT_ENOUGH_DATA")
        else:
            return gen_response(status_code=500, error_type="UNKNOWN_USER")



class DeletePatientConsultationRequest(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "patient_id"):
            user: Patient = request.user
            consultation_id = int(request.POST.get("consultation_id", False))
            
            if consultation_id:
                consultation = models.Consultation.objects.filter(Q(consultation_id=consultation_id, patient=user.get_self_record()))
                
                if consultation.exists():
                    consultation.delete()
                    
                    return Response({"status_type": "SUCCESS_DELETE"})
                else:
                    return gen_response(status_code=500, error_type="INCORRECT_DATA")
            else:
                return gen_response(status_code=500, error_type="NOT_ENOUGH_DATA")
        else:
            return gen_response(status_code=500, error_type="UNKNOWN_USER")
            
