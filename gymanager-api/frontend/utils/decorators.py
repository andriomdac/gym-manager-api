from django.shortcuts import redirect
from frontend.src.client.token import TokenAPIClient

def validate_session(func):
    def wrapper(request, *args, **kwargs):
        if "access" in request.session and "refresh" in request.session:
            access = request.session['access']
            refresh = request.session['refresh']

            client = TokenAPIClient()
            verify = client.verify_token(access_token=access)

            if verify.status_code == 200:
                return func(request, *args, **kwargs) 
            else:
                refresh = client.refresh_token(refresh_token=refresh)
                if refresh.status_code == 200:
                    request.session["access"] = refresh.json()["access"]
                    return redirect("home")
        return redirect(to="login")
    return wrapper
