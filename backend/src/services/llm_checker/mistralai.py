import json
import aiohttp
import logging
from src.services.llm_checker.base import BaseChecker

CHECK_LINK = "https://api.mistral.ai/v1/chat/completions"

logger = logging.getLogger(__name__)


class MistralAIChecker(BaseChecker):
    def __init__(self, model: str, token: str) -> None:
        self.model = model
        self.token = token

    async def check(self) -> tuple[bool, str]:
        async with aiohttp.ClientSession() as client:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "You"
                    }
                ],
                "max_tokens": 1
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                "Authorization": f"Bearer {self.token}"
            }
            async with client.post(CHECK_LINK, json=payload, headers=headers) as resp:
                print(f"Model response status code: {resp.status}")
                result = await resp.content.read()
                print(f"Model response content: {result}")
                if resp.status != 200:
                    return False, json.loads(result).get("message")
        return True, ""
