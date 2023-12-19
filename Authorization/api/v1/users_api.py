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
