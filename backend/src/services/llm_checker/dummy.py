from src.services.llm_checker.base import BaseChecker


class DummyChecker(BaseChecker):
    async def check(self) -> tuple[bool, str]:
        return True, ""
