from . import views
from django.urls import path, include

urlpatterns = [
    path('profile/', views.UsersIndexAPIView.as_view(), name="profile"),
    path('api/registerPatient', views.RegisterPatient.as_view()),
    path('api/loginPatient', views.LoginPatient.as_view()),
    path('api/logOut', views.LogOut.as_view()),
    path('api/renderWorkspace', views.RenderProfileWorkspace.as_view()),
    path('api/makeAppointment', views.MakePatientAppointment.as_view()),
    path('api/denyAppointment', views.DenyPatientAppointment.as_view()),
    path('api/editInfo', views.EditPatientData.as_view()),
    path('api/makeConsultationRequest', views.MakePatientConsultationRequest.as_view()),
    path('api/deleteConsultation', views.DeletePatientConsultationRequest.as_view()),
]
