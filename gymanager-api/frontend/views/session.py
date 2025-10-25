from django.shortcuts import render, redirect
from frontend.src.client.token import TokenAPIClient
from frontend.utils.decorators import validate_session


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        response = TokenAPIClient().get_token(
            username=username,
            password=password
        )
        if response.status_code == 200:
            access_token = response.json()["access"]
            refresh_token = response.json()["refresh"]

            request.session["access"] = access_token
            request.session["refresh"] = refresh_token
            request.session["user"] = username

            return redirect("homepage")
        
    return render(
        request,
        template_name='login.html'
    )


def logout(request):
    if 'access' in request.session:
        del request.session['access']
    if 'refresh' in request.session:
        del request.session['refresh']
    return redirect("login")
