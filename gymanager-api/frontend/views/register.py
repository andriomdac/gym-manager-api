from django.contrib import messages
from django.shortcuts import render, redirect
from frontend.utils.decorators import validate_session
from frontend.src.client.register import RegisterAPIClient


@validate_session
def list_registers(request):
    context = {}
    client = RegisterAPIClient()
    response = client.list_registers(request)

    if response.status_code == 200:
        context["registers"] = response.json()["results"]
    else:
        messages.error(request, f"{response.json()}", extra_tags="danger")

    return render(
        request=request,
        template_name="list_registers.html",
        context=context
    )


@validate_session
def detail_register(request, register_id):
    context = {}
    client = RegisterAPIClient()
    res = client.detail_register(
        request=request,
        register_id=register_id
    )

    if res.status_code == 200:
        context["register"] = res.json()

    return render(
        request=request,
        template_name="detail_register.html",
        context=context
    )


@validate_session
def open_register(request):
    client = RegisterAPIClient()
    if request.method == "POST":
        if "today" in request.POST:
            res = client.open_register(
                request=request,
            )
            if res.status_code == 201:
                messages.success(request, "Caixa de hoje aberto. Iniciando os trabalhos!")
                return redirect("homepage")
            else:
                error = res.json().get("detail", res.json())
                messages.error(request, f"Erro ao abrir caixa: {error}", extra_tags="danger")
                return redirect("open_register")
        if "date" in request.POST:
            res = client.open_register(
                request=request,
                register_date=request.POST["date"]
            )            
            if res.status_code == 201:
                messages.success(
                    request,
                    f"""
                    Caixa aberto com sucesso para a data {res.json()['register_date']}.
                    Agora é possível adicionar pagamentos para esta data
                    """
                )
                return redirect("homepage")
            else:
                error = res.json().get("detail", res.json())
                messages.error(request, f"Erro ao abrir caixa: {error}", extra_tags="danger")
                return redirect("open_register")

    return render(
        request=request,
        template_name="open_cash_register.html"
    )


@validate_session
def close_register(request, register_id):
    context = {"register_id": register_id}
    client = RegisterAPIClient()
    if request.method == "POST":
        if "close_register" in request.POST:
            res = client.close_register(
                request=request,
                register_id=register_id
            )
            if res.status_code == 200:
                messages.success(request, "Caixa Fechado. Encerrando os trabalhos!")
                return redirect("homepage")
            else:
                messages.error(request, f"{res.json()}")
        return redirect("close_register", register_id)
    return render(
        request=request,
        template_name="close_register.html",
        context=context
    )
