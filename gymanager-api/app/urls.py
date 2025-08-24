from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gyms/', include('gyms.urls')),

    path('api/gyms/<str:gym_id>/students/', include('students.urls')), 
    path('api/gyms/<str:gym_id>/students/<str:student_id>/payments/', include('payments.urls')),

    path('api/gyms/<str:gym_id>/cash-registers/', include('cash_registers.urls')),

    path('api/payment-methods/', include('payment_methods.urls')),
    path('api/payment-packages/', include('payment_packages.urls')),
]
