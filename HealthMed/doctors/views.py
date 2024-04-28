from datetime import datetime
from django.db import utils
from django.db.models import Q
from django.http import HttpRequest
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView, Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from . import serializers
from users import models
from doctors.models import Article
from users.utils import gen_response
from users.defs import DataEntryError, UserAlreadyExists, PasswordDoNotMatch, \
    create_password_hash, get_integrity_error_field, RU_TRANSCRIPTS_FIELDS
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from users.defs import NotValidData, TimeOverlapping, ScheduleNotExists, AlreadyExists


class DoctorIndexAPIView(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            user_json = user.to_dict()
            user_type = "patient" if "patient_id" in user_json else "doctor" if "doctor_id" in user_json else None
            
            return Response(template_name="doctors/doctor_cabinet.html", data=dict(
                                    authorized_status="personal-cabinet",
                                    user=user_json,
                                    user_type=user_type,
                                    doctor_id=user.doctor_id
                                )
                            )
        else:
            return redirect("doctor-login")


class DoctorLoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'doctors/login.html'
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            return redirect("doctor-profile")

        return Response({"serializer": serializers.DoctorLoginSerializer(), "style": self.style})

    def post(self, request: HttpRequest, *args, **kwargs):
        login_serializer = serializers.DoctorLoginSerializer(data=request.POST)

        if not login_serializer.is_valid():
            return Response({'serializer': login_serializer})
                    
        doctor_is_exists, doctor = login_serializer.doctor_is_exists()

        if doctor_is_exists:
            if login_serializer.doctor_check_password(doctor=doctor):

                authenticate(request=request, doctor=doctor)
                
                login(request=request, user=doctor, backend="doctors.backends.DoctorAuthBackend")
                
                # return gen_response(status_code=200, details="successful log in!")
                return redirect("doctor-profile")
            else:
                return Response({'serializer': login_serializer})
        else:
            return Response({'serializer': login_serializer})


class RegisterDoctor(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        doctor_serializer = serializers.DoctorRegistrationSerializer(data=request.POST)
        
        if doctor_serializer.is_valid():
            doctor_serializer.validated_data["password"] = \
                create_password_hash(doctor_serializer.validated_data["password"])
                
            if doctor_serializer.validated_data.get("password") == \
                    create_password_hash(request.POST.get("password_repeat", "")):
                try:
                    doctor_data = doctor_serializer.save()
                except utils.IntegrityError as error:
                    error_field: str = get_integrity_error_field(error.args[0])
                    return gen_response(status_code=500,
                                        error_type=UserAlreadyExists().as_str(),
                                        error=[error_field, doctor_serializer.validated_data.get(error_field),
                                               RU_TRANSCRIPTS_FIELDS.get(error_field, [""])[1]]
                                        )

                return gen_response(status_code=200)
            else:
                return gen_response(status_code=500, error_type=PasswordDoNotMatch.as_str(), error={
                    "password": "Passwords do not match",
                    "password_repeat": "Passwords do not match"
                })
        else:
            return gen_response(status_code=500, error_type=DataEntryError.as_str(), error=doctor_serializer.errors)


class GetDoctorsBySpecializationId(CreateAPIView):

    def get(self, request: HttpRequest, *args, **kwargs):
        specialization_id = request.GET.get("specialization_id", -1)
        doctors = [doctor.to_dict() for doctor in models.Doctor.objects.filter(Q(specialization_id=specialization_id))]
        return Response({"doctors": doctors}, status=200)


class DeleteDoctorScheduleRecord(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            schedule_id = request.POST.get("schedule_id", False)
            
            schedule = models.DoctorSchedule.objects.filter(Q(doctor_id=user.doctor_id, schedule_id=schedule_id))
            
            if schedule_id and schedule.exists():
                schedule.delete()
                
                return Response({"status_type": "SUCCESS_DEL_RECORD"})
            else:
                return gen_response(status_code=500, error_type=ScheduleNotExists.as_str())
        else:
            return Response(status=403)


class AcceptConsultation(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            consultation_id = request.POST.get("consultation_id", False)
            
            consultation = models.Consultation.objects.filter(Q(doctor=user.get_self_record(), consultation_id=consultation_id))
            
            if consultation_id and consultation.exists():
                consultation.update(status=True)
                
                return Response({"status_type": "SUCCESS_ACCEPT"})
            else:
                return gen_response(status_code=500, error_type=ScheduleNotExists.as_str())
        else:
            return Response(status=403)


class DenyConsultation(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            consultation_id = request.POST.get("consultation_id", False)
            
            consultation = models.Consultation.objects.filter(Q(doctor=user.get_self_record(), consultation_id=consultation_id))
            
            if consultation_id and consultation.exists():
                consultation.update(status=False)
                
                return Response({"status_type": "SUCCESS_DENY"})
            else:
                return gen_response(status_code=500, error_type=ScheduleNotExists.as_str())
        else:
            return Response(status=403)


class AddDoctorScheduleRecord(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            data = dict(
                doctor = user.doctor_id,
                schedule_date = request.POST.get("date", "").split("."),
                schedule_start_time = request.POST.get("start_time"),
                schedule_end_time = request.POST.get("end_time"),
                schedule_state = False
            )
            data["schedule_date"] = f'{data["schedule_date"][2]}-{data["schedule_date"][1]}-{data["schedule_date"][0]}'
            
            serializer = serializers.DoctorScheduleSerializer(data=data)
            
            if serializer.is_valid():
                valid_data = serializer.validated_data
                overlapping_slots = models.DoctorSchedule.objects.filter(Q(doctor=data.get("doctor")) and 
                    (Q(schedule_start_time__lt=valid_data.get("schedule_start_time"), schedule_end_time__gt=valid_data.get("schedule_end_time")) | 
                    Q(schedule_start_time__lt=valid_data.get("schedule_end_time"), schedule_end_time__gt=valid_data.get("schedule_start_time")))
                )
                
                if not overlapping_slots.exists():
                    serializer.save()
                    
                    return Response({"status_type": "SUCCESS_ADD_RECORD"})
                else:
                    return gen_response(status_code=500, error_type=TimeOverlapping.as_str())
            else:
                return gen_response(status_code=500, error_type=NotValidData.as_str(), error=serializer.errors)
        else:
            return Response(status=403)


class GetDoctorSchedule(CreateAPIView):

    def get(self, request: HttpRequest, *args, **kwargs):
        try:
            doctor_id = int(request.GET.get("doctor_id", False))
            special_id = int(request.GET.get("special_id", False))
        except ValueError:
            return gen_response(status_code=500, error="Args parsing error")
        result = {}
        if doctor_id:
            try:
                doctor = models.Doctor.objects.get(doctor_id=doctor_id)
                result = doctor.get_schedule()
            except models.Doctor.DoesNotExist:
                return gen_response(status_code=500, error="Doctor does not exists")
        if special_id:
            result: dict[int, dict[str, list[dict]]] = {}
            for doctor in models.Doctor.objects.filter(Q(specialization_id=special_id)):
                result[doctor.doctor_id] = result.get(doctor.doctor_id, {})
                result[doctor.doctor_id].update(doctor.get_schedule())
        
        return Response(result, status=200)
    
    
class RenderProfileWorkspace(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):

        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            today = datetime.date(datetime.now())
            match request.GET.get("workspace", ""):
                case "doctor-appointments":
                    doctor_appointments: list[dict] = [
                        item.to_dict() for item in models.Appointment.objects.filter(Q(doctor=user.doctor_id)) if item.schedule.schedule_date > today
                    ]
                    consultations: list[dict] = [
                        item.to_dict() for item in models.Consultation.objects.filter(Q(doctor=user.doctor_id, date__gte=today)).order_by("date") if item.status == True
                    ]
                    doctor_appointments.sort(key=lambda x: x["schedule"]["date"])
                    
                    return Response(template_name="doctors/workspaces/doctor_appointments.html", data=dict(
                        appointments=doctor_appointments, consultations=consultations
                    ))
                case "doctor-schedule":
                    return Response(template_name="doctors/workspaces/doctor_schedule.html", data=dict())
                case "doctor-consultation":
                    consultations: list[dict] = [
                        item.to_dict() for item in models.Consultation.objects.filter(Q(doctor=user.doctor_id, date__gte=today)).order_by("date") if item.status != True
                    ]
                    return Response(template_name="doctors/workspaces/doctor_consultation.html", data=dict(consultations=consultations))
                case "doctor-article":
                    articles = [item.to_dict() for item in Article.objects.all()]
                    
                    return Response(template_name="doctors/workspaces/doctor_article.html", data=dict(
                        articles=articles
                    ))
                case _:
                    return gen_response(status_code=500, details="Such a workspace does not exist!")
        else:
            return gen_response(status_code=500, details="You are not logged in!")


class CreateArticle(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            data = dict(
                publisher = user.doctor_id,
                title = request.POST.get("title", False),
                # image = request.POST.get("image", ""),
                text = request.POST.get("text", False),
                publish_date = datetime.now().strftime("%Y-%m-%d")
            )
            
            article = serializers.ArticleSerializer(data=data)
            
            if article.is_valid():
                if article.is_not_exists():
                
                    article.save()
                    
                    return Response({"status_type": "SUCCESS_CREATE"}, status=200)
                
                else:
                    return gen_response(status_code=500, error_type=AlreadyExists.as_str())
            else:
                return gen_response(status_code=500, error=article.errors, error_type=NotValidData.as_str())
            
        else:
            return Response(status=403)
        

class DeleteArticle(CreateAPIView):

    def post(self, request: HttpRequest, *args, **kwargs):
        
        if request.user.is_authenticated and hasattr(request.user, "doctor_id"):
            user: models.Doctor = request.user
            article_id = request.POST.get("article_id", "")
            if not article_id.isdigit():
                return gen_response(status_code=500)

            article = Article.objects.filter(article_id=int(article_id))
            
            if article.exists():
                article.delete()
                
                return Response({"status_type": "SUCCESS_DELETE"}, status=200)
            else:
                return gen_response(status_code=500)
            
        else:
            return Response(status=403)