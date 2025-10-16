from django.shortcuts import render
from frontend.utils.decorators import validate_session


def add_student(request):
    return render(
        request=request,
        template_name="add_student.html"
    )
