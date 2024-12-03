import json
import aiohttp
import logging
import ssl
from src.services.llm_checker.base import BaseChecker

AUTH_LINK = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHECK_LINK = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

logger = logging.getLogger(__name__)


class GigaChatChecker(BaseChecker):
    def __init__(self, model: str, auth_token: str) -> None:
        self.model = model
        self.auth_token = auth_token

    async def check(self) -> tuple[bool, str]:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as client:
            auth_payload = {
                'scope': 'GIGACHAT_API_PERS'
            }
            auth_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'RqUID': '71d31622-ba00-4dfc-a4f9-46cb9b4c5c6b',
                'Authorization': f'Basic {self.auth_token}'
            }
            async with client.post(AUTH_LINK, data=auth_payload, headers=auth_headers, ssl=ssl_context) as resp:
                print(f"Auth response status code: {resp.status}")
                result = await resp.content.read()
                print(f"Auth response content: {result}")
                if resp.status != 200:
                    return False, json.loads(result).get("message")
                access_token = json.loads(result).get("access_token")

            check_payload = {
                "model": self.model,
                "messages": [
                    {
                      "role": "system",
                      "content": "Ты"
                    }
                ],
                "stream": False,
                "update_interval": 0,
                "max_tokens": 1
            }
            check_headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            async with client.post(CHECK_LINK, json=check_payload, headers=check_headers, ssl=ssl_context) as resp:
                print(f"Model response status code: {resp.status}")
                result = await resp.content.read()
                print(f"Model response content: {result}")
                if resp.status != 200:
                    return False, json.loads(result).get("message")
        return True, ""
