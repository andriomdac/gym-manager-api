def build_api_headers(request) -> dict:
    return {
                "Authorization": f"Bearer {request.session.get('access')}",
                "Content-Type": "application/json" 
            }
