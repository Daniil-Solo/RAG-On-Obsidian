from src.services.llm.llm_service import LLMService


class LLMServiceBuilder:
    @staticmethod
    def create(
        model_type: str,
        token: str = "",
        model_name: str = "",
        max_length: int | None = None,
    ) -> LLMService:
        match model_type:
            case "gigachat":
                from src.services.llm.gigachat import GigaChatLLMService
                return GigaChatLLMService(model_name=model_name, token=token, max_length=max_length)
            case "dummy":
                from src.services.llm.dummy import DummyLLMService
                return DummyLLMService()
            case _:
                ret = f"LLM type {model_type} is not an option."
                raise NotImplementedError(ret)
