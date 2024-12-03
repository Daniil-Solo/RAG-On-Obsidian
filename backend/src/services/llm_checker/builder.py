from src.services.llm_checker.base import BaseChecker


class LLMCheckerBuilder:
    @staticmethod
    def build(vendor: str, model_name: str, token: str, base_url: str) -> BaseChecker:
        match vendor:
            case "GigaChat":
                from src.services.llm_checker.gigachat import GigaChatChecker
                return GigaChatChecker(auth_token=token, model=model_name)
            case "Mistral AI":
                from src.services.llm_checker.mistralai import MistralAIChecker
                return MistralAIChecker(token=token, model=model_name)
            case "dummy":
                from src.services.llm_checker.dummy import DummyChecker
                return DummyChecker()
            case _:
                raise NotImplementedError(f"Type {vendor} is unknown")
