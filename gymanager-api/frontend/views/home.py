from frontend.utils.decorators import validate_session
from django.shortcuts import render


@validate_session
def homepage(request):
    return render(
        request=request,
        template_name='homepage.html'
    )
