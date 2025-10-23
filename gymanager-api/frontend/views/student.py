from django.shortcuts import redirect, render
from django.utils.http import content_disposition_header
from icecream import ic
from frontend.utils.decorators import validate_session
from django.contrib import messages
from frontend.src.client.student import StudentAPIClient
from frontend.src.client.payment import PaymentAPIClient, PaymentMethodAPIClient, PaymentPackageAPIClient
from frontend.src.client.register import RegisterAPIClient


def get_list_current_page(request):
    if "list_students_page" in request.session:
        return request.session["list_students_page"]
    return 1

@validate_session
def list_students(request):

    context = {}
    client = StudentAPIClient()
    response = client.list_students_paginated(
        request=request,
        page=get_list_current_page(request)
    )

    if response.status_code == 200:
        context["students"] = response.json()["results"]
        context["pagination"] = response.json()["pagination"]
        request.session["list_students_page"] = context["pagination"]["current_page"]
        request.session["pagination"] = context["pagination"]
    else:
        messages.error(request, f"{response.json()}")
        return redirect("list_students")

    if request.method == "POST":
        if "next" in request.POST:
            if request.session["pagination"]["has_next_page"]:
                request.session["list_students_page"] += 1
            return redirect("list_students")
        if "previous" in request.POST:
            if request.session["pagination"]["has_previous_page"]:
                request.session["list_students_page"] -= 1
            return redirect("list_students")

    return render(
        request=request,
        template_name="list_students.html",
        context=context
    )


@validate_session
def add_student(request):
    if request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        reference = request.POST["reference"]

        client = StudentAPIClient()
        response = client.add_student(
            request=request,
            name=name,
            phone=phone,
            reference=reference
        )

        if response.status_code == 201:
            messages.success(request, "Aluno matriculado com sucesso.") 
        else:
            if "detail" in response.json():
                error = response.json()['detail']
            else:
                error = response.status_code
            messages.error(request, f"Erro ao matricular: {error}", extra_tags="danger")

        return redirect("add_student")
    return render(
        request=request,
        template_name="add_student.html"
    )



@validate_session
def add_payment(request, student_id):
    context = {}
    packages = PaymentPackageAPIClient().list_packages(request=request)
    cash_register_list_open = RegisterAPIClient().list_open_registers_only(request)
    
    if request.method == "POST":
        package_id = None
        cash_register_id = None

        if "package" in request.POST:
            package_id = request.POST["package"]
        if "cash_register" in request.POST:
            cash_register_id = request.POST["cash_register"]
        
        new_payment = PaymentAPIClient(student_id=student_id).add_payment(
            request=request,
            payment_package=package_id,
            cash_register=cash_register_id
        )

        if new_payment.status_code == 201:
            messages.success(request, "Pagamento criado ")
            return redirect("add_value", student_id=student_id, payment_id=new_payment.json()["id"])
        else:
            messages.error(request, f"Erro: {new_payment.content}", extra_tags="danger")
        return redirect("add_payment", student_id)


    if packages.status_code == 200:
        context["packages"] = packages.json()["results"]
    if cash_register_list_open.status_code == 200:
        context["open_registers"] = cash_register_list_open.json()["results"]
        
    return render(
        request=request,
        template_name="add_payment.html",
        context=context
    )


@validate_session
def add_value(request, student_id, payment_id):
    context = {}
    methods = PaymentMethodAPIClient().list_methods(request)
    payment_client = PaymentAPIClient(student_id=student_id)
    
    payment_details = payment_client.detail_payment(
        request=request,
        payment_id=payment_id
    )
    
    if methods.status_code == 200:
        context["methods"] = methods.json()["results"]
    else:
        messages.error(request, f"{methods.json()}")
    if payment_details.status_code == 200:
        context["payment_details"] = payment_details.json()
    else:
        messages.error(request, f"{payment_details.json()}")

    if request.method == "POST":
        if "delete_value" in request.POST:
            return delete_payment_value(
                request=request,
                payment_id=payment_id,
                student_id=student_id,
                value_id=request.POST["delete_value"]
            )
        if "finish_payment" in request.POST:
            messages.success(request, "Pagamento Registrado com sucesso.")
            return redirect("homepage")
            
        value = None
        method = None
        if "value" in request.POST:
            value = request.POST["value"]
        if "method" in request.POST:
            method = request.POST["method"]
        
        new_value = payment_client.add_value(
            request=request,
            payment_id=payment_id,
            value=value,
            payment_method=method
        )

        if new_value.status_code == 201:
            messages.success(request, "Valor adicionado")
        else:
            messages.error(request, f"{new_value.json()}")
        return redirect("add_value", student_id=student_id, payment_id=payment_id)


    return render(
        request=request,
        template_name="add_value.html",
        context=context
    )


@validate_session
def delete_payment_value(request, payment_id, student_id, value_id):
    response = PaymentAPIClient(
        student_id=student_id
    ).delete_value(
            request=request,
            payment_id=payment_id,
            value_id=value_id
        )    
    if response.status_code == 204:
        messages.success(request, "Valor deletado")
    else:
        messages.info(request, f"{response.url}")
    return redirect(
        "add_value",
        student_id=student_id,
        payment_id=payment_id
    )


@validate_session
def detail_student(request, student_id):
    context = {}
    client = StudentAPIClient()
    res = client.detail_student(
        request=request,
        student_id=student_id
    )
    payments = PaymentAPIClient(student_id=student_id).list_payments(request)

    if payments.status_code == 200:
        context["payments"] = payments.json()["results"]
    
    if res.status_code == 200:
        context["student"] = res.json()

    return render(
        request=request,
        template_name="detail_student.html",
        context=context
)
