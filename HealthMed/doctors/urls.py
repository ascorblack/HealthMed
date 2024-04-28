from . import views
from django.urls import path, include

urlpatterns = [
    path('api/getBySpecializationId', views.GetDoctorsBySpecializationId.as_view()),
    path('api/getSchedule', views.GetDoctorSchedule.as_view()),
    path('api/renderWorkspace', views.RenderProfileWorkspace.as_view()),
    path('api/addScheduleRecord', views.AddDoctorScheduleRecord.as_view()),
    path('api/deleteScheduleRecord', views.DeleteDoctorScheduleRecord.as_view()),
    path('api/acceptConsultation', views.AcceptConsultation.as_view()),
    path('api/denyConsultation', views.DenyConsultation.as_view()),
    path('api/createArticle', views.CreateArticle.as_view()),
    path('api/deleteArticle', views.DeleteArticle.as_view()),
    path('profile', views.DoctorIndexAPIView.as_view(), name="doctor-profile"),
    path('', views.DoctorIndexAPIView.as_view()),
    # path('/login', views.DoctorRegisterAPIView.as_view()),
    path('login', views.DoctorLoginAPIView.as_view(), name="doctor-login"),
]
