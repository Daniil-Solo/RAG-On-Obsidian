from src.services.llm_service.base import BaseLLMService


class LLMServiceBuilder:
    @staticmethod
    def build(vendor: str, model: str, token: str, base_url: str, max_tokens: int, **kwargs) -> BaseLLMService:
        match vendor:
            case "GigaChat":
                from src.services.llm_service.gigachat import GigaChatLLMService
                return GigaChatLLMService(auth_token=token, model=model, max_tokens=max_tokens)
            case "Mistral AI":
                from src.services.llm_service.mistralai import MistralAILLMService
                return MistralAILLMService(token=token, model=model, max_tokens=max_tokens)
            case "dummy":
                from src.services.llm_service.dummy import DummyLLMService
                return DummyLLMService()
            case _:
                raise NotImplementedError(f"Type {vendor} is unknown")
