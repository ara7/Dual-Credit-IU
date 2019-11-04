from django.urls import path
from django.conf.urls import re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about')
]