import re
from django.shortcuts import render



def home(request):
    return render(
        request,
        template_name='home.html'
    )



def add_student(request):
    return render(
        request,
        template_name='add_student.html'
    )
