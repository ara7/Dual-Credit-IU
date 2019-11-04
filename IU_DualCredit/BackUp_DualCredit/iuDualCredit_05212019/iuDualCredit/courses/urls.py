from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='courses'),
    path('coursesearch/', views.courseSearch, name='coursesearch'),
    #path('<int:course_id>', views.courseDetailView, name='courseDetail'),
    path('courseDetailView/<int:course_id>', views.courseDetailView, name='courseDetailView'),
    path('exportcsv', views.exportcsv, name='exportcsv')
]