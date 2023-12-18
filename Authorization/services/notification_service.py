# In the name of GOD
import httpx
import requests
import json
from fastapi import Body

from config import settings
from utils.secure_communicate import Encryption

class NotificationService:
    code_keys = {"auth_ntf_key1":settings.AUTH_NTF_KEY1, "auth_ntf_key2":settings.AUTH_NTF_KEY2, "auth_ntf_key3": settings.AUTH_NTF_KEY3}
    Encrypt_tools = Encryption(settings.NTF_AUTH_SHARED_KEY, code_keys)

    @classmethod
    async def send_email_notification(cls, data):
        url = settings.NOTIFICATION_SERVICE_URL + '/notification/send_email_notification'
        response = await cls.encrypt_and_send(data, url)
        return response   


    @classmethod
    def sinc_send_email_notification(cls, data):
        url = settings.NOTIFICATION_SERVICE_URL + '/notification/send_email_notification'
        response = cls.sinc_encrypt_and_send(data, url)
        return response   

    @classmethod
    async def encrypt_and_send(cls, data, url, headers={}):
        encrypted_data = cls.Encrypt_tools.encrypt_data(data)
        headers.update({"internal-service":"authentication"})
        async with httpx.AsyncClient() as client:
            # timeout = httpx.TimeoutConfig(connect_timeout=5, read_timeout=5 * 60, write_timeout=5)
            response = await client.post(url=url, data=json.dumps(encrypted_data), headers=headers)
            if response.status_code >= 500:
                return response
            response._content = json.loads(cls.Encrypt_tools.decrypt_data(response.content))
            return response       

    @classmethod
    def sinc_encrypt_and_send(cls, data, url, headers={}):
        encrypted_data = cls.Encrypt_tools.encrypt_data(data)
        headers.update({"internal-service":"authentication"})
        response = requests.post(url, data=json.dumps(encrypted_data), headers=headers)
        if response.status_code >= 500:
                return response
        response._content = json.loads(cls.Encrypt_tools.decrypt_data(response.content))
        return response       