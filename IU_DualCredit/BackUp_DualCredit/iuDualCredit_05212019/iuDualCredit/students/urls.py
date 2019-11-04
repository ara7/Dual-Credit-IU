from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='students'),
    #path('search', views.studentSearch, name='search'),
    path('studentDetailView/<int:student_uid>', views.studentDetailView, name='studentDetailView'),
    path('studentsearch/', views.studentSearch, name='studentsearch'),
    path('exportcsv', views.exportcsv, name='exportcsv')
]