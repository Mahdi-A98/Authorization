# In the name of GOD

# In the name of GOD
import httpx
import requests
import json
from fastapi import Body

from config import settings
from utils.secure_communicate import Encryption

class PodcastService:
    code_keys = {"auth_pod_key1":settings.AUTH_POD_KEY1}
    Encrypt_tools = Encryption(settings.POD_AUTH_SHARED_KEY, code_keys)

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