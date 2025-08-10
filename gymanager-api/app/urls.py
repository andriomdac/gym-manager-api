from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gyms/', include('gyms.urls')),
    path('api/students/', include('students.urls')),
    path('api/students/<str:student_id>/payments/', include('payments.urls')),
    path('api/payment_methods/', include('payment_methods.urls')),
    path('api/payment_packages/', include('payment_packages.urls')),
    path('api/cash_registers/', include('cash_registers.urls')),
]
