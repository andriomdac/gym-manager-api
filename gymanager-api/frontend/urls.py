from django.urls import path

from frontend.views.add_student import add_student
from .views.session import (
    login,
    logout,
)
from .views.home import homepage


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('homepage/', homepage, name='homepage'),
    path('add-student/', add_student, name='add_student'),

]
