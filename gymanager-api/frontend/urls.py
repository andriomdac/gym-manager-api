from django.urls import path

from frontend.views.student import add_payment, add_value, detail_student, list_students, add_student
from frontend.views.register import close_register, detail_register, list_registers, open_register, redo_payment
from .views.session import (
    login,
    logout,
)
from .views.home import homepage


urlpatterns = [
    path('', homepage, name='homepage'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('add-student/', add_student, name='add_student'),
    path('list-students/', list_students, name='list_students'),
    path('detail-student/<int:student_id>/', detail_student, name='detail_student'),
    path('detail-student/<int:student_id>/payment/', add_payment, name='add_payment'),
    path('detail-student/<int:student_id>/payment/<int:payment_id>/add-value/', add_value,name='add_value'),



    path('cash-registers/', list_registers, name='list_registers'),
    path('open-register/', open_register, name='open_register'),
    path('detail-register/<int:register_id>/', detail_register, name='detail_register'),
    path('detail-register/<int:register_id>/student/<int:student_id>/payment/<int:payment_id>/', redo_payment, name='redo_payment'),
    path('close-register/<int:register_id>/', close_register, name='close_register'),






]
