from django.contrib.auth.hashers import make_password, check_password
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView, Response
from django.http import HttpRequest
from doctors.models import Article
from main_pages.defs import get_user_type


class MainIndexAPIView(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):
        user_type = get_user_type(request=request)
        return Response(template_name="main_pages/index.html", data=dict(
            authorized_status=user_type
        ))


class ArticlesAPIView(APIView):

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request: HttpRequest, *args, **kwargs):
        user_type = get_user_type(request=request)
        return Response(template_name="main_pages/articles.html", data=dict(
            authorized_status=user_type,
            articles=[item.to_dict() for item in Article.objects.all()]
        ))
