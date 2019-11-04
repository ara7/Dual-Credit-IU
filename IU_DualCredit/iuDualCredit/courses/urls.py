from django.urls import include, path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='courses'),
    path('coursesearch/', views.courseSearch, name='coursesearch'),
    path('courseDetailView/<str:courseinfo>', views.courseDetailView, name='courseDetailView'),
    path('courseDetailView/', views.courseDetailView, name='courseDetailView'),
    path('exportcsv', views.exportcsv, name='exportcsv')
]


