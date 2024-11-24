from abc import ABC, abstractmethod


class SettingsRepository(ABC):
    @abstractmethod
    async def get_llm_settings(self) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def update_llm_settings(
        self,
        model_type: str,
        token: str,
        model_name: str,
        max_length: int,
    ) -> None:
        raise NotImplementedError
