from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def gym_list_create_view(request: Request) -> Response:
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
    return Response({"message": "working"})