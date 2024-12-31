import json
import logging

import aiohttp

from src.services.llm_service.base import BaseLLMService, LLMError

CHECK_LINK = "https://api.mistral.ai/v1/chat/completions"
SUCCESS_HTTP_STATUS = 200

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
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
            async with client.post(CHECK_LINK, json=payload, headers=headers) as resp:
                logger.info(f"Model response status code: {resp.status}")
                result = await resp.content.read()
                logger.info(f"Model response content: {result}")
                if resp.status != SUCCESS_HTTP_STATUS:
                    try:
                        error_message = json.loads(result)["message"]
                        raise LLMError(error_message)
                    except json.decoder.JSONDecodeError as ex:
                        raise LLMError(result.decode("utf-8")) from ex
        result_dict = json.loads(result)
        self.input_tokens += result_dict["usage"]["prompt_tokens"]
        self.output_tokens += result_dict["usage"]["completion_tokens"]
        return result_dict["choices"][0]["message"]["content"]

    async def run(self, query: str) -> str:
        return await self._run_with_params(query, self.max_tokens)

    async def check(self) -> tuple[bool, str]:
        try:
            await self._run_with_params("You", 1)
        except LLMError as ex:
            return False, ex.message
        else:
            return True, ""

    async def get_used_tokens(self) -> tuple[int, int]:
        return self.input_tokens, self.output_tokens
