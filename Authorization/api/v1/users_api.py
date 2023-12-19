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


@router.post(
    "/authorize_token",
    response_description="authorize token",
    status_code=status.HTTP_202_ACCEPTED,
)
async def authorize_token(authorization_tokens:AuthorizationTokens= Body(...)):
    access_token = authorization_tokens.access_token
    refresh_token = authorization_tokens.refresh_token
    username, email = JWTAuthentication.authenticate(access_token, refresh_token)
    return JSONResponse({"data": {"username": username, "email": email}, "message":"Token Authorized successfuy"}, status_code=status.HTTP_200_OK)


@router.post(
    "/send_otp",
    response_description="verify email",
    status_code=status.HTTP_200_OK,
)
async def send_otp(email_verification_data:dict= Body(...)):
    email = email_verification_data.get("email")
    otp = EmailAuthentication.create_and_store_otp(email, prefix_key="email_verification")
    message = f"podcast website. Your email verfication code is {otp}"
    await send_email(email=email, subject="verify email", message=message)
    return JSONResponse("otp has sent to your email", status_code=status.HTTP_200_OK)


@router.post(
    "/verify_email",
    response_description="verify email",
    status_code=status.HTTP_202_ACCEPTED,
)
async def verify_email(email_verification_data:dict= Body(...)):
    email = email_verification_data.get("email")
    otp = email_verification_data.get("otp")
    is_email_verified  = EmailAuthentication.verify_otp(email, otp, prefix_key="email_verification")
    if is_email_verified:
        result = await AccountService.update_user_data({"user_data": {"email":email}, "update_data": {"is_email_verified": True}}) # TODO
        mapped_result = {
            202:JSONResponse("Your email verified successfully", status_code=status.HTTP_202_ACCEPTED),
            404:JSONResponse("User with this email doesn't exist", status_code=status.HTTP_404_NOT_FOUND),
            215:JSONResponse("This email is already verified", status_code=215),
        }

        return mapped_result.get(result.status_code)
    return JSONResponse("Invalid otp", status_code=status.HTTP_401_UNAUTHORIZED)


@router.post(
    "/send_login_otp",
    response_description="login with email otp",
    status_code=status.HTTP_200_OK,
)
async def send_login_otp(email_verification_data:dict= Body(...)):
    email = email_verification_data.get("email")
    otp = EmailAuthentication.create_and_store_otp(email=email, prefix_key="login_verification@")
    message = f"podcast website. Your login code is {otp}"
    await send_email(email=email, subject="login code", message=message)
    return JSONResponse("login code has sent to your email", status_code=status.HTTP_200_OK)


@router.post(
    "/login_with_otp",
    response_description="login with otp")
async def verify_login_code(email_login_data:dict= Body(...)):
    email = email_login_data.get("email")
    otp = email_login_data.get("otp")
    account_response = await AccountService.user_profile({"email":email})
    if account_response.status_code == 404:
        return JSONResponse("User with this email doesn't exist", status_code=status.HTTP_404_NOT_FOUND)
    user_profile = account_response.json()
    user_profile = account_response.json().get("data")
    is_login_code_verified  = EmailAuthentication.verify_otp(email, otp, prefix_key="login_verification@")
    if is_login_code_verified and user_profile.get("is_email_verified"):
        access_token, refresh_token = await renew_tokens(user_profile.get("username"), user_profile.get("email"))
        return JSONResponse({"data": {"access-token":access_token, "refresh-token":refresh_token}, "message":"login successfully"}, status_code=status.HTTP_200_OK)
    return JSONResponse("Invalid otp", status_code=status.HTTP_401_UNAUTHORIZED)


@router.post(
    "/logout",
    response_description="logout user")
async def logout(user_data:LoginDep):
    username = user_data[0]
    JWTAuthentication.delete_old_user_login_tokens(username)
    return JSONResponse({"message": f"{username} logged out successfully"}, status_code=status.HTTP_200_OK)