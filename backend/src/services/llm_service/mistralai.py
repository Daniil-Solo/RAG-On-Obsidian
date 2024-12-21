import json
import aiohttp
import logging
from src.services.llm_service.base import BaseLLMService, LLMException

CHECK_LINK = "https://api.mistral.ai/v1/chat/completions"

logger = logging.getLogger(__name__)


class MistralAILLMService(BaseLLMService):
    def __init__(self, model: str, token: str, max_tokens: int) -> None:
        self.model = model
        self.token = token
        self.max_tokens = max_tokens
        self.input_tokens = 0
        self.output_tokens = 0

    async def _run_with_params(self, query: str, max_tokens: int) -> str:
        async with aiohttp.ClientSession() as client:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "max_tokens": max_tokens
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
                    raise LLMException(json.loads(result)["message"])
        result_dict = json.loads(result)
        self.input_tokens += result_dict["usage"]["prompt_tokens"]
        self.output_tokens += result_dict["usage"]["completion_tokens"]
        return result_dict["choices"][0]["message"]["content"]

    async def run(self, query: str) -> str:
        return await self._run_with_params(query, self.max_tokens)

    async def check(self) -> tuple[bool, str]:
        try:
            await self._run_with_params("You", 1)
            return True, ""
        except LLMException as ex:
            return False, ex.message

    async def get_used_tokens(self) -> tuple[int, int]:
        return self.input_tokens, self.output_tokens
