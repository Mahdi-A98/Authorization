async def check_login_status(request: Request):
    access_token = request.headers.get("access-token")
    refresh_token = request.headers.get("refresh-token")
    username, email = JWTAuthentication.authenticate(access_token, refresh_token)
    return username, email