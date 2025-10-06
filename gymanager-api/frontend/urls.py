from django.urls import path
from .views import add_student, home, login, logout


urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('add-student', add_student, name='add_student')
]
