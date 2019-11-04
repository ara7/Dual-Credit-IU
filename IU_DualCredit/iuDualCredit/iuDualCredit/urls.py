from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static

urlpatterns = [
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
