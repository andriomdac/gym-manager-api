from hashlib import new
from django.shortcuts import render, redirect
from django.contrib import messages
from frontend.src.client.register import RegisterAPIClient
from frontend.src.client.token import TokenAPIClient
from frontend.src.client.payment import PaymentAPIClient, PaymentPackageAPIClient
from frontend.src.client.student import StudentAPIClient
from frontend.utils.decorators import validate_session
from icecream import ic


@validate_session
def home(request):
    return render(
        request,
        template_name='base.html'
    )


@validate_session
def detail_cash_register(request, register_id):
    context = {}
    response = RegisterAPIClient().detail_register(
        request=request,
        register_id=register_id
    )
    if response.status_code == 200:
        context["register"] = response.json()
        return render(
            request=request,
            template_name='detail_cash_register.html',
            context=context
        )

@validate_session
def list_cash_registers(request):
    client = RegisterAPIClient()
    registers = client.list_registers(request)
    if "open_register" in request.POST:
        new_register = client.open_register(request)
        if new_register.status_code == 201:
            messages.success(request, "Caixa criado com sucesso.")
        else:
            messages.error(request, f"Erro: {new_register.json()}", extra_tags="danger")
    context = {}
    if registers.status_code == 200:
        context["registers"] = registers.json()["results"]
    

    return render(
        request=request,
        template_name="list_cash_registers.html",
        context=context
    )


@validate_session
def add_payment(request, student_id):
    context = {}
    package_client = PaymentPackageAPIClient()
    payment_client = PaymentAPIClient(student_id)

    list_packages = package_client.list_packages(request)
    new_payment_response = payment_client.add_payment(request, 1)
    if new_payment_response.status_code == 201:
        context["payment_packages"] = list_packages.json()
        context["payment"] = new_payment_response.json()
    else:
        messages.error(request, f"{new_payment_response.json()}", extra_tags="danger")
        return redirect("detail_student", student_id)
    return render(
        request=request,
        template_name="add_payment.html",
        context=context
    )

@validate_session
def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        reference = request.POST.get("reference")
        response= StudentAPIClient().add_student(
            request=request,
            name=name,
            phone=phone,
            reference=reference
        )

        if response.status_code == 201:
            messages.success(request, f"Aluno {name} matriculado com sucesso.")
            return redirect("add_student")
        else:
            if "detail" in response.json():
                messages.error(request, f"{response.json()["detail"]}", extra_tags="danger")
                return redirect("add_student")
            target_fields = ["name", "phone", "reference"]
            if any(field in response.json() for field in target_fields):
                fields_translated = {
                    "name": "nome",
                    "phone": "telefone",
                    "reference": "referência"
                }
                missing_fields = [fields_translated[field] for field in response.json()]
                messages.error(request, f"Os seguintes campos são obrigatórios: {missing_fields}", extra_tags="danger")
            else:
                messages.error(request, f"erro: {response.json()}", extra_tags="danger")
            
    return render(
        request,
        "add_student.html",
    )


@validate_session
def detail_student(request, student_id):
    response = StudentAPIClient().detail_student(request, student_id)
    student = response.json()
    context = {}
    if response.status_code == 200:
        context["student"] = student
    else:
        return not_found(
            request,
            message=f"Erro: {response.json()['detail']}",
            view_name="detail_student"
        )

    return render(
        request=request,
        template_name="detail_student.html",
        context=context
    )


@validate_session
def list_students(request):
    client = StudentAPIClient()
    context = {}
    page = 1
    if "list_students_page" in request.session:
        page = request.session["list_students_page"]
        if page < 1:
            page = 1

    if "previous" in request.POST:
        request.session["list_students_page"] = int(page) - 1
        return redirect("list_students")
    if "next" in request.POST:
        ic(request.session["list_students_page"])
        request.session["list_students_page"] = int(page) + 1
        return redirect("list_students")

    response = client.list_students_paginated(request=request, page=page)
    if response.status_code == 200:
        response = response.json()
        context["count"] = response["count"]
        context["students"] = response["results"]
        context["page"] = page
        return render(
            request,
            'list_students.html',
            context=context
        )
    else:
        response = response.json()
        return not_found(request, f"{response["detail"]}", view_name="list_students")


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


def not_found(request, message: str, view_name: str):
    if f"{view_name}_page" in request.session:
        request.session[f"{view_name}_page"] =- 1
        return redirect(f"{view_name}")
    return render(
        request=request,
        template_name="not_found.html",
        context={"message": message}
    )
