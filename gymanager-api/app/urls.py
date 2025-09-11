from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/users/', include('profiles.urls')),
    
    path('api/gyms/', include('gyms.urls')),

    path('api/gyms/<str:gym_id>/students/', include('students.urls')), 
    path('api/gyms/<str:gym_id>/students/<str:student_id>/payments/', include('payments.urls')),

    path('api/gyms/<str:gym_id>/cash-registers/', include('cash_registers.urls')),

    path('api/payment-methods/', include('payment_methods.urls')),
    path('api/payment-packages/', include('payment_packages.urls')),
]