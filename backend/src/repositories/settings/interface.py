from abc import ABC, abstractmethod


class SettingsRepository(ABC):
    @abstractmethod
    async def get_llm_settings(self) -> dict | None:
        raise NotImplementedError

    @abstractmethod
    async def update_llm_settings(
        self,
        vendor: str,
        token: str,
        model: str,
        base_url: str,
        max_tokens: int,
    ) -> None:
        raise NotImplementedError
