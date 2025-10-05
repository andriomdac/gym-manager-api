import re
from django.shortcuts import render



def home(request):
    return render(
        request,
        template_name='base.html'
    )


def login(request):
    return render(
        request,
        template_name='login.html'
    )
