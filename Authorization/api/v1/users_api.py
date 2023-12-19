# In the name of GOD

from fastapi import APIRouter, Depends, status, Body
from fastapi.responses import Response, JSONResponse
import asyncio

from pydantic.fields import Field
import typing
import json

from models.users import UserLogin, UserRegister, UserUpdate, AuthorizationTokens
# from config.dependencies import get_service
from db.db import databases, collections
from services.account_service import AccountService
from services.notification_service import NotificationService
from auth.authentication import JWTAuthentication, EmailAuthentication
from .utils import renew_tokens, send_email
from config.dependencies import check_login_status



router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description":"Not found"}, 307: {"detail":"method not allowed"}},)

# ServiceDep = typing.Annotated[str, Depends(get_service)]
LoginDep = typing.Annotated[str, Depends(check_login_status)]

@router.post(
    "/register",
    response_description="Register new User",
    status_code=status.HTTP_201_CREATED,
)
async def register(user_data: UserRegister = Body(...)):

    data = user_data.model_dump(by_alias=True, exclude=["id", "password"])
    data['password'] = user_data.password.get_secret_value()
    register_response = await AccountService.register_user(data) # TODO
    if register_response.status_code == 201:
        new_user = UserRegister(**register_response.json())
        if new_user.email:
            otp = EmailAuthentication.create_and_store_otp(new_user.email)
            message = f"Dear {new_user.username} Welcome to our podcast website. Your email verfication code is {otp}"
            subject = "Welcome to Podcast"
            await send_email(new_user.email, new_user.username, subject, message) 
            return JSONResponse("Registered successfully and email verification code has sent to your email.")
        return JSONResponse("Registered successfully")
    return JSONResponse(register_response.json(), status_code=register_response.status_code)


@router.post(
    "/login",
    response_description="login with credentials",
    status_code=status.HTTP_200_OK,
)
async def login(login_data: UserLogin = Body(...)):

    data = login_data.model_dump(by_alias=True, exclude=["id", "password"])
    data['password'] = login_data.password.get_secret_value()

    login_response = await AccountService.login_user(data) # TODO
    if login_response.status_code == 200:
        new_user = UserLogin(**login_response.json())
        access_token, refresh_token = await renew_tokens(new_user.username, new_user.email)
        if new_user.email:
            message = f"Dear {new_user.username} Welcome to our podcast website."
            subject = "Welcome to Podcast"
            await send_email(new_user.email, new_user.username, subject, message)
        return JSONResponse({"data": {"access-token":access_token, "refresh-token":refresh_token}, "message":"login successfully"}, status_code=status.HTTP_200_OK)
    return JSONResponse(login_response.json(), status_code=login_response.status_code)

