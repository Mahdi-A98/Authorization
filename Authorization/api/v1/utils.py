# in the name of GOD

from auth.authentication import JWTAuthentication, EmailAuthentication
from services.notification_service import NotificationService
from utils.celery_tasks import send_email_task
import asyncio

async def renew_tokens(username, email):
    JWTAuthentication.delete_old_user_login_tokens(username)
    access_token = JWTAuthentication.create_access_token({"username":username, "email":email})
    refresh_token = JWTAuthentication.create_refresh_token({"username":username, "email":email})
    return access_token, refresh_token


async def send_email(email, username=None, subject=None, message=None):
    email_data ={"reciever_username":username, "reciever_email":email, "subject": subject, "message":message}
    response = send_email_task.delay(email_data)
    print(f"{response=}")
    # response = await NotificationService.send_email_notification(email_data)
    return response