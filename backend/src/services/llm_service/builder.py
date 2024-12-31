import logging

from src.services.llm_service.base import BaseLLMService

logger = logging.getLogger(__name__)


class LLMServiceBuilder:
    @staticmethod
    def build(vendor: str, model: str, token: str, base_url: str, max_tokens: int) -> BaseLLMService:  # noqa: ARG004
        match vendor:
            case "GigaChat":
                from src.services.llm_service.gigachat import GigaChatLLMService
                logger.info("Using GigaChat LLM Service")
                return GigaChatLLMService(auth_token=token, model=model, max_tokens=max_tokens)
            case "Mistral AI":
                from src.services.llm_service.mistralai import MistralAILLMService
                logger.info("Using Mistral AI LLM Service")
                return MistralAILLMService(token=token, model=model, max_tokens=max_tokens)
            case "dummy":
                from src.services.llm_service.dummy import DummyLLMService
                logger.info("Using Dummy LLM Service")
                return DummyLLMService()
            case _:
                error_text = f"Type {vendor} is unknown"
                raise NotImplementedError(error_text)
