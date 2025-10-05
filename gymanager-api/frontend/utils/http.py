def build_api_headers(request) -> dict:
    access_token = request.session.get("access_token")
    return {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json" 
            }
