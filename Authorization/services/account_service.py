# In the name of GOD

import httpx
import json

from config import settings
from utils.secure_communicate import Encryption

class AccountService:
    code_keys = {"auth_acc_key1":settings.AUTH_ACC_KEY1, "auth_acc_key2":settings.AUTH_ACC_KEY2, "auth_acc_key3": settings.AUTH_ACC_KEY3}    
    Encrypt_tools = Encryption(settings.ACCOUNT_AUTH_SHARED_KEY, code_keys)

    @classmethod
    async def register_user(cls, data):
        url = settings.ACCOUNT_SERVICE_URL + '/users/register'
        response = await cls.encrypt_and_send(data, url)
        return response        

    @classmethod
    async def login_user(cls, data):
        url = settings.ACCOUNT_SERVICE_URL + '/users/login'
        response = await cls.encrypt_and_send(data, url)
        return response        

    @classmethod
    async def update_user_data(cls, data):
        url = settings.ACCOUNT_SERVICE_URL + '/users/update_user_data'
        response = await cls.encrypt_and_send(data, url)
        return response        


    @classmethod
    async def user_profile(cls, data):
        url = settings.ACCOUNT_SERVICE_URL + '/users/user_profile_X'
        response = await cls.encrypt_and_send(data, url)
        return response        

    @classmethod
    async def encrypt_and_send(cls, data, url, headers={}):
        encrypted_data = cls.Encrypt_tools.encrypt_data(data)
        async with httpx.AsyncClient(trust_env=False) as client:
            headers.update({"internal-service":"authentication"})
            response = await client.post(url=url, data=json.dumps(encrypted_data), headers=headers)
        response._content = json.loads(cls.Encrypt_tools.decrypt_data(response.content)) if response.content else response.content
        return response        

