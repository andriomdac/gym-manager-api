from django.urls import path
from .views import (
    add_payment,
    add_student,
    detail_cash_register,
    detail_student,
    home,
    list_cash_registers,
    list_students,
    login,
    logout,
)


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('add-student/', add_student, name='add_student'),
    path('list-students/', list_students, name='list_students'),
    path('detail-student/<int:student_id>/', detail_student, name='detail_student'),

    path('add-payment/<int:student_id>/', add_payment, name='add_payment'),


    path('cash-registers/', list_cash_registers, name='list_cash_registers'),
    path('cash-registers/<int:register_id>/', detail_cash_register, name='detail_cash_register'),
]
