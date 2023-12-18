# In the name of GOD
from fastapi import Header, HTTPException, Request
from typing import Annotated

from services import SERVICE_CLASSES
from auth.authentication import JWTAuthentication


async def get_service(internal_service: Annotated[str, Header()]):
    if not SERVICE_CLASSES.get(internal_service):
        raise HTTPException(detail="Access denied.", status_code=403)
    return SERVICE_CLASSES.get(internal_service)

async def check_login_status(request: Request):
    access_token = request.headers.get("access-token")
    refresh_token = request.headers.get("refresh-token")
    username, email = JWTAuthentication.authenticate(access_token, refresh_token)
    return username, email