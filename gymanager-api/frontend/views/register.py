from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from icecream import ic
from frontend.src.client.payment import PaymentAPIClient
from frontend.src.client.register import RegisterAPIClient
from frontend.utils.decorators import validate_session
from frontend.utils.helpers import format_api_date


@validate_session
def list_registers(request: HttpRequest) -> HttpResponse:
    """
    Lista todos os caixas (registers) disponíveis para o usuário logado.

    Faz chamada à API de registros, formata as datas retornadas e renderiza o template correspondente.
    """
    context: dict = {}
    client = RegisterAPIClient()
    response = client.list_registers(request)

    if response.status_code == 200:
        context["registers"] = response.json()["results"]
        for register in context["registers"]:
            register["register_date"] = format_api_date(
                original_date_str=register["register_date"],
                original_format="%Y-%m-%d",
                desired_format="%d/%m de %Y"
            )
    else:
        messages.error(request, f"{response.json()['detail']}", extra_tags="danger")

    return render(
        request=request,
        template_name="list_registers.html",
        context=context
    )


@validate_session
def redo_payment(request: HttpRequest, register_id: int, student_id: int, payment_id: int) -> HttpResponse:
    """
    Permite refazer um pagamento associado a um registro.

    Se confirmado via POST, deleta o pagamento anterior e redireciona para a criação de um novo.
    """
    context: dict = {"register_id": register_id}
    if request.method == "POST" and "confirm_redo" in request.POST:
        delete_payment = PaymentAPIClient(student_id).delete_payment(request, payment_id)
        if delete_payment.status_code == 204:
            messages.warning(request, "Pagamento antigo deletado. Realize o registro desse pagamento novamente.")
            return redirect("add_payment", student_id=student_id)
        messages.error(request, f"{delete_payment.json()}")
        return redirect("detail_register", register_id)
    return render(
        request=request,
        template_name="redo_payment.html",
        context=context
    )


@validate_session
def detail_register(request: HttpRequest, register_id: int) -> HttpResponse:
    """
    Exibe os detalhes de um caixa específico.

    Também permite redirecionar para o refazer de um pagamento, caso solicitado via POST.
    """
    context: dict = {}
    client = RegisterAPIClient()
    res = client.detail_register(request=request, register_id=register_id)
    if res.status_code == 200:
        context["register"] = res.json()

        for payment in context["register"]["payments"]:
            payment["created_at"] = format_api_date(
                original_date_str=payment["created_at"],
                original_format="%Y-%m-%dT%H:%M:%S.%f%z",
                desired_format="%H:%M"
            )
            total_values_amount = 0
            for value in payment["payment_values"]:
                total_values_amount += value["value"]

            payment["total_values_amount"] = total_values_amount
        context["register"]["register_date"] = format_api_date(
            original_date_str=context["register"]["register_date"],
            original_format="%Y-%m-%d",
            desired_format="%d/%m de %Y"
        )

    if request.method == "POST" and request.POST.get("action") == "redo_payment":
        student_id = request.POST["student_id"]
        payment_id = request.POST["payment_id"]
        return redirect("redo_payment", register_id=register_id, student_id=student_id, payment_id=payment_id)

    return render(
        request=request,
        template_name="detail_register.html",
        context=context
    )


@validate_session
def open_register(request: HttpRequest) -> HttpResponse:
    """
    Abre um novo caixa (register), para hoje ou para uma data específica.

    Envia requisição à API de registro e lida com mensagens de sucesso ou erro.
    """
    client = RegisterAPIClient()
    if request.method == "POST":
        if "today" in request.POST:
            res = client.open_register(request=request)
        elif "date" in request.POST:
            res = client.open_register(request=request, register_date=request.POST["date"])
        else:
            return render(request, "open_cash_register.html")

        if res.status_code == 201:
            messages.success(
                request,
                "Caixa aberto com sucesso." if "today" in request.POST
                else f"Caixa aberto com sucesso para a data {res.json()['register_date']}."
            )
            return redirect("homepage")

        error = res.json().get("detail", res.json())
        messages.error(request, f"Erro ao abrir caixa: {error}", extra_tags="danger")
        return redirect("open_register")

    return render(
        request=request,
        template_name="open_cash_register.html"
    )


@validate_session
def close_register(request: HttpRequest, register_id: int) -> HttpResponse:
    """
    Fecha o caixa especificado pelo ID.

    Em caso de sucesso, redireciona para a homepage. Caso contrário, exibe o erro.
    """
    context: dict = {"register_id": register_id}
    client = RegisterAPIClient()

    if request.method == "POST" and "close_register" in request.POST:
        res = client.close_register(request=request, register_id=register_id)
        if res.status_code == 200:
            messages.success(request, "Caixa Fechado. Encerrando os trabalhos!")
            return redirect("homepage")
        messages.error(request, f"{res.json()}")
        return redirect("close_register", register_id)

    return render(
        request=request,
        template_name="close_register.html",
        context=context
    )
