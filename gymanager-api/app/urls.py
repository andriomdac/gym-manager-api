from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', include('tokens.urls')),

    path('api/users/', include('profiles.urls')),
    path('api/roles/', include('roles.urls')),
    
    path('api/gyms/', include('gyms.urls')),

    path('api/students/', include('students.urls')), 
    path('api/students/<int:student_id>/payments/', include('payments.urls')),

    path('api/cash-registers/', include('cash_registers.urls')),

    path('api/payment-methods/', include('payment_methods.urls')),
    path('api/payment-packages/', include('payment_packages.urls')),
]
