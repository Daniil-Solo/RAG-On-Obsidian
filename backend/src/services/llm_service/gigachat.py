import json
import logging
import ssl

import aiohttp

from src.services.llm_service.base import BaseLLMService, LLMError

AUTH_LINK = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
CHECK_LINK = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
SUCCESS_HTTP_STATUS = 200

logger = logging.getLogger(__name__)


class GigaChatLLMService(BaseLLMService):
    def __init__(self, model: str, auth_token: str, max_tokens: int) -> None:
        self.model = model
        self.auth_token = auth_token
        self.max_tokens = max_tokens
        self.input_tokens = 0
        self.output_tokens = 0

    async def _run_with_params(self, query: str, max_tokens: int) -> str:
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        async with aiohttp.ClientSession() as client:
            auth_payload = {
                "scope": "GIGACHAT_API_PERS"
            }
            auth_headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "RqUID": "71d31622-ba00-4dfc-a4f9-46cb9b4c5c6b",
                "Authorization": f"Basic {self.auth_token}"
            }
            async with client.post(AUTH_LINK, data=auth_payload, headers=auth_headers, ssl=ssl_context) as resp:
                result = await resp.content.read()
                if resp.status != SUCCESS_HTTP_STATUS:
                    raise LLMError(message=json.loads(result)["message"])
                access_token = json.loads(result).get("access_token")

            check_payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": query
                    }
                ],
                "stream": False,
                "update_interval": 0,
                "max_tokens": max_tokens
            }
            check_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            async with client.post(CHECK_LINK, json=check_payload, headers=check_headers, ssl=ssl_context) as resp:
                logger.info(f"Model response status code: {resp.status}")
                result = await resp.content.read()
                logger.info(f"Model response content: {result}")
                if resp.status != SUCCESS_HTTP_STATUS:
                    raise LLMError(message=json.loads(result)["message"])
        result_dict = json.loads(result)
        self.input_tokens += result_dict["usage"]["prompt_tokens"]
        self.output_tokens += result_dict["usage"]["completion_tokens"]
        return result_dict["choices"][0]["message"]["content"]

    async def run(self, query: str) -> str:
        return await self._run_with_params(query, self.max_tokens)

    async def check(self) -> tuple[bool, str]:
        try:
            await self._run_with_params("Ты", 1)
        except LLMError as ex:
            return False, ex.message
        else:
            return True, ""

    async def get_used_tokens(self) -> tuple[int, int]:
        return self.input_tokens, self.output_tokens
