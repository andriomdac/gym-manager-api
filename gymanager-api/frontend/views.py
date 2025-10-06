from django.shortcuts import render, redirect
from django.contrib import messages
from frontend.src.client.token import TokenAPIClient
from frontend.src.client.student import StudentAPIClient
from frontend.utils.decorators import validate_session



@validate_session
def home(request):
    return render(
        request,
        template_name='base.html'
    )

@validate_session
def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        reference = request.POST.get("reference")

        response= StudentAPIClient(request).add_student(
            name=name,
            phone=phone,
            reference=reference
        )

        if response.status_code == 201:
            messages.success(request, f"Aluno {name} matriculado com sucesso.")
            return redirect("add_student")
        else:
            messages.error(request, f"{response.json().get("detail")}")
            return redirect("add_student")
    return render(
        request,
        "add_student.html",
    )


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

            return redirect("home")
        
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
