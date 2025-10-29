from datetime import datetime
from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from frontend.utils.helpers import format_api_date
from frontend.utils.decorators import validate_session
from frontend.src.client.student import StudentAPIClient
from frontend.src.client.payment import PaymentAPIClient, PaymentMethodAPIClient, PaymentPackageAPIClient
from frontend.src.client.register import RegisterAPIClient



def get_list_current_page(request: HttpRequest) -> int:
    """
    Retorna a página atual da listagem de alunos salva na sessão.
    """
    return request.session.get("list_students_page", 1)


def handle_pagination(request: HttpRequest) -> bool:
    """
    Controla a navegação entre páginas na listagem de alunos.

    Retorna True se houver redirecionamento necessário (mudança de página).
    """
    if request.method == "POST":
        pagination = request.session.get("pagination", {})
        if "next" in request.POST and pagination.get("has_next_page"):
            request.session["list_students_page"] += 1
            return True
        if "previous" in request.POST and pagination.get("has_previous_page"):
            request.session["list_students_page"] -= 1
            return True
    return False


@validate_session
def list_students(request: HttpRequest) -> HttpResponse:
    """
    Lista alunos com suporte a busca e paginação via API.

    Atualiza o número da página atual na sessão e trata navegação entre páginas.
    """
    context: dict[str, Any] = {}
    client = StudentAPIClient()
    search: str = request.GET.get("search", "")

    if search:
        request.session["list_students_page"] = 1

    if handle_pagination(request):
        return redirect("list_students")

    response = client.list_students_paginated(
        request=request,
        page=get_list_current_page(request),
        search=search
    )

    if response.status_code == 200:
        data = response.json()
        context["students"] = data["results"]
        context["pagination"] = data["pagination"]
        request.session["list_students_page"] = data["pagination"]["current_page"]
        request.session["pagination"] = data["pagination"]
    else:
        messages.error(request, f"{response.json()}")
        return redirect("list_students")

    return render(
        request=request,
        template_name="list_students.html",
        context=context
    )


def show_error_message(request: HttpRequest, response: Any, extra_message: str) -> None:
    """
    Exibe uma mensagem de erro no template com base em uma resposta da API.
    """
    error = response.json().get("detail", response.status_code)
    messages.error(request, f"{extra_message}: {error}", extra_tags="danger")


def show_success_message(request: HttpRequest, extra_message: str) -> None:
    """
    Exibe uma mensagem de sucesso genérica.
    """
    messages.success(request, extra_message)


@validate_session
def add_student(request: HttpRequest) -> HttpResponse:
    """
    Cadastra um novo aluno via API e redireciona para os detalhes do aluno após sucesso.
    """
    if request.method == "POST":
        client = StudentAPIClient()
        response = client.add_student(
            request=request,
            name=request.POST["name"],
            phone=request.POST["phone"],
            reference=request.POST["reference"]
        )

        if response.status_code == 201:
            student_id = response.json()["id"]
            show_success_message(request, "Aluno matriculado com sucesso.")
            return redirect("detail_student", student_id=student_id)

        show_error_message(request, response, "Erro ao matricular")
        return redirect("add_student")

    return render(request, "add_student.html")


def ensure_register_is_open(request: HttpRequest, cash_register_list_open: Any) -> None:
    """
    Verifica se o caixa de hoje está aberto. Caso não esteja, o abre automaticamente.
    """
    today = datetime.today().date().strftime("%Y-%m-%d")
    registers = cash_register_list_open.json().get("results", [])
    if not any(i["register_date"] == today for i in registers):
        RegisterAPIClient().open_register(request)


@validate_session
def add_payment(request: HttpRequest, student_id: int) -> HttpResponse:
    """
    Cria um novo pagamento para um aluno.

    Carrega pacotes, caixas abertos e dados do aluno. Após criação, redireciona para adicionar valores.
    """
    context: dict[str, Any] = {}
    packages = PaymentPackageAPIClient().list_packages(request=request)
    open_registers = RegisterAPIClient().list_open_registers_only(request)
    student = StudentAPIClient().detail_student(request, student_id)

    ensure_register_is_open(request, open_registers)

    if request.method == "POST":
        package_id = request.POST.get("package")
        cash_register_id = request.POST.get("cash_register")

        new_payment = PaymentAPIClient(student_id=student_id).add_payment(
            request=request,
            payment_package=package_id,
            cash_register=cash_register_id
        )

        if new_payment.status_code == 201:
            messages.success(request, "Pagamento criado. Agora adicione o(s) valor(es) que foram recebidos.")
            return redirect("add_value", student_id=student_id, payment_id=new_payment.json()["id"])

        messages.error(request, f"Erro: {new_payment.json().get('detail')}", extra_tags="danger")
        return redirect("add_payment", student_id)

    if packages.status_code == 200:
        context["packages"] = packages.json()["results"]
    if open_registers.status_code == 200:
        context["open_registers"] = open_registers.json()["results"]
    if student.status_code == 200:
        context["student"] = student.json()

    return render(request, "add_payment.html", context)


@validate_session
def add_value(request: HttpRequest, student_id: int, payment_id: int) -> HttpResponse:
    """
    Adiciona valores a um pagamento existente.

    Também permite excluir valores ou finalizar o pagamento.
    """
    context: dict[str, Any] = {}
    methods = PaymentMethodAPIClient().list_methods(request)
    payment_client = PaymentAPIClient(student_id=student_id)
    payment_details = payment_client.detail_payment(request, payment_id)

    if methods.status_code == 200:
        context["methods"] = methods.json()["results"]
    else:
        messages.error(request, f"{methods.json()}")

    if payment_details.status_code == 200:
        context["payment_details"] = payment_details.json()
    else:
        messages.error(request, f"{payment_details.json()}", extra_tags="danger")

    if request.method == "POST":
        if "delete_value" in request.POST:
            return delete_payment_value(
                request=request,
                payment_id=payment_id,
                student_id=student_id,
                value_id=request.POST["delete_value"]
            )
        if "finish_payment" in request.POST:
            messages.success(request, "Pagamento registrado com sucesso.")
            return redirect("detail_student", student_id=student_id)

        new_value = payment_client.add_value(
            request=request,
            payment_id=payment_id,
            value=request.POST.get("value"),
            payment_method=request.POST.get("method")
        )

        if new_value.status_code == 201:
            messages.success(request, "Valor adicionado com sucesso.")
        else:
            show_error_message(request, new_value, "Erro ao adicionar valor")

        return redirect("add_value", student_id=student_id, payment_id=payment_id)

    return render(request, "add_value.html", context)


@validate_session
def delete_payment_value(request: HttpRequest, payment_id: int, student_id: int, value_id: int) -> HttpResponse:
    """
    Exclui um valor específico associado a um pagamento.
    """
    response = PaymentAPIClient(student_id=student_id).delete_value(
        request=request,
        payment_id=payment_id,
        value_id=value_id
    )

    if response.status_code == 204:
        messages.success(request, "Valor deletado.")
    else:
        messages.info(request, f"{response.url}")

    return redirect("add_value", student_id=student_id, payment_id=payment_id)


@validate_session
def detail_student(request: HttpRequest, student_id: int) -> HttpResponse:
    """
    Exibe os detalhes de um aluno, incluindo seus pagamentos e respectivas datas formatadas.
    """
    context: dict[str, Any] = {}
    client = StudentAPIClient()
    res = client.detail_student(request=request, student_id=student_id)
    payments = PaymentAPIClient(student_id=student_id).list_payments(request)

    if payments.status_code == 200:
        payment_list = payments.json()["results"]
        for item in payment_list:
            item["next_payment_date"] = format_api_date(
                original_date_str=item["next_payment_date"],
                original_format="%Y-%m-%d",
                desired_format="%d/%m de %Y"
            )
            item["created_at"] = format_api_date(
                original_date_str=item["created_at"],
                original_format="%Y-%m-%dT%H:%M:%S.%f%z",
                desired_format="%d/%m de %Y às %H:%M"
            )
        context["payments"] = payment_list

    if res.status_code == 200:
        context["student"] = res.json()

    return render(request, "detail_student.html", context)
