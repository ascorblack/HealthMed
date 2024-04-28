from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.MainIndexAPIView.as_view(), name="main"),
    path('articles/', views.ArticlesAPIView.as_view(), name="articles"),
]
