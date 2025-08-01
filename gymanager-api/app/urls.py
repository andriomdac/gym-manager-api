from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gyms/', include('gyms.urls')),
    path('api/students/', include('students.urls')),
]
